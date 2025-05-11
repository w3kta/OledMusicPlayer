Used gadgets:
1. Raspberry Pi Zero 2W in headless mode with lite os installed
2. Hifiberry DAC: PCM5102A
3. Oled Display 1.3 inch: SH1106

1. Install OS by using an SD card and Raspberry Pi Imager
2. SSH from terminal and create a VENV for python

To install:
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


Pip install:
luma.oled
gpiozero
Pillow


