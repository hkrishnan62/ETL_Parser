#!/usr/bin/env python3
"""
Build script for creating standalone desktop executables.
Run this script to create a distributable desktop application.
"""

import os
import sys
import platform
import subprocess
import shutil

def get_platform_name():
    """Get the current platform name."""
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Darwin':
        return 'macos'
    elif system == 'Linux':
        return 'linux'
    else:
        return 'unknown'

def create_spec_file():
    """Create PyInstaller spec file for customized build."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('examples', 'examples'),
        ('.env.example', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'flask',
        'pandas',
        'openai',
        'langchain',
        'langchain_openai',
        'dotenv',
        'werkzeug',
        'jinja2',
        'click',
        'itsdangerous',
        'markupsafe',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy', 'PIL', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ETL_Parser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for Windows GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/icon.ico' if os.path.exists('static/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ETL_Parser',
)

# For macOS, create an app bundle
import platform
if platform.system() == 'Darwin':
    app = BUNDLE(
        coll,
        name='ETL_Parser.app',
        icon='static/icon.icns' if os.path.exists('static/icon.icns') else None,
        bundle_identifier='com.etlparser.app',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
        },
    )
'''
    
    with open('ETL_Parser.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller."""
    platform_name = get_platform_name()
    print(f"\n🏗️  Building desktop application for {platform_name}...")
    
    # Create spec file
    create_spec_file()
    
    # Run PyInstaller
    print("\n📦 Running PyInstaller...")
    try:
        subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            'ETL_Parser.spec',
            '--clean',
            '--noconfirm'
        ], check=True)
        
        print("\n✅ Build completed successfully!")
        print(f"\n📂 Executable location:")
        
        if platform_name == 'windows':
            print(f"   dist/ETL_Parser/ETL_Parser.exe")
        elif platform_name == 'macos':
            print(f"   dist/ETL_Parser.app")
        else:
            print(f"   dist/ETL_Parser/ETL_Parser")
        
        print("\n📝 To distribute:")
        print(f"   1. Zip the 'dist/ETL_Parser' folder")
        print(f"   2. Share the zip file with users")
        print(f"   3. Users extract and run the executable")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def check_requirements():
    """Check if all required packages are installed."""
    print("🔍 Checking requirements...")
    
    required_packages = ['pywebview', 'pyinstaller', 'flask', 'pandas']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"\nInstall them with:")
        print(f"   pip install -r desktop_requirements.txt")
        return False
    
    print("✓ All requirements installed")
    return True

def main():
    """Main build process."""
    print("=" * 70)
    print("   ETL Parser - Desktop Application Builder")
    print("=" * 70)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Build executable
    if build_executable():
        print("\n" + "=" * 70)
        print("   🎉 Desktop application built successfully!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("   ❌ Build failed. Please check errors above.")
        print("=" * 70)
        sys.exit(1)

if __name__ == '__main__':
    main()
