import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton
import ctypes
import shutil

class ClearStorageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Storage Cleaner')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.recycler_bin_checkbox = QCheckBox('Recycle Bin')
        self.temporary_files_checkbox = QCheckBox('Temporary Files')

        layout.addWidget(self.recycler_bin_checkbox)
        layout.addWidget(self.temporary_files_checkbox)

        clear_button = QPushButton('Clear Selected')
        clear_button.clicked.connect(self.clear_selected)
        layout.addWidget(clear_button)

        self.setLayout(layout)

    def clear_selected(self):
        if self.recycler_bin_checkbox.isChecked():
            self.empty_recycle_bin()
        if self.temporary_files_checkbox.isChecked():
            self.clear_temporary_files()

    def empty_recycle_bin(self):
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
        SHEmptyRecycleBin(None, None, 0)

    def clear_temporary_files(self):
        temp_path = os.environ.get('TEMP')
        if temp_path:
            for root, dirs, files in os.walk(temp_path):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except PermissionError:
                        pass
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                    except PermissionError:
                        pass

if __name__ == '__main__':
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    app = QApplication(sys.argv)
    window = ClearStorageApp()
    window.show()
    sys.exit(app.exec_())