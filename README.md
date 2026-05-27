# 🖥️ Spectra PC Monitor

> A high-performance, real-time hardware monitoring and optimization suite styled with a modern liquid-glass glassmorphism theme and designed natively for Linux / Zorin OS.

---

## ✨ Features

- **📊 Real-Time Telemetry**: Live circular gauges and historical line charts tracking CPU, RAM, and Disk space usage at near 0% execution overhead.
- **⚡ Dual Mode UI Rendering**:
  - **Glassmorphism (ON)**: Sophisticated alpha translucency (`rgba(8, 12, 20, 0.72)`) that lets your beautiful desktop wallpaper bleed through smoothly under the "liquid glass" UI.
  - **Solid Dark (OFF)**: High-contrast solid dark slate theme (`rgb(8, 12, 20)`) for maximum text legibility and ultra-low rendering overhead.
- **🎨 Cyberpunk Themes**: Dynamic real-time color scheme swapping globally across all gauge tracks, historical charts, outlines, and nav buttons:
  - 💎 **Spectra Blue** (Neon Aqua & Violet)
  - 🟢 **Emerald Green** (Vibrant Matrix Green)
  - 🔴 **Cyberpunk Red** (Neon Magenta & Ruby)
  - 🟠 **Neon Amber** (Cyber Gold & Crimson)
- **🚀 Built-in Speedtest**: Non-blocking multithreaded speed testing (Download, Upload, Ping) using a dedicated QThread.
- **🌐 Network Analytics**: Live active network adapter card list with MAC, IP, connectivity state, and dynamic reconstruction.
- **🎛️ Advanced Frameless Interactions**:
  - Global click-and-drag window movement.
  - Generous 10px grab margin enabling full 8-way directional window resizing with native double-arrow cursor states.
- **📦 Native Zorin OS App integration**: Built-in standalone single binary compilation support and a native Gnome `.desktop` launcher with custom emoji branding.

---

## 🛠️ Technology Stack

- **Core Framework**: Python 3 & PyQt6
- **System Telemetry**: `psutil`, `GPUtil`
- **Build Engine**: PyInstaller
- **Operating System**: Linux / Zorin OS / Ubuntu

---

## 🚀 Installation & Developer Setup

### Prerequisite Dependencies
Make sure you have Python 3 and Pip installed. Then install the required developer packages:
```bash
pip install PyQt6 psutil GPUtil pyinstaller
```

### Run in Development Mode
To launch the application from the source code:
```bash
python3 main.py
```

### Build a Standalone Zorin OS Executable
To package the app into a single, fully-independent double-clickable binary file (without black terminal logs behind it):
```bash
pyinstaller --onefile --windowed --name="SpectraMonitor" --add-data "app_icon.png:." --noconfirm --clean main.py
```
The compiled application binary will be built inside the `./dist/` directory as `SpectraMonitor` (size: ~61MB).

---

## 🖥️ Zorin OS Desktop Integration

To register Spectra PC Monitor in your Zorin OS Application Start Menu and add a launch icon on your Desktop:

1. Create a `SpectraMonitor.desktop` shortcut file on your Desktop:
   ```ini
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=Spectra PC Monitor
   Comment=Premium hardware monitoring and tune-up utility
   Exec="/home/YOUR_USERNAME/Desktop/Spectra-PC-Monitor/dist/SpectraMonitor"
   Icon=/home/YOUR_USERNAME/Desktop/Spectra-PC-Monitor/app_icon.png
   Terminal=false
   Categories=System;Monitor;
   StartupNotify=true
   ```
2. Grant executable permissions and mark it as trusted:
   ```bash
   chmod +x ~/Desktop/SpectraMonitor.desktop
   gio set ~/Desktop/SpectraMonitor.desktop metadata::trusted true
   ```
3. Copy the launcher to your application menu library to make it searchable in the Start Menu:
   ```bash
   cp ~/Desktop/SpectraMonitor.desktop ~/.local/share/applications/
   ```

---

## 🎨 Visual Design Choices

The application's interface design follows high-fidelity liquid-glass design rules:
* Curated dark-palette gradients that contrast nicely against white typography and high-contrast neon lines.
* Native vector drawing (`QPainter`) for all circular gauges, speed gauges, and grid charts, enabling completely fluid, vector-perfect real-time updates at 60 FPS.
* Soft shadows (`QGraphicsDropShadowEffect`) to elevate elements, giving the interface three-dimensional depth.

---

## 📄 License
This project is open-source and available under the MIT License.
