# Source: https://github.com/x4nth055/pythoncode-tutorials/blob/master/gui-programming/text-editor/text_editor.py, from Rockikz x4nth055 https://github.com/x4nth055
# MIT License

# Import
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox

import tkinter.font as tf
import platform
import os
import sys
import subprocess
import json

# Increas Dots Per inch so it looks sharper
# ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup Variables

class TTinyedApp:
    nofileOpenedString = 'New File'
    def __init__(self):
        self.name = 'ttinyed'
        self.config = {}
        with open('config.json') as fh:
            self.config = json.load(fh)
        self.os = platform.system()
        self.conf = self.config[self.os]
        self.cwd = cwd = os.getcwd()
        self.fontsize = self.conf['fontsize']
        self.fontfamily = "TkTextFont"
        self.ftypes = [("Text Files","*.txt"), ("Python","*.py"),  ("Markdown","*.md"), ("Any", "*")]

app = TTinyedApp()

currentFilePath = app.nofileOpenedString

# Tkinter Setup
window = Tk()

# Font settings
dFont = tf.Font(family=app.fontfamily, size=app.fontsize)
window.option_add("*Font", (app.fontfamily, app.fontsize, "normal"))
window.option_add("*Label.Font", (app.fontfamily, app.fontsize, "normal"))

# Set the first column to occupy 100% of the width
window.grid_columnconfigure(0, weight=1)

window.title(app.name + " - " + currentFilePath)

# Window Dimensions in Pixel
window.geometry('1000x1250' if platform.system() == 'Linux' else '750x750')

textsave = ""

def saveundo():
    global undo
    new = txt.get(1.0,END)
    if undo == [] or new != undo[-1]:
        undo.append(txt.get(1.0,END))
        if len(undo) > 100:
            undo = undo[1:]
        #print(''.join([u for u in undo]))
def crude_undo(event=False):
    global undo
    if len(undo) > 0:
        txt.delete(1.0,END)
        txt.insert(INSERT,undo[-1])
        undo = undo[:-1]

# Handler Function for Edit menu dropdown:
def editDropDownHandler(action):
    global textsave, SEL_FIRST, SEL_LAST
    # cut1, cut2, cut3?
    if action == "copy":
        content = txt.get(SEL_FIRST, SEL_LAST)
        textsave = content
        print(f"copied: {content}")
    elif action == "selectAll":
        txt.tag_add("sel", "1.0", END)
        txt.focus_force()
    elif action == "paste":
        # FIXME: if a text is selected, erase it first!
        print(f"inserted: {textsave}")
        txt.insert(INSERT, textsave)
    # Continue here:
    # https://www.javatpoint.com/python-tkinter-text
    # https://stackoverflow.com/questions/4073468/how-do-i-get-a-selected-string-in-from-a-tkinter-text-box

def callshell(wd):
    shcmd = app.conf['shell']
    path = app.cwd if wd == '' else wd
    path = path.replace('/', app.conf['pathsepr'])
    print(shcmd, path)
    os.system(f"{shcmd}'{path}'")
def callfilemgr(wd):
    fmgrcmd = app.conf['filemgr']
    path = app.cwd if wd == '' else wd
    path = path.replace('/', app.conf['pathsepr'])
    emb = app.conf['pathemb']
    print(fmgrcmd, path)
    os.system(f"{fmgrcmd} {emb}{path}{emb}")
# Handler Function for Tools menu dropdown:
def toolsDropDownHandler(action):
    global textsave, currentFilePath
    # cut1, cut2, cut3?
    print(action)
    if action == "shell":
        currentdir = '/'.join(currentFilePath.split('/')[0:-1])
        print(f'cwd={currentdir}')
        callshell(currentdir)
        #subprocess.call(['xfce4-terminal', f'--working-directory={currentdir}'])
    elif action == "filemgr":
        currentdir = '/'.join(currentFilePath.split('/')[0:-1])
        #subprocess.call(['thunar', currentdir])
        print(f'cwd={currentdir}')
        callfilemgr(currentdir)

def textchange(event):
    window.title(app.name + " - *" + currentFilePath)

# Widgets

# Text Area
txt = scrolledtext.Text(window, height=40, bg='#AADDAA', wrap=WORD, width=40, font=dFont)
txt.grid(row=1,sticky=N+S+E+W)

txt.configure(font = (app.fontfamily, app.fontsize, "normal"), tabs=('1c', '2c', '3c', '4c'))

# Scrollbar
yscrollbar=Scrollbar(window, orient=VERTICAL, command=txt.yview) # →
yscrollbar.grid(row=1, column=1, sticky=N+S+E+W) # →
txt["yscrollcommand"]=yscrollbar.set
txt.update()

h=int(round(txt.winfo_height()/txt["height"])), int(round(txt.winfo_width()/txt["width"]))

def resize(event):
    pixelX = window.winfo_width()-yscrollbar.winfo_width()
    pixelY = window.winfo_height()
    txt["width"] = int(round(pixelX/h[1]))
    txt["height"] = int(round(pixelY/h[0]))

# Bind event in the widget to a function
txt.bind('<KeyPress>', textchange)
window.bind("<Configure>", resize)

# Menu
menu = Menu(window)
menu.configure(font = (app.fontfamily, app.fontsize, "normal"))

# set tearoff to 0
fileDropdown = Menu(menu, tearoff=False)

### File ###
### File > New ###
def new_file(event=False):
    global currentFilePath, undo
    currentFilePath = nofileOpenedString
    txt.delete(1.0,END)
    undo = [txt.get(1.0,END)]
    window.title(appName + " - " + currentFilePath)
