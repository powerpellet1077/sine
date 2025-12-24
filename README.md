# sine
### what is it
a small yt-dlp wrapper, focused primarily on downloading music. this is made primarily for usage within a gui, but a cli tool may become available later

### compiling
```
git clone https://github.com/powerpellet1077/sine.git
cd sine
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed --add-data "sine;sine/" --name "sine" --icon=NONE desktop.py
```