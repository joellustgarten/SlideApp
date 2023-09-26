import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_style
from ttkthemes.themed_style import ThemedStyle
from ttkthemes.themed_tk import ThemedTk
import os
import cv2
import imutils
from PIL import Image, ImageTk
import numpy
from tkinter import messagebox
from FileManager import FileManager

# Set slideshow global variables for file and controls
directory = []
first_slide = 0
slide_number = None
size = None
# set video global variables
video = None


class VatApp:

    # open file directory and store in list
    def select_file(self):
        global directory
        global slide_number
        global size
        slide_number = 0
        directory = FileManager().SelectDirectory()
        size = len(directory)

    # Define styles for main window
    def changeTheme(self, theme):
        # style.theme_use(theme)
        ttk.Style().configure('Tbutton', relief='flat', anchor='center')

    # show slides in app and slide window
    def show_slide(self, slide: int):
        image = Image.open(directory[int(slide)])
        resize_image = image.resize((1280, 720))
        image = ImageTk.PhotoImage(resize_image)
        # image = ImageTk.PhotoImage(Image.open(directory[int(slide)]))
        self.label.configure(image=image)
        self.label.image = image
        self.label3.configure(image=image)
        self.label3.image = image

    # goto next slide
    def next_slide(self):
        global slide_number
        global first_slide
        global size
        if first_slide <= slide_number <= (size - 2):
            slide_number += 1
            self.show_slide(slide_number)
        else:
            pass
        print(f'{slide_number}, {first_slide}, {(size - 1)}')

    # goto last slide
    def last_slide(self):
        global slide_number
        global first_slide
        global size
        if first_slide < slide_number <= (size - 1):
            slide_number -= 1
            self.show_slide(slide_number)
        else:
            pass
        print(f'{slide_number}, {first_slide}, {(size - 1)}')

    # start video stream
    def video_stream(self):
        global video
        video = cv2.VideoCapture(0)
        self.initialize()

    # initialize video conversion
    def initialize(self):
        global video
        ret, frame = video.read()
        if ret:
            frame = imutils.resize(frame, width=380)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image=img)
            self.label2.configure(image=image)
            self.label2.image = image
            self.label2.after(10, self.initialize)

    # Close program using close button in root window
    def close_root_window(self):
        self.root.quit()

    def close_window_window(self):
        messagebox.showwarning("Slide viewer", "Close slide screen in\n 'Close slideshow'")

    # Finalize video stream from webcam
    def finalize(self):
        global video
        # label2.place_forget() destroy the label
        video.release()
        self.label2.configure(background='red')

    def __init__(self):

        # Create main (root) window
        self.root = tk.Tk()
        self.root.title('Tkinter Open File Dialog')
        self.root.resizable(True, True)
        # self.root.iconbitmap(self.root, 'resources/logo.ico')
        self.icon = tk.PhotoImage(file='resources/logo.png')
        self.root.iconphoto(True, self.icon)

        # Screen size variables
        root_window_width = 1280
        root_window_height = 680
        root_screen_width = self.root.winfo_screenwidth()
        root_screen_height = self.root.winfo_screenheight()
        root_position_left = int((root_screen_width / 2) - (root_window_width / 2))
        root_position_top = int(((root_screen_height / 2) - (root_screen_height / 2)) - 50)
        # Set root window geometry
        # self.root.geometry('1280x650+0+0')
        self.root.geometry(f'{root_window_width}x{root_window_height}+{root_position_left}+{root_position_top}')
        self.root.minsize(int(root_window_width * 0.66), int(root_window_height * 0.66))

        # Set root window attributes
        self.root.attributes('-alpha', 1)  # Set root window opacity
        self.root.wm_overrideredirect(False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_root_window)
        self.root.bind('<Escape>', lambda event: self.close_root_window)

        # Set root window style
        style = ThemedStyle(self.root)
        style.set_theme("black")

        # Create background label for style setting and resize corner tab
        self.bgPanel = ttk.Labelframe(self.root, border=False)
        self.bgPanel.place(relwidth=1.0, relheight=1.0)
        self.grip = ttk.Sizegrip(self.bgPanel)
        self.grip.place(relx=1.0, rely=1.0, anchor='se')

        # Create menu bar on root window
        self.menu = tk.Menu(self.root)

        # Create sub-menu on root window
        # Sub-menu 1 (program)
        self.sub_menu_program = tk.Menu(self.menu,tearoff=False)
        self.sub_menu_program.add_command(label='Quit', command=self.close_root_window)
        self.menu.add_cascade(label='Program', menu=self.sub_menu_program)

        # Sub-menu 2 (files)
        self.sub_menu_files = tk.Menu(self.menu, tearoff=False)
        self.sub_menu_files.add_command(label='Open file', command=self.select_file)
        self.sub_menu_files.add_command(label='Save file', command='')
        self.menu.add_cascade(label='Files', menu=self.sub_menu_files)

        # Sub-menu 3 ()
        

        # Place menu on root window
        self.root.configure(menu=self.menu)

        # create the label for the slides on the root window
        self.label = tk.Label(self.root, background='blue')
        self.label.place(relwidth=0.50, relheight=0.70, relx=0.3, rely=0.6, anchor='center')

        # create the label for video feed on the root window
        self.label2 = tk.Label(self.root, background='red')
        self.label2.place(relwidth=0.3, relheight=0.6, relx=0.8, rely=0.55, anchor='center')

        # create the toplevel window
        self.window = tk.Toplevel(self.root)
        self.window.title('Slide')
        self.window.resizable(True, True)

        # Screen size variables
        window_window_width = 1280
        window_window_height = 780
        window_screen_width = self.window.winfo_screenwidth()
        window_screen_height = self.window.winfo_screenheight()

        # set Window (window) geometry
        self.window.geometry(f'{window_screen_width}x{window_screen_height - 80}+0+0')
        self.window.minsize(window_window_width, window_window_height)

        # Display Window (window) attributes
        self.window.attributes('-topmost', True)  # Set attributer for always on top
        self.window.protocol("WM_DELETE_WINDOW", self.close_window_window)

        # create the label for slides on toplevel window
        self.label3 = tk.Label(self.window, background='white')
        self.label3.place(relwidth=0.95, relheight=0.95, relx=0.5, rely=0.5, anchor='center')

        # open button
        open_button = ttk.Button(
            self.root,
            text='Open a File',
            command=self.select_file
        )
        open_button.pack(expand=False)

        # open button
        show_button = ttk.Button(
            self.root,
            text='show slide',
            command=lambda: self.show_slide(slide_number)
        )
        show_button.pack(expand=False)
        # next slide button
        next_button = ttk.Button(
            self.root,
            text='Next slide',
            command=self.next_slide
        )
        print('slide number:', slide_number)
        print('first slide: ', first_slide)
        next_button.pack(expand=False)

        # last slide button
        last_button = ttk.Button(
            self.root,
            text='last slide',
            command=self.last_slide
        )
        last_button.pack(expand=False)

        # start video button
        start_button = ttk.Button(
            self.root,
            text='start video',
            command=self.video_stream
        )
        start_button.place(x=100, y=10)

        # stop video button
        stop_button = ttk.Button(
            self.root,
            text='stop video',
            command=self.finalize
        )
        stop_button.place(x=100, y=50)

        # run the application
        self.root.mainloop()


if __name__ == '__main__':
    vatFrame = VatApp()
    vatFrame.__init__()
