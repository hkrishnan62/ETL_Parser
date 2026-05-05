# 🖥️ ETL Parser Desktop App - Quick Start

Convert your ETL Parser into a **desktop application** that runs like any native software!

---

## For Users (Just Want to Use It)

### Windows:
1. Double-click `install_desktop.bat`
2. Wait for installation
3. Desktop app opens automatically!

### macOS / Linux:
1. Open terminal in this folder
2. Run: `./install_desktop.sh`
3. Desktop app opens automatically!

**That's it!** No browser needed, runs like a normal desktop app.

---

## For Developers (Want to Build & Distribute)

### 1. Install Desktop Dependencies

```bash
pip install -r desktop_requirements.txt
```

### 2. Run in Desktop Mode (Testing)

```bash
python desktop_app.py
```

### 3. Build Standalone Executable (For Distribution)

```bash
python build_desktop_app.py
```

**Output:**
- Windows: `dist/ETL_Parser/ETL_Parser.exe` (80-100 MB)
- macOS: `dist/ETL_Parser.app`
- Linux: `dist/ETL_Parser/ETL_Parser`

### 4. Share with Others

**Method A: Zip and Share**
```bash
# Zip the dist folder
cd dist
zip -r ETL_Parser.zip ETL_Parser/

# Share ETL_Parser.zip
# Users extract and double-click the executable
```

**Method B: Create Installer**
- **Windows:** Use [Inno Setup](https://jrsoftware.org/isdl.php)
- **macOS:** Use `dmgbuild`
- **Linux:** Create `.deb` or `.rpm` package

---

## What Changes?

### Before (Web App):
```bash
python app.py
# Opens in browser at http://localhost:5000
```

### After (Desktop App):
```bash
python desktop_app.py
# Opens in native desktop window
```

Or just double-click the executable!

---

## Features of Desktop Version

✅ **Native Desktop Window** - Feels like a real desktop app
✅ **No Browser Required** - Runs independently
✅ **Offline Operation** - Works without internet (except AI features)
✅ **Easy Distribution** - Single executable file
✅ **Cross-Platform** - Windows, macOS, Linux
✅ **Professional Look** - Custom window title, icon, size
✅ **Simple for Users** - No Python knowledge needed

---

## File Structure After Building

```
dist/
└── ETL_Parser/
    ├── ETL_Parser.exe (Windows) / ETL_Parser (Linux) / ETL_Parser.app (macOS)
    ├── templates/          # Web interface files
    ├── static/             # CSS, JS, images
    ├── examples/           # Example CSV files
    ├── _internal/          # Python runtime & dependencies
    └── README.txt          # User instructions
```

**Total Size:** ~80-100 MB (includes Python runtime)

---

## Distribution Checklist

- [ ] Test on clean Windows/Mac/Linux VM
- [ ] Include example CSV files in `examples/`
- [ ] Add `.env.example` for AI features
- [ ] Create user documentation (README.txt in dist/)
- [ ] Test without Python installed
- [ ] Verify all features work (upload, AI, export)
- [ ] Create installer (optional)
- [ ] Code sign executable (recommended)
- [ ] Zip the dist folder
- [ ] Upload to distribution platform

---

## Troubleshooting

### Windows: "Windows protected your PC"
**Solution:** Click "More info" → "Run anyway"
(Or code sign your executable)

### macOS: "App can't be opened"
**Solution:** Right-click → Open
(Or code sign with Apple Developer certificate)

### Linux: Permission denied
**Solution:** `chmod +x ETL_Parser`

### Blank Window
**Solution:** Check firewall, increase wait time in `desktop_app.py`

---

## Customization

### Change Window Size
Edit `desktop_app.py`:
```python
window = webview.create_window(
    width=1600,  # Your width
    height=1000, # Your height
    ...
)
```

### Add Custom Icon
1. Place `icon.ico` in `static/` folder
2. Rebuild with `build_desktop_app.py`

### Change App Name
Edit `desktop_app.py`:
```python
title='Your Company - ETL Parser'
```

---

## Need Help?

📖 **Full Guide:** See [DESKTOP_APP_GUIDE.md](DESKTOP_APP_GUIDE.md)

📝 **Documentation:**
- PyWebView: https://pywebview.flowrl.com/
- PyInstaller: https://pyinstaller.org/

🐛 **Issues:** Open an issue on GitHub

---

## Quick Commands Reference

```bash
# Run desktop mode
python desktop_app.py

# Build executable
python build_desktop_app.py

# Install dependencies
pip install -r desktop_requirements.txt

# Test executable (Windows)
dist\ETL_Parser\ETL_Parser.exe

# Test executable (Linux/Mac)
./dist/ETL_Parser/ETL_Parser
```

---

**Ready to go!** Your web app is now a desktop app! 🎉
