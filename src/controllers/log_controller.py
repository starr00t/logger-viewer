class LogController:
    def __init__(self, log_tree_view, log_content_view):
        self.log_tree_view = log_tree_view
        self.log_content_view = log_content_view
        
        self.log_tree_view.file_selected.connect(self.on_file_selected)

    def on_file_selected(self, file_path):
        log_content = self.load_log_file(file_path)
        self.log_content_view.display_content(log_content)

    def load_log_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error loading file: {str(e)}"