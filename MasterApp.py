import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import os
import cv2
from cvzone.HandTrackingModule import HandDetector
from PIL import Image
from PIL import ImageTk
import numpy as np
import mediapipe
from ttkthemes.themed_tk import ThemedTk

from HandGesture import pathImages, folderPath, imgNumber


#define class
class VatApp:
    # old testing variables
    """
    window=None
    InnerFrame=None
    webCanera=None """
    # General variables for video capture and display inc. hand tracking
    # folderPath = 'present'
    window_width = 1200  # used for slide display and hand tracking
    window_height = 670  # used for slide display and hand tracking
    imgNumber = 0
    hs, ws = int(120 * 1), int(213 * 1)  # size of small video window, change as required
    gestureThreshold = 300
    buttonPressed = False
    buttonCounter = 0
    buttonDelay = 15

    def changeTheme(t):
        #style.theme_use(t)
        ttk.Style().configure("TButton", relief="flat", anchor='center')


    def slideLoad(slide_image=None):
        pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
        slideImage = cv2.imread(pathFullImage)
        cv2.imshow('Slides', slideImage)
        test = cv2.imshow('Slides', slideImage)
        slide_image.configure(image=slideImage)


    def __init__(self):
       # window basic settings
        self.window = tk.Tk()
        self.window.title(' VTA - Virtual Training App')
        self.window.resizable(True, True) # boolean for resize x and y
        self.window.iconbitmap(self.window, 'testlogo.ico')
        # screen information to open full height
        display_width = self.window.winfo_screenwidth()
        display_height = self.window.winfo_screenheight()
        position_left = int((display_width / 2) - (self.window_width / 2))
        position_top = int(((display_height / 2) - (self.window_height / 2))-50)
        # window size and position
        self.window.geometry(f'{self.window_width}x{self.window_height}+{position_left}+{position_top}') #check for errors
        self.window.minsize(int(self.window_width * 0.66), int(self.window_height * 0.66))
        # window location & attributes
        self.window.attributes('-alpha', 1)  # Set window opacity, change int(index)
        self.window.attributes('-topmost', True)  # Change True or False to keep on top
        self.window.attributes('-fullscreen', False)  # Change True or False for full screen
        # override title bar and change boolean, requires close event window.bind
        self.window.wm_overrideredirect(False)
        # safety escape event
        self.window.bind('<Escape>', lambda event: self.window.quit())
        # defining window style
        style = ThemedStyle(self.window)
        style.set_theme("black")
        availableThemes = style.theme_names()
        style.configure("TButton", relief="flat", anchor='center')
        # create panel for background styling
        bgPanel = ttk.LabelFrame(self.window, border=None)
        bgPanel.place(relwidth=1.0, relheight=1.0)
        # include resize corner tab
        grip = ttk.Sizegrip(bgPanel)
        grip.place(relx=1.0, rely=1.0, anchor='se')
        # create menu bar
        menu = tk.Menu(self.window)
        # create sub-menu
        # sub-menu 1 (program)
        menu_program = tk.Menu(menu, tearoff=False)
        menu_program.add_command(label='Exit', command=self.window.destroy)
        menu.add_cascade(label='Program', menu=menu_program)
        # sub-menu 2 (file)
        menu_file = tk.Menu(menu, tearoff=False)
        menu_file.add_command(label='Open file', command=lambda: print('open file'))
        menu_file.add_command(label='Close file', command=lambda: print('open file'))
        menu.add_cascade(label='File', menu=menu_file)
        # sub-menu 3 (settings)
        menu_settings = tk.Menu(menu, tearoff=False)
        # Nested sub-menu for themes
        menu_themes = tk.Menu(self.window, tearoff=False)
        menu_settings.add_cascade(label="Themes", menu=menu_themes)
        # Themes sub-manu

        for t in availableThemes:
            menu_themes.add_cascade(label=t, command=lambda t=t: style.theme_use(t))

        menu_settings.add_command(label='Camera calibration', command='')
        menu.add_cascade(label='Settings', menu=menu_settings)
        # sub-menu 4 (help)
        menu_help = tk.Menu(menu, tearoff=False)
        menu_help.add_command(label='Online help', command=lambda: print('open file'))
        menu.add_cascade(label='Help', menu=menu_help)
        # Place menu on window
        self.window.configure(menu=menu)
        # Create and place slide frame on window
        slide_panel = ttk.LabelFrame(self.window, text=' Video feed: ')
        slide_panel.place(relwidth=0.60, relheight=0.71, relx=0.030, rely=0.043)
        # Place slide image in slide_panel
        slide_image = ttk.Label(slide_panel, background='white')
        slide_image.place(anchor='center', relwidth=0.965, relheight=0.965, relx=0.5, rely=0.5)
        # Create and place button frame on window
        button_panel = ttk.LabelFrame(self.window)
        button_panel.place(relwidth=0.60, relheight=0.10, relx=0.030, rely=0.78)
        # Define grid distribution for button_panel
        button_panel.columnconfigure(0, weight=1)
        button_panel.columnconfigure(1, weight=1)
        button_panel.columnconfigure(2, weight=1)
        button_panel.columnconfigure(3, weight=1)
        button_panel.columnconfigure(4, weight=1)
        button_panel.rowconfigure(0, weight=1)
        # define  buttons
        playButton = ttk.Button(button_panel, text='PLAY', command=lambda: slide_panel, cursor='target', width=18)
        leftButtonDouble = ttk.Button(button_panel, text='<<  FIRST SLIDE', command='', cursor='target', width=18)
        rightButtonDouble = ttk.Button(button_panel, text='LAST SLIDE >>', command='', cursor='target', width=18)
        leftButtonSingle = ttk.Button(button_panel, text='< PREV SLIDE', command='', cursor='target', width=18)
        rightButtonSingle = ttk.Button(button_panel, text='NEXT SLIDE >', command='', cursor='target', width=18)
        # Set buttons on button_panel
        playButton.grid(row=0, column=2)
        leftButtonDouble.grid(row=0, column=1)
        rightButtonDouble.grid(row=0, column=3)
        leftButtonSingle.grid(row=0, column=0)
        rightButtonSingle.grid(row=0, column=4)
        # Create and place video feed frame on window
        video_panel = ttk.LabelFrame(self.window, text=' Actual slide ')
        video_panel.place(relwidth=0.31, relheight=0.35, relx=0.66, rely=0.043)
        # Place slide image in slide_panel
        video_image = ttk.Label(video_panel, background='white')
        video_image.place(anchor='center', relwidth=0.965, relheight=0.955, relx=0.5, rely=0.5)
        # labels for number of fingers
        fingerLabel = ttk.Label(self.window, text='Detected fingers: ', font=('Arial', 25))
        fingerLabel.place(relwidth=0.31, relx=0.66, rely=0.42, )
        # labels for number of fingers data
        fingerNumber = ttk.Label(self.window, text='', font=('Arial bold', 75), anchor="center")
        fingerNumber.place(relwidth=0.31, relx=0.66, rely=0.49)
        # labels for command
        commandLabel = ttk.Label(self.window, text='Command: ', font=('Arial', 25), anchor="w")
        commandLabel.place(relwidth=0.31, relx=0.66, rely=0.665)
        # Command text label
        commandText = ttk.Label(self.window, text='', font=('Arial bold', 45), anchor='center')
        commandText.place(relwidth=0.31, relx=0.66, rely=0.735)
        # Label for threshold line height change
        tLineLabel = ttk.Label(self.window, text='')
        tLineLabel.place(relwidth=0.31, relheight=0.10, relx=0.66, rely=0.865)
        # Define grid distribution for threshold line panel
        tLineLabel.columnconfigure(0, weight=1)
        tLineLabel.columnconfigure(1, weight=1)
        tLineLabel.rowconfigure(0, weight=1)
        tLineLabel.rowconfigure(1, weight=1)
        # text label for threshold line adjustment and arrow buttons
        tLine = ttk.Label(tLineLabel, text='Adjust threshold line', font=('Arial bold', 20), anchor='e')
        #plusSign = tk.PhotoImage(file='arrowUp.png')
        #upButton = ttk.Button(tLineLabel, image=plusSign, command='', cursor='target')
        upButton = ttk.Button(tLineLabel, text=">", command='', cursor='target')
        #minusSign = tk.PhotoImage(file='arrowDown.png')
        #downButton = ttk.Button(tLineLabel, image=minusSign, command='', cursor='target')
        downButton = ttk.Button(tLineLabel, text="<", command='', cursor='target')
        # Set text and buttons in threshold line panel
        tLine.grid(column=0, row=0, rowspan=2)
        upButton.grid(column=1, row=0)
        downButton.grid(column=1, row=1)
        # button for drawing function
        drawButton = ttk.Button(self.window, text='DRAW', command='', cursor='target')
        drawButton.place(relx=0.13, rely=0.91)
        # Zoom button
        zoomButton = ttk.Button(self.window, text='ZOOM', command='', cursor='target')
        zoomButton.place(relx=0.41, rely=0.91)
        #place the window in display
        self.window.mainloop()


if __name__=='__main__':
    vatFrame = VatApp()