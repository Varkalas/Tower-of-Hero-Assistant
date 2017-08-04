import math
from tkinter import Tk, ttk, N, W, E, S, CENTER, filedialog, Menu, messagebox

import numpy
from PIL import Image, ImageTk
import pytesseract

from constants import *


class TowerOfHeroAssistant(object):
    def __init__(self):
        # GUI Elements
        self.root = None
        self.frame = None
        self.tree = None

        self.list_of_images = list()

    def create_gui(self):
        # Initialize the GUI
        self.root = Tk()
        self.root.iconbitmap(r"C:\Users\Varkalas D`Lonovan\PycharmProjects\Tower-of-Hero\img\toh_assistant_icon.ico")
        self.root.geometry("1000x800")
        style = ttk.Style(self.root)
        style.configure("Treeview", rowheight=60, background="darkgreen", borderwidth=2)
        style.configure("Treeview.Heading", foreground="black")
        self.frame = ttk.Frame(self.root, width=600, height=800)
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.tree = ttk.Treeview(self.frame)

        # Menu Bar
        menu_bar = Menu(self.root)
        self.frame.master.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Records from PNG", command=self.open_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Table
        self.tree["columns"] = ("Name", "Tier", "Importance", "Order")
        self.tree.heading("#0", text="Item")
        self.tree.column("#0", stretch=False)
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", anchor=W, stretch=False)
        self.tree.heading("Tier", text="Tier")
        self.tree.column("Tier", anchor=CENTER, stretch=False)
        self.tree.heading("Importance", text="Importance")
        self.tree.column("Importance", anchor=CENTER, stretch=False)

    def add_tree_view_elements(self):
        # Append the images to column 1 (alphabetical)
        index = 0
        for item in GAME_ITEMS:
            # Resize the image
            image = item[1][5:56, 16:69]

            # Convert from BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert cv2 image to PIL image
            converted_image = Image.fromarray(image)

            # Convert to ImageTk
            self.list_of_images.append(ImageTk.PhotoImage(converted_image))

            # Append the name, tier, and importance
            self.tree.insert("", "end", image=self.list_of_images[index], values=(item[0], item[2], item[3]))
            index += 1

    def run(self):
        self.create_gui()
        self.add_tree_view_elements()

        # Pack the GUI elements
        self.frame.pack()
        self.tree.pack()

        self.root.mainloop()

    def open_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Choose a Tower of Hero Records image file.",
                                              filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))

    def get_item_order_and_stats(self):
        # Create a new file
        my_file = open("C:\\tmp\\item_location.txt", "w")
        my_file.close()

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
                level_image = IMG_GAME_STATS[y:y + height, x:x + width]
                optimized_level_image = cv2.inRange(level_image, numpy.array([200, 200, 200]),
                                                    numpy.array([255, 255, 255]))
                # cv2.imshow("test", optimized_level_image)
                # cv2.waitKey(0)
                # TODO: Error checking for OCR

                # Optical character recognition
                image = Image.fromarray(optimized_level_image)
                item_level = pytesseract.image_to_string(image, config="tower_of_hero")

                # Remove spaces and LV
                item_level_number = item_level.translate({ord(char): None for char in " LV"})
                with open("C:\\tmp\\item_location.txt", "a") as my_file:
                    my_file.writelines("%s\t%s\t%d\n" % (item[0], item_level_number, item_acquisition_number))
            else:
                messagebox.showerror("Image Recognition Failure",
                                     "Couldn't see {}. Try lowering the match % for images.".format(item[0]))

    def get_cumulative_statistics(self):
        # Find the cumulative statistics
        result = cv2.matchTemplate(IMG_GAME_STATS, IMG_CUMULATIVE_STATS, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.8:
            # Get the region of the textz
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
        level_image = IMG_GAME_STATS[y:y + height, x:x + width]
        optimized_level_image = cv2.inRange(level_image, numpy.array([200, 200, 200]),
                                            numpy.array([255, 255, 255]))
        # cv2.imshow("test", optimized_level_image)
        # cv2.waitKey(0)
        # TODO: Error checking for OCR

        # Optical character recognition
        image = Image.fromarray(optimized_level_image)
        item_level = pytesseract.image_to_string(image, config="tower_of_hero")

if __name__ == "__main__":
    assistant = TowerOfHeroAssistant()
    assistant.run()
