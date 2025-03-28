from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from log_tree_view import LogTreeView
from log_content_view import LogContentView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Log Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.log_tree_view = LogTreeView()
        self.log_content_view = LogContentView()

        self.layout.addWidget(self.log_tree_view)
        self.layout.addWidget(self.log_content_view)

        self.log_tree_view.file_selected.connect(self.log_content_view.display_log_content)