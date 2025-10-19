## Mobile as Mouse for Laptop

Control your Windows laptop mouse from your phone via a simple FastAPI + WebSocket app.

### Features
- Single-finger move, tap to left-click
- Two-finger tap for right-click
- Runs as a standalone `mouse.exe` after packaging

### Quick Start (no install)
- Download `mouse.exe` from the `dist` folder in this repository and run it.
- If you only want to use the app, you do NOT need to download any other files.

### Prerequisites (for source users)
- Windows 10+
- Python 3.11 (if running from source)

### Run (from source)
```bash
python main.py
```
Then open your phone browser to: `http://<PC-IP>:5000/`

### Build (PyInstaller) — optional
```bash
pyinstaller main.spec
```
Output binary: `dist/mouse.exe`

### Notes
- Ensure PC and phone are on the same network.
- Windows Firewall: allow the app to accept inbound connections on port 5000.
- Some environments may require running as Administrator for system input control.


