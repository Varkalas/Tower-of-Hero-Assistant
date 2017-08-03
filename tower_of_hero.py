import math

import cv2
import numpy
from PIL import Image, ImageTk
import pytesseract
import tkinter
from tkinter import ttk

from constants import *
from images import *


if __name__ == "__main__":
    # Initialize the GUI
    root = tkinter.Tk()
    root.geometry("1000x800")
    style = ttk.Style(root)
    style.configure("Treeview", rowheight=60, background="darkgreen", borderwidth=2)
    style.configure("Treeview.Heading", foreground="black")
    frame = ttk.Frame(root, width=600, height=800)
    frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    tree = ttk.Treeview(frame)

    # Table
    tree["columns"] = ("Name", "Tier", "Importance", "Order")
    tree.heading("#0", text="Item")
    tree.column("#0", stretch=False)
    tree.heading("Name", text="Name")
    tree.column("Name", anchor=tkinter.W, stretch=False)
    tree.heading("Tier", text="Tier")
    tree.column("Tier", anchor=tkinter.CENTER, stretch=False)
    tree.heading("Importance", text="Importance")
    tree.column("Importance", anchor=tkinter.CENTER, stretch=False)
    #tree.heading("Order", text="Order Acquired")
    #tree.column("Order", anchor=tkinter.CENTER, stretch=False)
    #tree["show"] = "headings"

    # Append the images to column 1 (alphabetical)
    list_of_images = list()
    index = 0
    for item in GAME_ITEMS:
        # Resize the image
        image = item[1][5:56, 16:69]

        # Convert from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert cv2 image to PIL image
        converted_image = Image.fromarray(image)

        # Convert to ImageTk
        list_of_images.append(ImageTk.PhotoImage(converted_image))

        tree.insert("", "end", image=list_of_images[index], values=(item[0], item[2], item[3]))
        index += 1

    # Append the item names to column 2

    # Create a new file
    my_file = open("C:\\tmp\\item_location.txt", "w")
    my_file.close()

    # Run the GUI
    frame.pack()
    tree.pack()
    root.mainloop()

    # TODO: make this section part of GUI button (e.g. Import Data From Records Image)
    # Go through each item
    for item in GAME_ITEMS:
        # Match the template and if it's >= 80%, run with it
        result = cv2.matchTemplate(IMG_GAME_STATS, item[1], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.8:
            # Get the region of the text
            x = max_loc[0] - 2
            y = max_loc[1] + 51
            width = 95
            height = 24

            # Find the location of the item to get the item acquisition order
            row_number = math.floor((max_loc[0] - 34) / 92) + 1
            column_number = math.floor((max_loc[1] - 1150) / 80)
            item_acquisition_number = row_number + (11 * column_number)
            if item_acquisition_number >= 12:
                item_acquisition_number -= 1

            # Optimize the image for Tesseract OCR to accurately get the numbers
            level_image = IMG_GAME_STATS[y:y+height, x:x+width]
            optimized_level_image = cv2.inRange(level_image, numpy.array([200, 200, 200]), numpy.array([255, 255, 255]))
            # cv2.imshow("test", optimized_level_image)
            # cv2.waitKey(0)

            # Optical character recognition
            image = Image.fromarray(optimized_level_image)
            item_level = pytesseract.image_to_string(image, config="tower_of_hero")

            # Remove spaces and LV
            item_level_number = item_level.translate({ord(char): None for char in " LV"})
            with open("C:\\tmp\\item_location.txt", "a") as my_file:
                my_file.writelines("%s\t%s\t%d\n" % (item[0], item_level_number, item_acquisition_number))
