from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import QDir, pyqtSignal

class LogTreeView(QTreeView):
    file_selected = pyqtSignal(str)  # Signal to emit when a file is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create file system model
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        
        # Set the model for this view
        self.setModel(self.model)
        
        # Hide unnecessary columns
        for column in range(1, 4):  # Hide Size, Type, Date Modified columns
            self.hideColumn(column)
        
        # Other customizations
        self.setAnimated(True)
        self.setSortingEnabled(True)
        
        # Connect selection signal
        self.clicked.connect(self._on_item_clicked)
    
    def set_root_directory(self, directory_path):
        """Set the root directory for the tree view"""
        index = self.model.setRootPath(directory_path)
        self.setRootIndex(index)
    
    def _on_item_clicked(self, index):
        """Handle tree item click"""
        # Get the file path of the clicked item
        file_path = self.model.filePath(index)
        
        # Check if it's a file (not a directory)
        if not self.model.isDir(index):
            self.file_selected.emit(file_path)