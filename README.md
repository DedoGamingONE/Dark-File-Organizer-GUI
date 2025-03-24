# 📁 Dark File Organizer GUI

A sleek drag-and-drop file organizer built with **Python + PyQt6**, featuring:

- 🗁️ Drag-and-drop folder support  
- 🗂️ Auto-sorting by **common name** and **file type**  
- 🗽 File **preview before organizing**  
- 📊 Progress bar and logging  
- 🌑 Dark theme UI  
- 🪤 Fuzzy matching to group similar filenames (e.g. `Dog01`, `dog_2`, `Doggo-03`)

---

## 🔧 How It Works

This tool scans a selected folder and:

1. Groups files by a common prefix, ignoring trailing patterns like `(01)`, `[01]`, `_01`, `-01`, and uses **fuzzy matching** to cluster similar names.
2. Creates subfolders based on that prefix.
3. Separates files by type within those folders.
4. Handles duplicate files by **renaming** with a timestamp.

### 🧱 Example structure:
```
📁 dog
 └── 📁 jpg
     ├── Dog01.jpg
     ├── dog_2.jpg
     └── Doggo-03.jpg
```

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.8+
- PyQt6

### 🧪 Installation

```bash
pip install PyQt6
```

### ▶️ Run the App

```bash
python organizer_gui.py
```

---

## 🛠 Features

- Drag-and-drop folder support
- Manual folder selection
- Live preview of files
- Smart grouping using fuzzy match
- Rename duplicate files automatically
- Dark theme for comfy vibes
- Live log of actions

---

## 📆 Optional: Build into an EXE

Use [PyInstaller](https://pyinstaller.org/) to make it portable:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile organizer_gui.py
```

---

## 💡 Future Ideas

- Thumbnail preview for images
- Scheduling and automation
- Sorting rules customization
- Light/dark theme toggle
- Undo organization actions
- Manual review before finalizing moves

