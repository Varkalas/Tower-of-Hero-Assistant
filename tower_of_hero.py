# Imports
import math
from os import system
from tempfile import gettempdir
from time import time
from tkinter import Toplevel, Frame, Tk, ttk, CENTER, TOP, W, filedialog, Menu, Label, Entry, Button

import numpy
from PIL import Image, ImageTk
import pytesseract

from constants import *


# Consants
_debug = False


# Tower of Hero Assistant
class TowerOfHeroAssistant(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.item_statistics = list()
        self.cumulative_statistics = list()
        self.list_of_images = list()

        # GUI elements
        self.parent = parent
        self.input_frame = Frame(self)
        self.tree_view_frame = Frame(self)
        self.import_button = None
        self.import_name = None
        self.imports = 0
        self.tree = ttk.Treeview(self.tree_view_frame)
        self.tkinter_gui()

        # Execute Tkinter GUI
        self.parent.mainloop()

    # Initialize the GUI
    def tkinter_gui(self):
        self.input_frame.pack(side=TOP)
        self.tree_view_frame.pack(side=TOP)
        self.pack(side=TOP)

        # Title
        self.parent.title("Tower of Hero Assistant")

        # Icon
        self.parent.iconbitmap(r"C:\Users\Varkalas D`Lonovan\PycharmProjects\Tower-of-Hero\img\toh_assistant_icon.ico")

        # Window Size
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(sticky="nsew")

        # Background Color
        self.parent.config(background="darkgreen")

        # Menu Bar
        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Records from PNG", command=self.get_item_order_and_stats)
        file_menu.add_command(label="Exit", command=self.parent.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Records Import Elements
        import_description = Label(self.input_frame, text="Import Records via PNG Screenshot")
        import_description.grid(column=0, row=0, sticky="w", columnspan=2, padx=4, pady=4)
        import_details = Label(self.input_frame, text="Enter player's name:")
        import_details.grid(column=0, row=1, sticky="e", padx=4, pady=4)
        self.import_name = Entry(self.input_frame)
        self.import_name.grid(column=1, row=1, sticky="nsew", padx=4, pady=4)
        self.import_button = Button(self.input_frame, text="Import", command=self.insert_stats)
        self.import_button.grid(column=0, row=2, sticky="nsew", columnspan=2, padx=4, pady=4)

        # Table
        treeview_style = ttk.Style(self.tree_view_frame)
        treeview_style.configure("Treeview", rowheight=30, background="darkgreen", borderwidth=0)
        treeview_style.configure("Treeview.Heading", foreground="black")
        self.tree.grid(padx=4, pady=4)
        scrollbar = ttk.Scrollbar(self.tree_view_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=2, rowspan=4, sticky="nsew")
        scrollbar.grid(row=0, column=5+self.imports, rowspan=4, sticky="nse", pady=4)
        scrollbar.configure(command=self.tree.yview)

        # Set up the initial columns
        self.tree["columns"] = ("Name", "Tier", "Importance", "Order")
        self.tree.heading("#0", text="Item")
        self.tree.column("#0", anchor=CENTER, minwidth=0, width=60)
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", anchor=W, minwidth=0, width=150)
        self.tree.heading("Tier", text="Tier")
        self.tree.column("Tier", anchor=CENTER, minwidth=0, width=36)
        self.tree.heading("Importance", text="Importance")
        self.tree.column("Importance", anchor=CENTER, minwidth=0, width=80)

        # Go through each item for the row
        index = 0
        for item in GAME_ITEMS:
            # Resize the image
            image = item[1][5:56, 16:69]
            image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

            # Convert from BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert cv2 image to PIL image
            converted_image = Image.fromarray(image)

            # Convert to ImageTk
            self.list_of_images.append(ImageTk.PhotoImage(converted_image))

            # Append the name, tier, and importance
            self.tree.insert("", "end", image=self.list_of_images[index], values=(item[0], item[2], item[3]))
            index += 1

    def get_item_order_and_stats(self, image):
        # Reset the item list
        self.item_statistics = list()

        # Add the titles (Item Name, Tier, Importance, Level, Item Acquisition Order)
        self.item_statistics.append(("Item Name", "Tier", "Importance", "Level", "Item Acquisition Order"))

        # Iterate through the items
        start_time = time()
        for item in GAME_ITEMS:
            # Match the template and if it's >= 80%, run with it
            result = cv2.matchTemplate(image, item[1], cv2.TM_CCOEFF_NORMED)
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
                item_acquisition_order = row_number + (11 * column_number)
                if item_acquisition_order >= 12:
                    item_acquisition_order -= 1

                # Optimize the image for Tesseract OCR to accurately get the numbers
                level_image = image[y:y + height, x:x + width]
                optimized_level_image = cv2.inRange(level_image, numpy.array([200, 200, 200]),
                                                    numpy.array([255, 255, 255]))
                if _debug:
                    cv2.imshow("test", optimized_level_image)
                    cv2.waitKey(0)

                # Optical character recognition
                ocr_image = Image.fromarray(optimized_level_image)
                item_level = pytesseract.image_to_string(ocr_image,
                                                         config="-c tessedit_char_whitelist=0123456789LV -psm 6")
                if item_level is "":
                    messagebox.showerror("Optical Character Recognition Failure",
                                         "Couldn't read the number for the {}. Try lowering the "
                                         "match % for images or changing the config file.".format(item[0]))
                    return None

                # Remove spaces and LV, replace O with 0
                item_level_number_almost = item_level.translate({ord(char): None for char in " LV"})
                item_level_number = item_level_number_almost.translate({ord(char): "0" for char in "O"})

                # Add to the item list (Item name, Tier, Importance, Level, Item Acquisition Order)
                self.item_statistics.append((item[0], item[2], item[3], item_level_number, item_acquisition_order))

                # Print the time it took
                seconds = time() - start_time
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                print("Found %s after %d:%02d:%02d" % (item[0], hours, minutes, seconds))
            else:
                messagebox.showerror("Image Recognition Failure",
                                     "Couldn't see {}. Try lowering the match % for images.".format(item[0]))
                return None

        # Reset the cumulative statistics list
        self.cumulative_statistics = list()

        # Add the titles (Cumulative Stat, Number)
        self.item_statistics.append(("Cumulative Stat", "Number"))

        # Match the template and if it's >= 80%, run with it
        result = cv2.matchTemplate(image, IMG_CUMULATIVE_STATS, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.8:
            # Get the region of the text
            x = 230
            y = max_loc[1]

            for stat in CUMULATIVE_STATS:
                # Grab the images of the text
                if stat == "Coins":
                    image = stat[y + 31:y + 66, x:x + 200]
                elif stat == "Play Time":
                    image = stat[y + 66:y + 99, x:x + 200]
                elif stat == "Summoned Heroes":
                    image = stat[y + 99:y + 130, x:x + 200]
                elif stat == "Top Floor":
                    image = stat[y + 130:y + 165, x:x + 200]
                elif stat == "Acquired Items":
                    image = stat[y + 165:y + 198, x:x + 200]
                elif stat == "New Dungeon":
                    image = stat[y:y + 31, x:x + 200]

                # Optimize the image for Tesseract OCR to accurately get the data
                optimized_image = cv2.inRange(image, numpy.array([200, 200, 200]), numpy.array([255, 255, 255]))
                if _debug:
                    cv2.imshow("test", optimized_image)
                    cv2.waitKey(0)

                # Optical character recognition
                image = Image.fromarray(optimized_image)
                text = ""
                if stat == "Coins":
                    text = pytesseract.image_to_string(image,
                                                       config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzKM -psm 6")
                elif stat == "Play Time":
                    text = pytesseract.image_to_string(image,
                                                       config="-c tessedit_char_whitelist=0123456789: -psm 6")
                elif stat == "Summoned Heroes":
                    text = pytesseract.image_to_string(image,
                                                       config="-c tessedit_char_whitelist=0123456789KM -psm 6")
                elif stat == "Top Floor":
                    text = pytesseract.image_to_string(image,
                                                       config="-c tessedit_char_whitelist=0123456789 -psm 6")
                elif stat == "Acquired Items":
                    text = pytesseract.image_to_string(image,
                                                       config="-c tessedit_char_whitelist=0123456789 -psm 6")
                elif stat == "New Dungeon":
                    text = pytesseract.image_to_string(image,
                                                       config="-c tessedit_char_whitelist=0123456789 -psm 6")
                if text is "":
                    messagebox.showerror("Optical Character Recognition Failure",
                                         "Couldn't read the number for the {}. Try lowering the "
                                         "match % for images or changing the config file.".format(stat))
                # TODO: Convert weird formats to scientific or exponential formats

                # Remove spaces
                final_text = text.translate({ord(char): None for char in " "})

                # Add to the cumulative stats list (Cumulative Stat, Number)
                self.cumulative_statistics.append((stat, final_text))
        else:
            messagebox.showerror("Image Recognition Failure",
                                 "Couldn't see Cumulative. Try lowering the match % for images.")

        return True

    # TODO: Have a button for text save file. And openaskfilename for saving.
    def open_stats_in_default_text_editor(self):
        # Overwrite the temp file
        my_file_name = gettempdir() + "\\tower_of_hero_statistics.txt"
        my_file = open(my_file_name, "w")
        my_file.close()

        # Add the titles (Item Name, Level, Item Acquisition Order)
        with open(my_file_name, "a") as my_file:
            my_file.writelines("Item Name\tLevel\tItem Acquisition Order")

        # Write only the Item Name, Item Level, and Item Aquisition Order
        for game_stat in self.item_statistics:
            with open(my_file_name, "a") as my_file:
                my_file.writelines("%s\t%s\t%d\n" % (game_stat[0], game_stat[3], game_stat[4]))

        # Add a space and then the titles (Cumulative Stat, Number)
        with open("C:\\tmp\\item_location.txt", "a") as my_file:
            my_file.writelines("\n")
            my_file.writelines("%s\t%s\n" % ("Cumulative Stat", "Number"))

        # Write cumulative stats
        for cumulative_stat in self.cumulative_statistics:
            with open("C:\\tmp\\item_location.txt", "a") as my_file:
                my_file.writelines("%s\t%s\n" % (cumulative_stat[0], cumulative_stat[1]))

        # Open the temporary file in the native text editor
        system(my_file_name)

    def insert_stats(self):
        # Error check if the user didn't use a name
        if not self.import_name or self.import_name == "":
            messagebox.showerror("Import Name Missing", "Please enter a name for the data being imported.")

        # Open a file
        filename = filedialog.askopenfilename(initialdir="/", title="Choose a Tower of Hero Records image file.",
                                              filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))
        if not filename:  # If the user cancels
            return None

        image = cv2.imread(filename)
        self.get_item_order_and_stats(image)

        # Create a progress bar
        # TODO: have it have a label and a not be in a stupid position
        progress_window = Toplevel()
        progress_window.wm_title("Progress")
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
        progress_bar["value"] = 0
        progress_bar["maximum"] = 52
        progress_bar.pack()

        # Recreate the table (treeview)
        self.tree["columns"] = ("Name", "Tier", "Importance", "Order", self.import_name)
        self.tree.heading("#0", text="Item")
        self.tree.column("#0", anchor=CENTER, minwidth=0, width=60)
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", anchor=W, minwidth=0, width=150)
        self.tree.heading("Tier", text="Tier")
        self.tree.column("Tier", anchor=CENTER, minwidth=0, width=36)
        self.tree.heading("Importance", text="Importance")
        self.tree.column("Importance", anchor=CENTER, minwidth=0, width=80)
        self.tree.heading(self.import_name, text=self.import_name)
        self.tree.column(self.import_name, anchor=CENTER, minwidth=0, width=80)
        self.tree.grid(row=0, column=2, rowspan=4, sticky="nsew")

        index = 0
        for stat in self.item_statistics:
            # Insert the row (Item name, Tier, Importance, Level, Acquisition number)
            # NOTE: You cannot insert columns in Tkinter
            self.tree.insert("", "end", values=(stat[0], stat[1], stat[2], stat[3], stat[4]))

            index += 1
            progress_bar["value"] += 1
            progress_bar.update()

        self.imports += 1
        progress_bar.stop()
        progress_bar.destroy()  # TODO: Not working
        print("Successfully imported the Records.")

    def delete_column(self):
        selected_column = self.tree.selection()[0]
        self.tree.delete(selected_column)


if __name__ == "__main__":
    root = Tk()
    assistant = TowerOfHeroAssistant(root)
