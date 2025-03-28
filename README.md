# 📁 Dark File Organizer GUI

A sleek drag-and-drop file organizer built with **Python + PyQt6**, featuring:

- 🗁️ Drag-and-drop folder support  
- 🗂️ Auto-sorting by **common name** and **file type**  
- 🗽 File **preview before organizing**  
- 📊 Progress bar and logging  
- 🌑 Dark theme UI  
- 🪤 Fuzzy matching to group similar filenames (e.g. `Dog01`, `dog_2`, `Doggo-03`)
- ⚖️ Custom rule editor via settings panel
- 🔄 Undo last organization
- ✅ Manual review and confirmation before sorting
- 🗌 Recursive organization of nested folders

---

## 🔧 How It Works

This tool scans a selected folder and:

1. Recursively finds all files, including those in nested folders.
2. Groups files by a common prefix, ignoring trailing patterns like `(01)`, `[01]`, `_01`, `-01`, and uses **fuzzy matching** to cluster similar names.
3. Creates subfolders based on that prefix.
4. Separates files by type within those folders.
5. Handles duplicate files by **renaming** with a timestamp.
6. Allows **manual review** and **undo** of the last operation.
7. Supports full **customization** of fuzzy similarity and file-naming regex through a **settings panel**.
8. Optionally deletes the old folder structure after organizing.

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
- Recursive file scanning (nested folders included)
- Live preview of files
- Smart grouping using fuzzy match
- Rename duplicate files automatically
- Manual review before confirming sort
- Undo last organization with one click
- Dark theme for comfy vibes
- Live log of actions
- Customizable sorting rules in Settings panel
- Optionally delete old folder tree after sorting

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
- Import/export sorting presets
- Light/dark theme toggle
- Integration with cloud storage
- File tagging system

