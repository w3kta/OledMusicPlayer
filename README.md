# Raspberry Pi FLAC Player Project

---

## 🛠️ Used Hardware

- **Raspberry Pi Zero 2W** (headless mode, Raspberry Pi OS Lite)  
- **HiFiBerry DAC**: PCM5102A  
- **OLED Display**: 1.3" SH1106 (I2C)  
- **7 buttons**

## Wiring:  
**OLED - Raspberry Pi Zero 2W**  

VCC - 3.3V (PIN 1)  
GND - any free GND  
SCL - PIN 5  
SCA - PIN 3  

**DAC - Raspberry Pi Zero 2W**  
VIN - 5V Pin 2  
GND - any free GND  
LCK - PIN 35  
DIN - PIN 39  
BCK - PIN 12 

**Buttons**
up_pin = GPIO 4 (PIN 7)
down_pin = GPIO 17 (PIN 11)
enter_pin = GPIO 27 (PIN 13)
back_pin = GPIO 22 (PIN 15)
volumeup_pin = GPIO 24 (PIN 18)
volumedown_pin = GPIO 23 (PIN 16)

## Install OS by using an SD card and Raspberry Pi Imager and SSH in the system, for this use terminal or putty

## Installation

To install:  
  python3-venv  
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

## Python packages to install

- **luma.oled**  
- **gpiozero**  
- **Pillow**  



Steps after SSH:  
1. Enable I2C in raspi-config and reboot  
2. Edit /boot/firmware/config.txt and copy-paste the uploaded version  
3. Edit /etc/asound.conf and add:  
   defaults.pcm.card 0  
   defaults.ctl.card 0
4. Create and start a venv
5. Create a player.py file and run it
6. Optional in crontab start the venv and py on every boot






