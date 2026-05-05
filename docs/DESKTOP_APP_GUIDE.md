# ETL Parser - Desktop Application Guide

Transform the ETL Parser into a **native desktop application** that users can install and run like any other desktop software!

---

## 🖥️ What is the Desktop Version?

The desktop version is a **standalone application** that:
- ✅ Runs like a native desktop app (no browser needed)
- ✅ Can be installed with a simple double-click
- ✅ Works offline (except AI features)
- ✅ No Python or technical knowledge required for users
- ✅ Cross-platform (Windows, macOS, Linux)

---

## 🚀 Quick Start (For Developers)

### Step 1: Install Desktop Requirements

```bash
# Install desktop dependencies
pip install -r desktop_requirements.txt
```

**Platform-Specific Requirements:**

**Windows:**
```bash
pip install pywebview[cef]  # For better rendering
```

**macOS:**
```bash
pip install pyobjc  # Usually auto-installed
```

**Linux:**
```bash
# Install system dependencies first
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# Or use Qt backend
pip install PyQt5
```

### Step 2: Run as Desktop App (Development Mode)

```bash
python desktop_app.py
```

This opens ETL Parser in a native desktop window! 🎉

### Step 3: Build Standalone Executable (For Distribution)

```bash
python build_desktop_app.py
```

This creates a **distributable application** in the `dist/` folder.

---

## 📦 Distribution Methods

### Method 1: Standalone Executable (Recommended)

**Build:**
```bash
python build_desktop_app.py
```

**Result:**
- Windows: `dist/ETL_Parser/ETL_Parser.exe`
- macOS: `dist/ETL_Parser.app`
- Linux: `dist/ETL_Parser/ETL_Parser`

**Share with Users:**
1. Zip the entire `dist/ETL_Parser` folder
2. Share the zip file
3. Users extract and double-click the executable
4. Done! No installation needed.

**File Size:** ~50-100 MB (includes Python runtime)

---

### Method 2: Installer Packages

#### Windows Installer (.msi)

```bash
# Install Inno Setup from: https://jrsoftware.org/isdl.php
# Create installer script

pip install pyinstaller
python build_desktop_app.py

# Then create installer with Inno Setup
```

**Inno Setup Script (installer.iss):**
```ini
[Setup]
AppName=ETL Parser
AppVersion=1.0
DefaultDirName={pf}\ETL Parser
DefaultGroupName=ETL Parser
OutputDir=installers
OutputBaseFilename=ETL_Parser_Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\ETL_Parser\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\ETL Parser"; Filename: "{app}\ETL_Parser.exe"
Name: "{commondesktop}\ETL Parser"; Filename: "{app}\ETL_Parser.exe"
```

#### macOS Installer (.dmg)

```bash
# After building with PyInstaller
pip install dmgbuild

# Create dmg
dmgbuild -s dmg_settings.py "ETL Parser" dist/ETL_Parser.dmg
```

#### Linux Package (.deb / .rpm)

```bash
# For Debian/Ubuntu
pip install stdeb
python setup.py --command-packages=stdeb.command bdist_deb

# For RedHat/Fedora
pip install pyinstaller
python build_desktop_app.py
alien dist/*.deb  # Convert .deb to .rpm
```

---

### Method 3: PyWebView Runner (Lightest)

For users who already have Python:

**Create launcher script:**

```python
# run_desktop.py
import subprocess
import sys

# Install requirements if needed
subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'desktop_requirements.txt'])

# Run desktop app
subprocess.run([sys.executable, 'desktop_app.py'])
```

**Share:**
1. Zip the entire project folder
2. Users extract and run: `python run_desktop.py`

---

## 🎨 Customization Options

### Change Window Settings

Edit `desktop_app.py`:

```python
window = webview.create_window(
    title='Your Company - ETL Parser',  # Custom title
    url=url,
    width=1600,                          # Custom width
    height=1000,                         # Custom height
    resizable=True,                      # Allow resizing
    fullscreen=False,                    # Start fullscreen?
    min_size=(1200, 800),               # Minimum size
    background_color='#2d2d2d',         # Background color
    text_select=True                     # Allow text selection
)
```

### Add Custom Icon

**Windows (.ico):**
```bash
# Place icon at: static/icon.ico
# PyInstaller will automatically use it
```

**macOS (.icns):**
```bash
# Place icon at: static/icon.icns
# Convert PNG to ICNS: https://cloudconvert.com/png-to-icns
```

**Linux (.png):**
```bash
# Place icon at: static/icon.png
```

### Add System Tray Icon

Edit `desktop_app.py`:

```python
import pystray
from PIL import Image

def create_tray_icon():
    icon = pystray.Icon('ETL Parser')
    icon.icon = Image.open('static/icon.png')
    icon.title = 'ETL Parser'
    
    menu = pystray.Menu(
        pystray.MenuItem('Open', lambda: webview.windows[0].show()),
        pystray.MenuItem('Exit', lambda: webview.windows[0].destroy())
    )
    icon.menu = menu
    icon.run()
```

---

## 🔧 Advanced Build Options

### Reduce Executable Size

Edit `build_desktop_app.py` to exclude more packages:

```python
excludes=[
    'matplotlib', 'numpy', 'scipy', 'PIL', 'tkinter',
    'setuptools', 'distutils', 'email', 'xml', 'unittest',
    'pydoc', 'doctest', 'test', 'tests'
]
```

### Add Splash Screen

