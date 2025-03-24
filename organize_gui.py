import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import re
import json
from difflib import get_close_matches
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QListWidget, QFileDialog, QProgressBar, QTextEdit, QMessageBox, QCheckBox,
    QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sorting Settings")
        self.setGeometry(300, 300, 300, 150)
        layout = QFormLayout()

        self.similarity_cutoff = QSpinBox()
        self.similarity_cutoff.setRange(50, 100)
        self.similarity_cutoff.setValue(int(parent.similarity_cutoff * 100))
        layout.addRow("Similarity Cutoff (%)", self.similarity_cutoff)

        self.naming_pattern = QLineEdit()
        self.naming_pattern.setText(parent.naming_pattern)
        layout.addRow("Naming Regex", self.naming_pattern)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

class FileOrganizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dark File Organizer")
        self.setGeometry(100, 100, 800, 600)
        self.folder_path = None
        self.files = []
        self.undo_log = []
        self.manual_review = True

        # Settings
        self.similarity_cutoff = 0.85
        self.naming_pattern = r"[\s_\-]*(\(\d+\)|\[\d+\]|\d+)$"

        # Dark theme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor("#3c3f41"))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

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

        self.manual_checkbox = QCheckBox("Manual review before organizing")
        self.manual_checkbox.setChecked(True)
        self.manual_checkbox.stateChanged.connect(self.toggle_manual_review)
        layout.addWidget(self.manual_checkbox)

        self.browse_button = QPushButton("Browse Folder")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        self.organize_button = QPushButton("Organize Files")
        self.organize_button.clicked.connect(self.organize_files)
        layout.addWidget(self.organize_button)

        self.undo_button = QPushButton("Undo Last Organization")
        self.undo_button.clicked.connect(self.undo_last)
        layout.addWidget(self.undo_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setAcceptDrops(True)

    def toggle_manual_review(self, state):
        self.manual_review = bool(state)

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

    def extract_common_name(self, filename):
        name = filename.stem
        name = re.sub(self.naming_pattern, "", name)
        return name.strip().lower()

    def organize_files(self):
        if not self.folder_path:
            self.log.append("No folder selected.")
            return

        total = len(self.files)
        self.progress.setMaximum(total)
        self.progress.setValue(0)
        self.undo_log.clear()

        groups = {}

        for file in self.files:
            common = self.extract_common_name(file)
            match = get_close_matches(common, groups.keys(), n=1, cutoff=self.similarity_cutoff)
            key = match[0] if match else common
            groups.setdefault(key, []).append(file)

        for i, (group_name, file_list) in enumerate(groups.items()):
            for file in file_list:
                ext = file.suffix.lstrip('.')
                target_folder = self.folder_path / group_name / ext
                target_folder.mkdir(parents=True, exist_ok=True)
                destination = target_folder / file.name

                if destination.exists():
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    destination = target_folder / f"{file.stem}_{timestamp}{file.suffix}"

                if self.manual_review:
                    reply = QMessageBox.question(self, "Move File", f"Move {file.name} to {destination.relative_to(self.folder_path)}?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply != QMessageBox.StandardButton.Yes:
                        continue

                shutil.move(str(file), str(destination))
                self.undo_log.append((destination, file))
                self.log.append(f"Moved: {file.name} -> {destination.relative_to(self.folder_path)}")
                self.progress.setValue(self.progress.value() + 1)

        self.log.append("\n✅ Done organizing files!")
        self.load_folder(str(self.folder_path))

    def undo_last(self):
        if not self.undo_log:
            self.log.append("Nothing to undo.")
            return

        for dest, original in reversed(self.undo_log):
            shutil.move(str(dest), str(original))
            self.log.append(f"Undone: {dest.name} -> {original.name}")

        self.undo_log.clear()
        self.load_folder(str(self.folder_path))
        self.log.append("\n↩️ Undo complete.")

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            self.similarity_cutoff = dialog.similarity_cutoff.value() / 100.0
            self.naming_pattern = dialog.naming_pattern.text()
            self.log.append(f"Updated settings: similarity cutoff = {self.similarity_cutoff}, regex = {self.naming_pattern}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerGUI()
    window.show()
    sys.exit(app.exec())

