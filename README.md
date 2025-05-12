# Raspberry Pi FLAC Player Project

A minimalist headless FLAC player built on a Raspberry Pi Zero 2W, using GPIO buttons and an SH1106 OLED display. Audio output is handled by a HiFiBerry DAC (PCM5102A), and playback is managed with MPV.

---

## 🛠️ Used Hardware

- **Raspberry Pi Zero 2W** (headless mode, Raspberry Pi OS Lite)
- **HiFiBerry DAC**: PCM5102A
- **OLED Display**: 1.3" SH1106 (I2C)

1. Install OS by using an SD card and Raspberry Pi Imager
2. SSH from terminal and create a VENV for python

## Installation

sudo apt update && sudo apt install -y \
  python3-pip \
  python3-dev \
  libjpeg-dev \
  libfreetype6-dev \
  libtiff5-dev \
  libopenjp2-7 \
  libatlas-base-dev \
  i2c-tools \
  ffmpeg \
  mpv \
  fonts-dejavu-core


## Python packages
luma.oled
gpiozero
Pillow


