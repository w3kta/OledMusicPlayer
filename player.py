import os
import time
import subprocess
import threading
import json
import socket
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from gpiozero import Button
from PIL import ImageFont

# Buttons
up = Button(4)
down = Button(17)
enter = Button(27)
back = Button(22)
volumeup = Button(24)
volumedown = Button(23)

# OLED setup
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# Constants
MAX_VISIBLE = 6
MAX_CHARACTERS = 25
font = ImageFont.load_default()

# State
BASE_PATH = "/media"
current_path = BASE_PATH
selected_index = 0      # Absolute index in the entries list
cursor_position = 0     # Position drawn on the screen (0...MAX_VISIBLE-1)
scroll_offset = 0       # Start index of visible portion of the list
volume_percent = 20
volume_lock = threading.Lock()

# Playback State
playback_state = {
    "title": "Unknown Title",
    "artist": "Unknown Artist",
    "progress": 0,
    "total": 180.0,
    "active": False
}

def list_directory(path):
    try:
        entries = os.listdir(path)
        entries.sort()
        return entries
    except Exception:
        return []

def get_metadata(file_path):
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format_tags=title,artist",
            "-of", "default=noprint_wrappers=1:nokey=0",
            file_path
        ]
        result = subprocess.check_output(cmd).decode().strip().split("\n")
        metadata = {}
        for line in result:
            if line.startswith("TAG:"):
                key, value = line[4:].split("=", 1)
                metadata[key.lower()] = value
        return metadata.get("title", "Unknown Title"), metadata.get("artist", "Unknown Artist")
    except Exception:
        return "Unknown Title", "Unknown Artist"

def get_duration(file_path):
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        output = subprocess.check_output(cmd).decode().strip()
        return float(output)
    except Exception:
        return 180.0

def draw_playback_screen():
    while playback_state["active"]:
        progress = playback_state["progress"]
        total = playback_state["total"]

        current_time = time.strftime("%M:%S", time.gmtime(progress))
        total_time = time.strftime("%M:%S", time.gmtime(total))
        time_display = f"{current_time}/{total_time}"

        with volume_lock:
            vol = volume_percent

        with canvas(device) as draw:
            draw.rectangle((0, 0, device.width, 10), fill="white")
            draw.text((0, 0), playback_state["title"][:MAX_CHARACTERS], fill="black", font=font)
            draw.text((0, 15), playback_state["artist"][:MAX_CHARACTERS], fill="white", font=font)
            draw.text((0, 30), time_display, fill="white", font=font)
            draw.text((0, 45), f"Vol: {vol}%", fill="white", font=font)

        if not playback_state["active"]:
            break

        time.sleep(0.05)

def adjust_volume(change):
    global volume_percent
    with volume_lock:
        volume_percent = max(0, min(100, volume_percent + change))

def set_mpv_volume(ipc_socket_path, volume):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(ipc_socket_path)
        cmd = json.dumps({"command": ["set_property", "volume", volume]})
        sock.send((cmd + "\n").encode("utf-8"))
        sock.close()
    except Exception:
        pass

def play_folder_loop(entry_path, stop_button):
    global playback_state

    folder = os.path.dirname(entry_path)
    playlist = sorted([
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith((".mp3", ".wav", ".flac"))
    ])

    try:
        index = playlist.index(entry_path)
    except ValueError:
        return

    playback_state["active"] = True

    while playback_state["active"]:
        current_track = playlist[index]
        title, artist = get_metadata(current_track)
        duration = get_duration(current_track)

        playback_state.update({
            "title": title,
            "artist": artist,
            "progress": 0,
            "total": duration
        })

        # Stop previous playback thread before starting a new one
        playback_state["active"] = False
        time.sleep(0.2)
        playback_state["active"] = True

        draw_thread = threading.Thread(target=draw_playback_screen)
        draw_thread.daemon = True
        draw_thread.start()

        ipc_path = "/tmp/mpvsocket"
        if os.path.exists(ipc_path):
            os.remove(ipc_path)

        with volume_lock:
            vol = volume_percent

        proc = subprocess.Popen([
            "mpv", current_track,
            "--no-video", "--really-quiet",
            f"--input-ipc-server={ipc_path}",
            f"--volume={vol}"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        start = time.time()

        while proc.poll() is None and playback_state["active"]:
            if stop_button.is_pressed:
                playback_state["active"] = False
                proc.terminate()
                break

            if volumeup.is_pressed:
                adjust_volume(5)
                set_mpv_volume(ipc_path, volume_percent)
                time.sleep(0.1)

            elif volumedown.is_pressed:
                adjust_volume(-5)
                set_mpv_volume(ipc_path, volume_percent)
                time.sleep(0.1)

            playback_state["progress"] = int(time.time() - start)
            time.sleep(0.2)

        if proc.poll() is None:
            proc.terminate()

        if not playback_state["active"]:
            break

        index = (index + 1) % len(playlist)

    playback_state["active"] = False

def draw_menu(path, entries, cursor_position, scroll_offset):
    with canvas(device) as draw:
        visible_entries = entries[scroll_offset:scroll_offset + MAX_VISIBLE]
        while len(visible_entries) < MAX_VISIBLE:
            visible_entries.append("")
        for i, entry in enumerate(visible_entries):
            y = i * 10
            text = entry[:MAX_CHARACTERS]
            if len(entry) > MAX_CHARACTERS:
                text += "..."
            if i == cursor_position:
                draw.rectangle((0, y, device.width, y + 10), fill="white")
                draw.text((0, y), text, fill="black", font=font)
            else:
                draw.text((0, y), text, fill="white", font=font)

def main():
    global current_path, selected_index, cursor_position, scroll_offset
    while True:
        entries = list_directory(current_path)
        if not entries:
            # Reset selection if directory is empty
            selected_index = 0
            cursor_position = 0
            scroll_offset = 0

        draw_menu(current_path, entries, cursor_position, scroll_offset)
        time.sleep(0.05)

        if up.is_pressed:
            if selected_index > 0:
                selected_index -= 1
                # If not at top of visible window, just move the cursor up.
                if cursor_position > 0:
                    cursor_position -= 1
                # Otherwise, slide the window upward.
                elif scroll_offset > 0:
                    scroll_offset -= 1
            time.sleep(0.1)

        elif down.is_pressed:
            if selected_index < len(entries) - 1:
                selected_index += 1
                # If cursor is not at the bottom of the screen, move it.
                if cursor_position < MAX_VISIBLE - 1:
                    cursor_position += 1
                # Otherwise, slide the window down.
                elif scroll_offset < len(entries) - MAX_VISIBLE:
                    scroll_offset += 1
            time.sleep(0.1)

        elif back.is_pressed and current_path != BASE_PATH:
            current_path = os.path.dirname(current_path)
            # Reset selection variables when moving to a new directory.
            selected_index = 0
            cursor_position = 0
            scroll_offset = 0
            time.sleep(0.1)

        elif enter.is_pressed:
            if entries:
                entry_path = os.path.join(current_path, entries[selected_index])
                if os.path.isdir(entry_path):
                    current_path = entry_path
                    selected_index = 0
                    cursor_position = 0
                    scroll_offset = 0
                elif entry_path.lower().endswith((".mp3", ".wav", ".flac")):
                    play_folder_loop(entry_path, back)
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting gracefully...")
        playback_state["active"] = False
        device.clear()
        time.sleep(0.2)
