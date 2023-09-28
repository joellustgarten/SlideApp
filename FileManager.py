import tkinter as tk
import os
from tkinter import filedialog, messagebox

class FileManager:
    def __init__(self, title="Select presentation folder"):
        self.title = title

    def SelectDirectory(self):
        root = tk.Tk()
        root.withdraw()

        # Open a file dialog to select a directory
        directory = filedialog.askdirectory(title=self.title)

        # If a directory is selected, return a list of files in that directory
        if directory:
            Files = self.selectFiles(directory)
            return Files
        else:
            return []

    def selectFiles(self, Directory):
        Files = []
        for root, _, files in os.walk(Directory):
            for file in files:
                Files.append(os.path.join(root, file))
        return Files

if __name__ == "__main__":
    file_manager = FileManager()
    FileLists = file_manager.SelectDirectory()

    if FileLists:
        print(FileLists)
    else:
        print("No directory selected")

# This class, FileManager, allows you to create an instance and call the
# SelectDirectory() method to open a file dialog and return a list of files
# in the selected directory. You can customize the title of the file dialog by
# passing it as an argument to the class constructor.