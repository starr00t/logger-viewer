from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QSplitter, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
# Add this import for Find flags
from PyQt5.QtGui import QTextDocument
import sys
import os
import configparser

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import using relative imports instead of absolute imports
from ui.log_tree_view import LogTreeView
from ui.log_content_view import LogContentViewer

# Configuration file path
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".log_viewer_config.ini")

def save_config(root_dir):
    """Save configuration to file"""
    config = configparser.ConfigParser()
    config['Settings'] = {'RootDirectory': root_dir}
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_config():
    """Load configuration from file"""
    if not os.path.exists(CONFIG_FILE):
        return None
        
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    try:
        return config['Settings']['RootDirectory']
    except (KeyError, configparser.NoSectionError):
        return None

def main():
    app = QApplication(sys.argv)
    
    # Set dark theme style sheet with light blue text
    dark_stylesheet = """
    QWidget {
        background-color: #1E1E1E;
        color: #7FDBFF;
    }
    
    QTreeView {
        background-color: #252526;
        color: #7FDBFF;
        border: 1px solid #3F3F46;
    }
    
    QTreeView::item:selected {
        background-color: #3F3F70;
    }
    
    QTextEdit {
        background-color: #1A1A1A;
        color: #7FDBFF;
        border: 1px solid #3F3F46;
        font-family: monospace;
    }
    
    QPushButton {
        background-color: #0E639C;
        color: #FFFFFF;
        border: 1px solid #0E639C;
        border-radius: 2px;
        padding: 5px 10px;
    }
    
    QPushButton:hover {
        background-color: #1177BB;
    }
    
    QPushButton:pressed {
        background-color: #0D5C8F;
    }
    
    QSplitter::handle {
        background-color: #3F3F46;
    }
    
    QHeaderView::section {
        background-color: #2D2D30;
        color: #7FDBFF;
        border: 1px solid #3F3F46;
    }
    
    QScrollBar {
        background-color: #2D2D30;
    }
    
    QScrollBar::handle {
        background-color: #3F3F46;
    }
    QLineEdit {
        background-color: #1A1A1A;
        color: #7FDBFF;
        border: 1px solid #3F3F46;
        border-radius: 2px;
        padding: 3px;
    }
    
    QLabel {
        color: #7FDBFF;
    }
    """
    
    app.setStyleSheet(dark_stylesheet)
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Log Viewer")
    main_window.setGeometry(100, 100, 1000, 700)
    
    # Create central widget
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    
    # Create layout for the main window
    main_layout = QHBoxLayout(central_widget)
    
    # Create a splitter to divide the window
    splitter = QSplitter()
    main_layout.addWidget(splitter)
    
    # Create a container for tree view and button
    tree_container = QWidget()
    tree_layout = QVBoxLayout(tree_container)
    
    # Create button to change root directory
    change_dir_button = QPushButton("Change Root Directory")
    tree_layout.addWidget(change_dir_button)
    
    # Create and add the log tree view 
    log_tree = LogTreeView()
    tree_layout.addWidget(log_tree)
    
    # Add tree container to splitter
    splitter.addWidget(tree_container)
    
    # Create and add the log content viewer to the splitter
    content_container = QWidget()
    content_layout = QVBoxLayout(content_container)
    
    # Create search bar
    search_container = QWidget()
    search_layout = QHBoxLayout(search_container)
    search_layout.setContentsMargins(0, 0, 0, 5)
    
    search_label = QLabel("Find:")
    search_edit = QLineEdit()
    search_edit.setPlaceholderText("Enter text to search...")
    search_edit.setClearButtonEnabled(True)
    
    next_button = QPushButton("Next")
    prev_button = QPushButton("Previous")
    
    search_layout.addWidget(search_label)
    search_layout.addWidget(search_edit, 1)  # Give the search box more space
    search_layout.addWidget(prev_button)
    search_layout.addWidget(next_button)
    
    content_layout.addWidget(search_container)
    
    # Add log content viewer
    log_content = LogContentViewer()
    content_layout.addWidget(log_content)
    
    # Add content container to splitter
    splitter.addWidget(content_container)
    
    # Set initial splitter sizes (30% for tree, 70% for content)
    splitter.setSizes([300, 700])
    
    # Connect the tree view's selection signal to the content viewer
    log_tree.file_selected.connect(log_content.load_file)
    
    # Search functionality
    last_search = {"text": "", "position": 0, "found": False}
    
    def find_text(text, forward=True):
        if not text:
            return
            
        # Reset search position if the search term changed
        if text != last_search["text"]:
            cursor = log_content.textCursor()
            cursor.setPosition(0)
            log_content.setTextCursor(cursor)
            last_search["text"] = text
            last_search["position"] = 0
            
        # Get current cursor and text
        cursor = log_content.textCursor()
        
        # Start search from current position
        if forward:
            found = log_content.find(text)
        else:
            found = log_content.find(text, QTextDocument.FindBackward)
            
        # Update search status
        last_search["found"] = found
        
        # Update the style of the search box based on if text was found
        if found:
            search_edit.setStyleSheet("background-color: #1A1A1A; color: #7FDBFF;")
        else:
            search_edit.setStyleSheet("background-color: #5A1A1A; color: #FF7F7F;")
            
            # If not found and we're searching forward, wrap around to the beginning
            if forward and last_search["position"] > 0:
                cursor.setPosition(0)
                log_content.setTextCursor(cursor)
                found = log_content.find(text)
                if found:
                    search_edit.setStyleSheet("background-color: #1A1A1A; color: #7FDBFF;")
                    
            # If not found and we're searching backward, wrap around to the end
            elif not forward and cursor.position() < log_content.document().characterCount() - 1:
                cursor.setPosition(log_content.document().characterCount() - 1)
                log_content.setTextCursor(cursor)
                found = log_content.find(text, QTextDocument.FindBackward)
                if found:
                    search_edit.setStyleSheet("background-color: #1A1A1A; color: #7FDBFF;")
                    
        # Update last position
        last_search["position"] = log_content.textCursor().position()

    
    # Connect signals
    search_edit.returnPressed.connect(lambda: find_text(search_edit.text(), True))
    next_button.clicked.connect(lambda: find_text(search_edit.text(), True))
    prev_button.clicked.connect(lambda: find_text(search_edit.text(), False))
    
    # Add shortcut to focus search box with Ctrl+F
    def focus_search():
        search_edit.setFocus()
        search_edit.selectAll()
    
    main_window.keyPressEvent = lambda event: focus_search() if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier else QMainWindow.keyPressEvent(main_window, event)
    
    # Function to change the root directory
    def change_root_directory():
        directory = QFileDialog.getExistingDirectory(
            main_window, 
            "Select Root Directory",
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:  # If a directory was selected (not cancelled)
            log_tree.set_root_directory(directory)
            # Save the selected directory to config
            save_config(directory)
    
    # Connect the button to the function
    change_dir_button.clicked.connect(change_root_directory)
    
    # Load saved root directory from config
    saved_directory = load_config()
    
    if saved_directory and os.path.exists(saved_directory):
        # Use saved directory if it exists
        log_tree.set_root_directory(saved_directory)
    else:
        # Fallback to default directory
        log_directory = os.path.expanduser("~/logs")
        if os.path.exists(log_directory):
            log_tree.set_root_directory(log_directory)
        else:
            log_tree.set_root_directory(os.path.expanduser("~"))

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()