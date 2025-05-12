# Raspberry Pi FLAC Player Project

---

## 🛠️ Used Hardware

- **Raspberry Pi Zero 2W** (headless mode, Raspberry Pi OS Lite)
- **HiFiBerry DAC**: PCM5102A
- **OLED Display**: 1.3" SH1106 (I2C)
- **7 buttons**

1. Install OS by using an SD card and Raspberry Pi Imager
2. SSH from terminal and create a VENV for python

## Installation

To install:
  ython3-venv
  python3-pip
  python3-dev
  python3-smbus i2c-tools
  python3-pil
  python3-setuptools
  libjpeg-dev
  libfreetype6-dev
  libtiff5-dev
  libopenjp2-7
  libatlas-base-dev
  i2c-tools
  ffmpeg
  mpv
  fonts-dejavu-core


## Python packages

- **luma.oled**
- **gpiozero**
- **Pillow**


Steps after SSH:
1. Enable I2C in raspi-config and reboot
2. Edit /boot/firmware/config.txt and copy paste the uploaded version
3. Edit /etc/asound.conf and add:
   defaults.pcm.card 0
   defaults.ctl.card 0
