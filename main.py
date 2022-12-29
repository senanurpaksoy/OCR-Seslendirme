from tkinter.messagebox import showinfo
import pytesseract
import cv2
from gtts import gTTS
import os
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import tkinter as tk
from os.path import exists as file_exists
from tkinter import ttk


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
options = {"English": "en", "Turkish": "tr"}
root = Tk()
root.title("OCR-SESLENDİRME | ©2022 SENANUR PAKSOY")
root.geometry("600x350")
# root.resizable(False, False)


def open():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir="/gui/images", title="Select A File", filetypes=(("png files", "*.png"),("all files", "*.*")))
    my_label = Label(root, text=root.filename).pack()
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(image=my_image).pack()


my_btn = Button(root, text="Open File", command=lambda: [open(), setTextInput(root.filename)]).pack()

def show():
    global lang
    lang = entry2.get()
    return lang

def setTextInput(text):
    entry1.delete(0, "end")
    entry1.insert(0, text)

entry1 = tk.Entry()
entry2 = tk.Entry()

material = tk.StringVar()
label = ttk.Label(text="Seslendirme Dilini Seçiniz:").pack()
combo = ttk.Combobox(root, state="readonly", values=list(options.keys()), textvariable=material)
combo.current()
combo.bind("<<ComboboxSelected>>",
           lambda event: [show(), entry2.delete(0, "end"), (entry2.insert(0, options[material.get()]))])
combo.pack()

def Process():
    xqc = entry1.get()
    if xqc == "":
        showinfo(title="UYARI!", message="Dosyayı Seçmediniz.")
    elif not xqc.endswith(".png" or ".jpg"):
        showinfo(title="UYARI!",
                 message="Dosya Yolu ya da Dosya Formatı Hatalı. Dosya '.jpg' ya da '.png' uzantılı olmalıdır.")
    elif file_exists(xqc) == False:
        showinfo(title="UYARI!", message="Girdiğiniz dizinde böyle bir dosya bulunmamaktadır.")
    img = cv2.imread(xqc)
    img = cv2.resize(img, (600, 360))

    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    xy = pytesseract.image_to_string(img)
    for z,b in enumerate(boxes.splitlines()):
       if z != 0:
          b = b.split()
          if len(b) == 12:
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
            cv2.putText(img, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

    # cv2.imshow('Detected text', img)
    lang = show()
    audio = gTTS(text = xy, lang =lang, slow = False)
    audio.save("saved_audio.wav")
    os.system("saved_audio.wav")

button1 = Button(root, text='Seslendir', command=lambda: [Process()] ).pack()

root.mainloop()