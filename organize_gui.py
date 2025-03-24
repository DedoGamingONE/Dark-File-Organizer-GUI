import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QListWidget, QFileDialog, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class FileOrganizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dark File Organizer")
        self.setGeometry(100, 100, 800, 600)
        self.folder_path = None
        self.files = []

        # Dark theme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor("#3c3f41"))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

        # Layouts and widgets
        layout = QVBoxLayout()

        self.label = QLabel("Drag and drop a folder or click 'Browse Folder'")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.browse_button = QPushButton("Browse Folder")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        self.organize_button = QPushButton("Organize Files")
        self.organize_button.clicked.connect(self.organize_files)
        layout.addWidget(self.organize_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            folder = url.toLocalFile()
            if os.path.isdir(folder):
                self.load_folder(folder)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.load_folder(folder)

    def load_folder(self, folder):
        self.folder_path = Path(folder)
        self.label.setText(f"Selected Folder: {self.folder_path}")
        self.list_widget.clear()
        self.files = [f for f in self.folder_path.iterdir() if f.is_file()]

        for file in self.files:
            self.list_widget.addItem(file.name)

    def organize_files(self):
        if not self.folder_path:
            self.log.append("No folder selected.")
            return

        total = len(self.files)
        self.progress.setMaximum(total)
        self.progress.setValue(0)

        for i, file in enumerate(self.files):
            if file.name.count("_") > 0:
                base = file.name.split("_")[0]
            elif file.name.count("-") > 0:
                base = file.name.split("-")[0]
            else:
                base = file.stem

            ext = file.suffix.lstrip('.')
            base_folder = self.folder_path / base / ext
            base_folder.mkdir(parents=True, exist_ok=True)
            dest = base_folder / file.name

            if dest.exists():
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                dest = base_folder / f"{file.stem}_{timestamp}{file.suffix}"
                self.log.append(f"Renamed: {file.name} -> {dest.name}")

            shutil.move(str(file), str(dest))
            self.log.append(f"Moved: {file.name} -> {dest.relative_to(self.folder_path)}")
            self.progress.setValue(i + 1)

        self.log.append("\n✅ Done organizing files!")
        self.load_folder(str(self.folder_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerGUI()
    window.show()
    sys.exit(app.exec())
