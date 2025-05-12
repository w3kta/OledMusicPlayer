# Raspberry Pi FLAC Player Project

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

- **luma.oled**
- **gpiozero**
- **Pillow**


