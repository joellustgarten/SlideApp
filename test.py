import tkinter as tk
from tkinter import ttk

import cv2
import imutils
from PIL import Image, ImageTk

from FileManager import FileManager


# Set slideshow global variables for file and controls
directory = []
first_slide = 0
slide_number = None
size = None
# set video global variables
video = None
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('1280x650')
# create the label for the slides on the root window
label = tk.Label(root, background='blue')
label.place(relwidth=0.50, relheight=0.70, relx=0.3, rely=0.6, anchor='center')
# create the label for video feed on the root window
label2 = tk.Label(root, background='red')
label2.place(relwidth=0.3, relheight=0.6, relx=0.8, rely=0.55, anchor='center')


# create the toplevel window
window = tk.Toplevel(root)
window.title('Slide')
window.resizable(False, False)
WIDTH, HEIGHT = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry(f'{WIDTH}x{HEIGHT-80}+0+0')
# create the label for slides on toplevel window
label3 = tk.Label(window, background='white')
label3.place(relwidth=0.95, relheight=0.95, relx=0.5, rely=0.5, anchor='center')
print(WIDTH, HEIGHT)

# open file directory and store in list
def select_file():
    global directory
    global slide_number
    global size
    slide_number = 0
    directory = FileManager().SelectDirectory()
    size = len(directory)


# show slides in app and slide window
def show_slide(slide: int):
    image = Image.open(directory[int(slide)])
    resize_image = image.resize((1280,720))
    image = ImageTk.PhotoImage(resize_image)
    #image = ImageTk.PhotoImage(Image.open(directory[int(slide)]))
    label.configure(image=image)
    label.image = image
    label3.configure(image=image)
    label3.image = image


# goto next slide
def next_slide():
    global slide_number
    global first_slide
    global size
    if first_slide <= slide_number <= (size-2):
        slide_number += 1
        show_slide(slide_number)
    else:
        pass
    print(f'{slide_number}, {first_slide}, {(size - 1)}')


# goto last slide
def last_slide():
    global slide_number
    global first_slide
    global size
    if first_slide < slide_number <= (size-1):
        slide_number -= 1
        show_slide(slide_number)
    else:
        pass
    print(f'{slide_number}, {first_slide}, {(size - 1)}')


# start video stream
def video_stream():
    global video
    video = cv2.VideoCapture(0)
    initialize()


# initialize video conversion
def initialize():
    global video
    ret, frame = video.read()
    if ret:
        frame = imutils.resize(frame, width=380)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image=img)
        label2.configure(image=image)
        label2.image = image
        label2.after(10, initialize)


# stop video feed
def finalize():
    global video
    # label2.place_forget() destroy the label
    video.release()
    label2.configure(background='red')


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=False)


# open button
show_button = ttk.Button(
    root,
    text='show slide',
    command=lambda: show_slide(slide_number)
)
show_button.pack(expand=False)
# next slide button
next_button = ttk.Button(
    root,
    text='Next slide',
    command=next_slide
)
next_button.pack(expand=False)


# last slide button
last_button = ttk.Button(
    root,
    text='last slide',
    command=last_slide
)
last_button.pack(expand=False)


# start video button
start_button = ttk.Button(
    root,
    text='start video',
    command=video_stream
)
start_button.place(x=100, y=10)


# stop video button
stop_button = ttk.Button(
    root,
    text='stop video',
    command=finalize
)
stop_button.place(x=100, y=50)

# run the application
root.mainloop()