### File > Open ###
def open_file(event=False):
    global currentFilePath
    file = filedialog.askopenfilename(filetypes = app.ftypes)
    if file == '' or file == ():
        return
    window.title(app.name + " - " + str(file))
    currentFilePath = file
    try:
        with open(file, 'r') as f:
            txt.delete(1.0,END)
            txt.insert(INSERT,f.read())
        undo = [txt.get(1.0,END)]
    except Exception as e:
        # print(f'Could not open file: {file}')
        messagebox.showerror("Open File Error", f"Could not open file:\n{file}\n\nError: {e}")
        window.title(appName + "")
### File > Save ###
def save_current_file(event=False):
    global currentFilePath
    if currentFilePath == nofileOpenedString:
        currentFilePath = filedialog.asksaveasfilename(filetypes = app.ftypes)
    try:
        with open(currentFilePath, 'w') as f:
            f.write(txt.get('1.0','end'))
        window.title(appName + " - " + currentFilePath)
    except Exception as e:
        messagebox.showerror("Save File Error", f"Could not save file:\n{currentFilePath}\n\nError: {e}")
### File > Save As ###
def save_as_current_file(event=False):
    global currentFilePath
    currentFilePath = filedialog.asksaveasfilename(filetypes = app.ftypes)
    try:
        with open(currentFilePath, 'w') as f:
            f.write(txt.get('1.0','end'))
        window.title(appName + " - " + currentFilePath)
    except Exception as e:
        messagebox.showerror("Save As Error", f"Could not save file:\n{currentFilePath}\n\nError: {e}")
### File > Exit ###
def exit_program(event=False):
    # TODO: here test if file is changed, if not ask to save
    exit()
### Edit > Cut ###
def cut_sel(event=False):
    global textsave, SEL_FIRST, SEL_LAST
    # cut1, cut2, cut3?
    content = txt.get(SEL_FIRST, SEL_LAST)
    textsave = content
    txt.delete(SEL_FIRST, SEL_LAST)
    print(f"cut: {content}")

#### File menu items
fileDropdown.add_command(label='New', accelerator="Ctrl+N", command=new_file)
fileDropdown.add_command(label='Open', accelerator="Ctrl+O", command=open_file)
fileDropdown.add_separator()
fileDropdown.add_command(label='Save', accelerator="Ctrl+S", command=save_current_file)
fileDropdown.add_command(label='Save as', accelerator="Ctrl+Shift+S", command=save_as_current_file)
fileDropdown.add_command(label='Exit', accelerator="Ctrl+Q", command=exit_program)

menu.add_cascade(label='File', menu=fileDropdown)

#### Edit menu items
editDropdown = Menu(menu, tearoff=False)
editDropdown.add_command(label='Undo', accelerator="Ctrl+Z", command=crude_undo)
editDropdown.add_command(label='Cut', accelerator="Ctrl+X", command=cut_sel)
editDropdown.add_command(label='Copy', accelerator="Ctrl+C", command=lambda: editDropDownHandler("copy"))
editDropdown.add_command(label='Paste', accelerator="Ctrl+P", command=lambda: editDropDownHandler("paste"))
editDropdown.add_command(label='Select All', accelerator="Ctrl+A", command=lambda: editDropDownHandler("selectAll"))

menu.add_cascade(label='Edit', menu=editDropdown)

#### Tools menu items
toolsDropdown = Menu(menu, tearoff=False)
toolsDropdown.add_command(label='Shell', accelerator="Ctrl+Alt+S", command=lambda: toolsDropDownHandler("shell"))
toolsDropdown.add_command(label='File manager', accelerator="Ctrl+Alt+F", command=lambda: toolsDropDownHandler("filemgr"))

menu.add_cascade(label='Tools', menu=toolsDropdown)

# Set Menu to be Main Menu
window.config(menu=menu)

# Keypress stuff
def copy_sel(event=False):
    editDropDownHandler("copy")
    saveundo()
def paste_cut(event=False):
    editDropDownHandler("paste")
    saveundo()
def sel_all(event=False):
    editDropDownHandler("selectAll")
    saveundo()
def open_shell(event=False):
    toolsDropDownHandler("shell")
def open_file_manager(event=False):
    toolsDropDownHandler("filemgr")

def key(a):
    saveundo()
    print(f"Key {a}")

# hotkey to save current file
window.bind('<Control-n>', new_file)
window.bind('<Control-o>', open_file)
window.bind('<Control-Shift-S>', save_as_current_file)
window.bind('<Control-s>', save_current_file)
window.bind('<Control-q>', exit_program)

window.bind('<Control-z>', crude_undo)
window.bind('<Control-x>', cut_sel)
window.bind('<Control-c>', copy_sel)
window.bind('<Control-p>', paste_cut)
window.bind('<Control-a>', sel_all)

window.bind('<Control-Alt-s>', open_shell)
window.bind('<Control-Alt-f>', open_file_manager)
window.bind("<Key>", key)

# Enabling "open with" by looking if the second argument was passed.
if len(sys.argv) == 2:
    currentFilePath = sys.argv[1]
    window.title(app.name + " - " + currentFilePath)
    if os.path.isfile(currentFilePath):
        with open(currentFilePath, 'r') as f:
            txt.delete(1.0,END)
            txt.insert(INSERT,f.read())

undo = [txt.get(1.0,END)]
# Main Loop
window.mainloop()