```python
# In desktop_app.py, before creating window:
splash = webview.create_window(
    'Loading ETL Parser...',
    html='<h1 style="text-align:center; padding:50px;">Loading...</h1>',
    width=400,
    height=200,
    frameless=True
)

# Start loading
webview.start()

# After Flask starts, close splash
splash.destroy()
```

### Enable Auto-Update

Use **PyUpdater** for automatic updates:

```bash
pip install pyupdater

# Initialize
pyupdater init

# Configure settings
pyupdater settings --app-name "ETL Parser" --company "YourCompany"

# Build with updates
pyupdater build --app-version 1.0.0 desktop_app.py
```

---

## 📤 Sharing the Desktop App

### For End Users (Non-Technical)

**Option 1: Direct Download**
1. Upload `dist/ETL_Parser.zip` to your website/cloud storage
2. Share download link
3. Users download, extract, and run

**Instructions for users:**
```
1. Download ETL_Parser.zip
2. Extract the zip file
3. Double-click ETL_Parser.exe (Windows) or ETL_Parser.app (macOS)
4. That's it! The app will open.
```

**Option 2: Installer**
1. Create installer using Inno Setup (Windows) or dmgbuild (macOS)
2. Share the installer file
3. Users run installer and follow wizard

**Instructions for users:**
```
1. Download ETL_Parser_Setup.exe
2. Double-click to install
3. Follow installation wizard
4. Launch from Start Menu or Desktop shortcut
```

### For IT Departments

**Deployment Options:**
1. **MSI Installer** for Windows Group Policy
2. **DMG** for macOS enterprise deployment
3. **Silent Install** for automated deployment:
   ```bash
   ETL_Parser_Setup.exe /SILENT /SUPPRESSMSGBOXES
   ```

---

## 🐛 Troubleshooting

### Windows: "Windows protected your PC" warning

**Solution:** Code sign your executable
```bash
# Get a code signing certificate
# Sign with signtool.exe
signtool sign /f certificate.pfx /p password ETL_Parser.exe
```

Or tell users: Click "More info" → "Run anyway"

### macOS: "App is damaged and can't be opened"

**Solution:** Remove quarantine attribute
```bash
xattr -cr ETL_Parser.app
```

Or code sign with Apple Developer certificate.

### Linux: "Permission denied"

**Solution:** Make executable
```bash
chmod +x ETL_Parser
```

### App Opens but Shows Blank Window

**Check:**
1. Flask server is starting correctly
2. Increase wait time in `desktop_app.py`:
   ```python
   time.sleep(5)  # Increase from 2 to 5 seconds
   ```
3. Check firewall settings

### "No module named 'flask'" error

**Solution:** PyInstaller didn't bundle Flask properly
```bash
# Rebuild with hidden imports
pyinstaller --hidden-import=flask --hidden-import=werkzeug desktop_app.py
```

---

## 📊 Comparison: Web vs Desktop

| Feature | Web App | Desktop App |
|---------|---------|-------------|
| **Installation** | `pip install` + `python app.py` | Double-click executable |
| **User Experience** | Browser window | Native desktop window |
| **File Size** | ~5 MB | ~80 MB (includes Python) |
| **Offline Work** | ❌ Needs server | ✅ Fully offline |
| **Updates** | `git pull` | New executable |
| **Platform** | Any with Python | Windows/Mac/Linux specific build |
| **For End Users** | Requires Python knowledge | Zero technical knowledge |

---

## 🎯 Best Practices

### For Distribution:
1. ✅ Code sign executables (Windows/macOS)
2. ✅ Include README in the dist folder
3. ✅ Test on clean virtual machines
4. ✅ Provide uninstall instructions
5. ✅ Include example CSV files

### For Updates:
1. ✅ Version number in window title
2. ✅ Check for updates feature
3. ✅ Changelog file
4. ✅ Backward compatibility for user files

### For Security:
1. ✅ Don't bundle `.env` with API keys
2. ✅ Let users configure their own API keys
3. ✅ Validate all file uploads
4. ✅ Use HTTPS for update checks

---

## 📚 Additional Resources

**PyWebView Documentation:**
https://pywebview.flowrl.com/

**PyInstaller Manual:**
https://pyinstaller.org/en/stable/

**Platform-Specific Packaging:**
- Windows: https://jrsoftware.org/isinfo.php (Inno Setup)
- macOS: https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/SoftwareDistribution/
- Linux: https://www.debian.org/doc/manuals/maint-guide/

---

## 🚀 Quick Reference

**Run Desktop Mode:**
```bash
python desktop_app.py
```

**Build Executable:**
```bash
python build_desktop_app.py
```

**Test Executable:**
```bash
# Windows
dist\ETL_Parser\ETL_Parser.exe

# macOS
open dist/ETL_Parser.app

# Linux
./dist/ETL_Parser/ETL_Parser
```

**Create Installer:**
```bash
# Windows: Use Inno Setup
# macOS: Use dmgbuild
# Linux: Use alien or fpm
```

---

## 💡 Tips for Success

1. **Test thoroughly** on clean systems (VMs)
2. **Keep executables under 100 MB** for easy sharing
3. **Provide clear instructions** for non-technical users
4. **Include example files** in the distribution
5. **Version your releases** (e.g., ETL_Parser_v1.0.zip)
6. **Create video tutorials** for end users
7. **Set up update mechanism** for long-term maintenance

---

**Ready to distribute your desktop app!** 🎉

Follow the steps above to create professional, installable desktop applications that anyone can use.
