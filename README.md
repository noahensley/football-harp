# Football Harp Installation Guide

## Prerequisites

- Linux operating system
- Git installed
- Sudo privileges

## Installation Steps

### 1. Clone Repository

First, clone the football-harp repository to your local machine.

### 2. Install Dependencies

#### System Packages

Install required system packages using apt-get:

```bash
sudo apt-get install -y python3 fswebcam python3-smbus cmake git gcc g++ make libasound2-dev libudev-dev
```

#### Python Packages

Due to externally managed environment restrictions, choose one of the following options:

**Option 1: Virtual Environment (Recommended)**

```bash
python3 -m venv ~/football-harp-env
source ~/football-harp-env/bin/activate
pip install adafruit-blinka adafruit-circuitpython-bmp280 aprslib
```

**Option 2: System-wide Installation (Not Recommended)**

```bash
pip install --break-system-packages adafruit-blinka adafruit-circuitpython-bmp280 aprslib
```

#### Direwolf Installation

Build and install Direwolf from source:

```bash
cd ~
git clone https://www.github.com/wb2osz/direwolf
cd direwolf
mkdir build && cd build
cmake ..
make -j4
sudo make install
```

Verify the installation:

```bash
which direwolf  # Should output: /usr/local/bin/direwolf
```

Clean up the build directory:

```bash
cd ~
rm -rf direwolf
```

### 3. Configure Services

Service configuration scripts will be provided separately.

## Notes

- An automated installation script is planned for future releases
- If using the virtual environment, remember to activate it before running the application:
  ```bash
  source ~/football-harp-env/bin/activate
  ```