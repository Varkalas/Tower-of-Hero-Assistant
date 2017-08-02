import math

import numpy
from PIL import Image
import pytesseract
import tkinter
from tkinter import ttk

from constants import *
from images import *


if __name__ == "__main__":
    # Initialize the GUI
    '''root = tkinter.Tk()
    tree = ttk.Treeview(root)
    tree["columns"] = ("Item", "Name", "Tier", "Importance", "Order")'''

    # Append the images to column 1 (alphabetical)

    # Append the item names to column 2

    # Create a new file
    my_file = open("C:\\tmp\\item_location.txt", "w")
    my_file.close()

    # TODO: make this section part of GUI button (e.g. Gather Data)
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

    # Run the GUI
    '''tree.pack()
    root.mainloop()'''
