#!/bin/bash
# Build script for creating cross-platform installers

echo "Building Assignment Tracker for multiple platforms..."

# Clean previous builds
rm -rf build/ dist/

echo "Building for Linux (current platform)..."
pyinstaller main.spec --clean --noconfirm

echo "Attempting Windows build (may not work on Linux)..."
pyinstaller main-windows.spec --clean --noconfirm --target-platform win32

echo "Attempting macOS build (may not work on Linux)..."
pyinstaller main-macos.spec --clean --noconfirm --target-platform darwin

echo "Build complete. Check dist/ folder for results."
echo "Note: Cross-platform builds from Linux may not work properly."
echo "For best results, build on native platforms."
