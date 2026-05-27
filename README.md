# 🖥️ Spectra PC Monitor

> A high-performance, real-time hardware monitoring, system optimization, and network analytics suite styled with an ultra-premium solid **Deep Space Dark Mode** theme and designed natively for Linux / Zorin OS.

---

## ✨ Features

- **📊 Real-Time Telemetry**: Live circular gauges and historical line charts tracking CPU, RAM, and Disk space usage at near 0% execution overhead.
- **🎨 Deep Space Themes**: Four distinct, custom-curated solid dark color profiles that glow beautifully against the space-black interface:
  - 💎 **Spectra Blue** (Neon Aqua & Violet)
  - 🟢 **Emerald Green** (Vibrant Matrix Green)
  - 🔴 **Cyberpunk Red** (Neon Magenta & Ruby)
  - 🟠 **Neon Amber** (Cyber Gold & Crimson)
- **⚡ Performance-First rendering**: Uses a hardware-accelerated, high-contrast solid slate canvas (`#04060a` and `#080c14`) to eliminate window manager composite latency, rendering text with maximum legibility.
- **🚀 Built-in Speedtest**: Non-blocking multithreaded speed testing (Download, Upload, Ping) using a dedicated QThread.
- **🌐 Network Analytics**: Live active network adapter card list with MAC, IP, connectivity state, and dynamic reconstruction.
- **🧹 Active Tune-Up Panel**: Dedicated cleanup panel for recursive temp file purging and recycling bin management with real-time status reporting.
- **🎛️ Advanced Frameless Interactions**:
  - Global click-and-drag window movement.
  - Generous 10px grab margin enabling full 8-way directional window resizing with native double-arrow cursor states.
- **📦 Native Zorin OS App Integration**: Built-in standalone single binary compilation support and a native Gnome `.desktop` launcher with custom emoji branding.

---

## 📂 Project Architecture (Hybrid Modular)

The codebase is organized into a clean, modern, and high-performance developer layout:

```
pc info/
│
├── main.py                   # Primary Application & UI Class Shell (~2800 lines)
├── requirements.txt          # Python dependencies
├── app_icon.png              # Vector graphic app icon
├── power_history.db          # Setting & history persistence SQLite database (Git Ignored)
│
├── core/                     # Logic & System Telemetry
│   ├── __init__.py           # Declares core as Python package
│   ├── constants.py          # Global QSS Stylesheets & asset resolvers
│   ├── telemetry.py          # Advanced hardware probes (CPU, GPU, OS, Power draw)
│   └── workers.py            # Multithreaded background workers (SpeedTest, DiskBench, TuneUp)
│
└── ui/                       # Helper Presentation & Desklets
    ├── __init__.py           # Declares ui as Python package
    ├── custom_widgets.py     # Custom vector gauges (CircularGauge, SpeedGauge, RealTimeGraph)
    └── desktop_widget.py     # Floating capsule SpectraDesktopWidget desklet
```

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
   Exec="/home/YOUR_USERNAME/Desktop/pc info/dist/SpectraMonitor"
   Icon=/home/YOUR_USERNAME/Desktop/pc info/app_icon.png
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

The application's interface design follows high-fidelity liquid-glass design rules adapted for solid dark modes:
* Curated dark-palette gradients that contrast nicely against white typography and high-contrast neon lines.
* Native vector drawing (`QPainter`) for all circular gauges, speed gauges, and grid charts, enabling completely fluid, vector-perfect real-time updates at 60 FPS.
* Soft shadows (`QGraphicsDropShadowEffect`) to elevate elements, giving the interface three-dimensional depth.

---

## 📄 License
This project is open-source and available under the MIT License.
