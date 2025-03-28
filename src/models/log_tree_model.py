from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
import os

class LogTreeModel(QAbstractItemModel):
    def __init__(self, root_path):
        super().__init__()
        self.root_path = root_path
        self.root_item = self._build_tree(root_path)

    def _build_tree(self, path):
        item = LogTreeItem(os.path.basename(path), path)
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                item.append_child(self._build_tree(full_path))
            else:
                item.append_child(LogTreeItem(entry, full_path))
        return item

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return 1
        item = self.get_item(parent)
        return item.child_count()

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        item = self.get_item(index)
        return item.data()

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            return self.createIndex(0, 0, self.root_item)
        parent_item = self.get_item(parent)
        child_item = parent_item.child(row)
        return self.createIndex(row, column, child_item)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        child_item = self.get_item(index)
        parent_item = child_item.parent()
        if parent_item == self.root_item:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def get_item(self, index):
        return index.internalPointer()

class LogTreeItem:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.children = []

    def append_child(self, child_item):
        self.children.append(child_item)

    def child(self, row):
        return self.children[row]

    def child_count(self):
        return len(self.children)

    def data(self):
        return self.name

    def parent(self):
        return None  # This can be modified to keep track of parent if needed

    def row(self):
        if self.parent() is None:
            return 0
        return self.parent().children.index(self)