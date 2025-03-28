from PyQt5.QtWidgets import QTextEdit
import os

class LogContentViewer(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        
    def load_file(self, file_path):
        """Load and display contents of a log file"""
        try:
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.setText(content)
                self.setWindowTitle(os.path.basename(file_path))
            else:
                self.setText("")
        except Exception as e:
            self.setText(f"Error loading file: {str(e)}")