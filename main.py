import sys
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
import ntpath

# Set slideshow global variables for file and controls
directory = []
images = []
first_slide = 0
slide_number = None
size = None
# Set video global variables
video = None
# Set ntpath format
ntpath.basename("a/b/c")


class VatApp:

    # open file directory and store in list
    def select_file(self):
        global directory
        global slide_number
        global size
        slide_number = 0
        directory = FileManager().SelectDirectory()
        size = len(directory)
        if directory:
            for path in directory:
                head, tail = ntpath.split(path)
                images.append(tail+'/')
        self.filePanel.configure(text=images)

    # Define styles for main window
    def changeTheme(self, theme):
        self.style.set_theme(theme)
        ttk.Style().configure('Tbutton', relief='flat', anchor='center')

    # show slides in app and slide window
    def show_slide(self, slide: int):
        image = Image.open(directory[int(slide)])
        resize_image1 = image.resize((1280, 720))
        image1 = ImageTk.PhotoImage(resize_image1)
        slide_window_width = self.slideLabel.winfo_width()
        slide_window_height = self.slideLabel.winfo_height()
        print(slide_window_width)
        print(slide_window_height)
        resize_image2 = image.resize((slide_window_width, slide_window_height))
        image2 = ImageTk.PhotoImage(resize_image2)
        # image = ImageTk.PhotoImage(Image.open(directory[int(slide)]))
        self.slideLabel.configure(image=image2)
        self.slideLabel.image = image2
        self.label3.configure(image=image1)
        self.label3.image = image1

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
        # noinspection PyTypeChecker
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
            self.videoLabel.configure(image=image)
            self.videoLabel.image = image
            self.videoLabel.after(10, self.initialize)

    # Close program using close button in root window
    def close_root_window(self):
        sys.exit()

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
        # self.root.iconbitmap(r'/home/joel/Documents/Projects/SlideApp/resources/logo.png')
        # self.icon = tk.PhotoImage(file='resources/logo.png')
        # self.root.iconphoto(True, self.icon)

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
        self.style = ttk.Style(self.root)
        self.style.theme_use("classic")
        availableThemes = self.style.theme_names()
        # self.style.configure('TButton', relief='flat', anchor='center')
        # self.style.configure('TLabelframe', bordercolor='white', background='blue')

        # Create background label for style setting and resize corner tab
        self.bgPanel = ttk.Labelframe(self.root, border=False)
        self.bgPanel.place(relwidth=1.0, relheight=1.0)
        self.grip = ttk.Sizegrip(self.bgPanel)
        self.grip.place(relx=1.0, rely=1.0, anchor='se')

        # Create menu bar on root window
        self.menu = tk.Menu(self.root, relief='flat', font=("Verdana", 12), background='#95A5A6', activebackground='#839192', border=True, borderwidth=1, )

        # Create sub-menu on root window
        # Sub-menu 1 (program)
        self.sub_menu_program = tk.Menu(self.menu, tearoff=False, relief='flat', font=("Verdana", 12), activebackground='#839192')
        self.sub_menu_program.add_command(label='Quit', command=self.close_root_window)
        self.menu.add_cascade(label='Program', menu=self.sub_menu_program)

        # Sub-menu 2 (files)
        self.sub_menu_files = tk.Menu(self.menu, tearoff=False, relief='flat', font=("Verdana", 12), activebackground='#839192')
        self.sub_menu_files.add_command(label='Open file', command=self.select_file)
        self.sub_menu_files.add_command(label='Save file', command='')
        self.menu.add_cascade(label='Files', menu=self.sub_menu_files)

        # Sub-menu 3 (settings)
        self.sub_menu_settings = tk.Menu(self.menu, tearoff=False, relief='flat', font=("Verdana", 12),activebackground='#839192')
        # Nested sub-menu for themes
        self.sub_menu_themes = tk.Menu(self.root, tearoff=False, relief='flat', font=("Verdana", 12), activebackground='#839192')
        self.sub_menu_settings.add_cascade(label='Themes', menu=self.sub_menu_themes)

        for t in availableThemes:
            self.sub_menu_themes.add_cascade(label=t, command=lambda t=t: self.changeTheme(t))

        self.sub_menu_settings.add_command(label='Help', command='')
        self.menu.add_cascade(label='Settings', menu=self.sub_menu_settings)

        # Place menu on root window
        self.root.configure(menu=self.menu)

        # Create label to grid-align upper button row
        self.button_frame = ttk.Label(self.root, border=True, borderwidth=0.3, relief='groove', background='#95A5A6')
        self.button_frame.place(relwidth=0.95, relheight=0.08, relx=0.025, rely=0.02)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.rowconfigure(0, weight=1)

        # Define and place upper row buttons
        # Open file button
        self.open_button = tk.Button(self.button_frame, text='OPEN FILE', command=self.select_file, cursor='mouse', width=18)
        self.style.configure('TButton.label', justify='center')
        self.open_button.grid(row=0, column=0)

        # Show slide button
        self.show_button = tk.Button(self.button_frame, text='SHOW SLIDE', command=lambda: self.show_slide(slide_number), cursor='mouse', width=18)
        self.style.configure('TButton.label', justify='center')
        self.show_button.grid(row=0, column=1)

        # Next slide button
        self.stream_button = tk.Button(self.button_frame, text='START STREAMING', command=self.video_stream, cursor='mouse', width=18)
        self.style.configure('TButton.label', justify='center')
        self.stream_button.grid(row=0, column=2)

        # Last slide button
        self.stop_stream_button = tk.Button(self.button_frame, text='STOP STREAMING', command=self.finalize, cursor='mouse', width=18)
        self.style.configure('TButton.label', justify='center')
        self.stop_stream_button.grid(row=0, column=3)

        # Create and place label frame for image folder content
        self.title_file_panel = ttk.Label(self.root, border=False, text='FILE CONTENT', foreground='black', font=("Verdana", 8))
        self.title_file_panel.place(relx=0.05, rely=0.12)
        self.filePanel = ttk.Label(self.root, border=True, text='', background='white', foreground='black')
        self.filePanel.place(relwidth=0.90, relheight=0.035, relx=0.05, rely=0.15)

        # create the label for the slides on the root window
        self.slideLabel = tk.Label(self.root, border=True, borderwidth=1, relief='groove')
        self.slideLabel.place(relwidth=0.4, relheight=0.590, relx=0.25, rely=0.53,  anchor='center')

        # create the label for video feed on the root window
        self.videoLabel = tk.Label(self.root, border=True, borderwidth=0.5, relief='groove')
        self.videoLabel.place(relwidth=0.3, relheight=0.46, relx=0.66, rely=0.466, anchor='center')

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
        self.window.attributes('-topmost', True)  # Set attribute for always on top
        self.window.protocol("WM_DELETE_WINDOW", self.close_window_window)

        # create the label for slides on toplevel window
        self.label3 = tk.Label(self.window, background='white')
        self.label3.place(relwidth=0.95, relheight=0.95, relx=0.5, rely=0.5, anchor='center')

        # run the application
        self.root.mainloop()


if __name__ == '__main__':
    vatFrame = VatApp()
    vatFrame.__init__()
