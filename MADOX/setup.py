import os
import urllib.request
import zipfile
import subprocess

# URL to official wget for Windows (EzWinPorts version)
WGET_URL = "https://eternallybored.org/misc/wget/1.21.4/64/wget.exe"
INSTALL_DIR = r"C:\Tools\wget"

# Ensure install directory exists
os.makedirs(INSTALL_DIR, exist_ok=True)

# Download wget.exe
wget_path = os.path.join(INSTALL_DIR, "wget.exe")
print(f"Downloading wget to {wget_path}...")
urllib.request.urlretrieve(WGET_URL, wget_path)

# Add INSTALL_DIR to PATH permanently
print("Adding to PATH...")
subprocess.run(f'setx PATH "%PATH%;{INSTALL_DIR}"', shell=True)

print("Done! You can now run wget from the command line.")
