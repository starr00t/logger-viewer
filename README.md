# Log Viewer

This project is a log viewer application developed using PyQt. It provides a user-friendly interface for browsing log folders and files, displaying their contents in a structured manner.

## Features

- **Tree View**: Browse through log folders and files on the left side of the interface.
- **Log Content Display**: View the contents of selected log files on the right side.
- **Easy Navigation**: Quickly navigate through different log files and folders.

## Project Structure

```
log-viewer
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui                     # UI components
│   │   ├── __init__.py        # UI package initializer
│   │   ├── main_window.py      # Main window layout
│   │   ├── log_tree_view.py    # Tree view for log files
│   │   └── log_content_view.py  # View for log file content
│   ├── models                  # Data models
│   │   ├── __init__.py        # Models package initializer
│   │   └── log_tree_model.py   # Model for the log tree view
│   ├── controllers             # Controllers for handling logic
│   │   ├── __init__.py        # Controllers package initializer
│   │   └── log_controller.py    # Logic for interacting with logs
│   └── utils                   # Utility functions
│       ├── __init__.py        # Utils package initializer
│       └── log_parser.py       # Functions for parsing log files
├── resources                   # Resource files
│   └── styles.qss             # Stylesheet for UI components
├── requirements.txt            # Project dependencies
├── setup.py                   # Setup script for packaging
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd log-viewer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage

- Launch the application to view the log folders and files.
- Click on a file in the tree view to display its contents on the right side of the interface.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.