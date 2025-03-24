# 📁 Dark File Organizer GUI

A sleek drag-and-drop file organizer built with **Python + PyQt6**, featuring:

- 🗁️ Drag-and-drop folder support  
- 🗂️ Auto-sorting by **common name** and **file type**  
- 🗽 File **preview before organizing**  
- 📊 Progress bar and logging  
- 🌑 Dark theme UI  

---

## 🔧 How It Works

This tool scans a selected folder and:

1. Groups files by a common prefix (e.g., everything starting with `invoice_`).
2. Creates subfolders based on that prefix.
3. Separates files by type within those folders.
4. Handles duplicate files by **renaming** with a timestamp.

### 🧱 Example structure:
```
📁 invoice
 └── 📁 pdf
     ├── invoice_jan.pdf
     └── invoice_feb.pdf
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

