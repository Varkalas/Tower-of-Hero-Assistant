from decimal import Decimal
from os import system
from math import floor
from re import findall
from tempfile import gettempdir
from time import time
from tkinter import Toplevel, Frame, Tk, ttk, CENTER, TOP, W, filedialog, Menu, Label, Entry, Button, StringVar, messagebox

import cv2
import numpy
from PIL import Image, ImageTk
import pytesseract

from core.constants import GAME_ITEMS, CUMULATIVE_STATS, MATH_NOTATION
from core.images import *
from definitions import ROOT_DIR


_debug = False
IMPORT_NAME = 0
IMPORT_ITEM_STATISTICS = 0
IMPORT_CUMULATIVE_STATISTICS = 0


class TowerOfHeroGUI(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.list_of_imports = list()        # Name1, TupleOfStats1, Name2, TupleOfStats2, etc.
        self.item_statistics = list()
        self.cumulative_statistics = list()
        self.list_of_images = list()

        # GUI elements
        self.parent = parent
        self.input_frame = Frame(self)
        self.tree_view_frame = Frame(self)
        self.import_button = None
        self.import_name = StringVar()
        self.tree = ttk.Treeview(self.tree_view_frame)
        self.progress_window = None
        self.progress_bar = None
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
        self.parent.iconbitmap(ROOT_DIR + "\\images\\toh_assistant_icon.ico")

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
        # TODO: Add saving
        # TODO: Memory leak

        # Records Import Elements
        import_description = Label(self.input_frame, text="Import Records via PNG Screenshot")
        import_description.grid(column=0, row=0, sticky="w", columnspan=2, padx=4, pady=4)
        import_details = Label(self.input_frame, text="Enter player's name:")
        import_details.grid(column=0, row=1, sticky="e", padx=4, pady=4)
        import_name_box = Entry(self.input_frame, textvariable=self.import_name)
        import_name_box.grid(column=1, row=1, sticky="nsew", padx=4, pady=4)
        # TODO: Checkbox for showing the image to confirm the results
        # TODO: Checkbox for opening Notepad document
        # TODO: Checkbox for displaying found results
        self.import_name.set("")
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
        scrollbar.grid(row=0, column=5+len(self.list_of_imports), rowspan=4, sticky="nse", pady=4)
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

        # Move to center
        self.parent.withdraw()  # Hide it immediately
        self.parent.update_idletasks()  # Then hold on drawing the window
        x = (self.parent.winfo_screenwidth() - self.parent.winfo_reqwidth()) / 2
        y = (self.parent.winfo_screenheight() - self.parent.winfo_reqheight()) / 2
        self.parent.geometry("+%d+%d" % (x, y))
        self.parent.deiconify()  # Draw the window immediately

        # Create a progress bar
        self.progress_window = Toplevel()
        sub_x = x + self.parent.winfo_reqwidth() / 4
        sub_y = y + self.parent.winfo_reqheight() / 2
        self.progress_window.geometry("+%d+%d" % (sub_x, sub_y))
        # self.progress_window.wm_title("Progress")
        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=200, mode="determinate")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 60  # 61 total: 54 items, 6 stats, 1 total line
        self.progress_window.withdraw()
        self.progress_window.update_idletasks()

        self.make_the_treeview()

    def make_the_treeview(self):
        # Reset the treeview
        self.tree.delete(*self.tree.get_children())

        # Put the header -- Name, Tier, Importance, Username1 (Item Level), Username1 (Order Acquired), etc.
        header = list()
        header.append("Name")
        header.append("Tier (corfe83)")
        header.append("Rank (Varkalas)")
        for users in self.list_of_imports:
            header.append(users[0])
        self.tree["columns"] = header
        # TODO: Do I need this? self.tree.heading("Importance", text="Importance")
        # TODO: Do I need this? self.tree.column("Importance", anchor=CENTER, minwidth=0, width=80)

        # Make the rows for the items
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

            # Append the name, tier, importance, and each import's item data
            value_list = list()
            value_list.append(item[0])
            value_list.append(item[2])
            value_list.append(item[3])
            for users in self.list_of_imports:               # (String, List, List) = (Username, list of tuples of item stats, list of tuples of cumulative stats)
                for items in users[IMPORT_ITEM_STATISTICS]:  # (Item name, Tier, Importance, Level, Item Acquisition Order)
                    if item[0] == items[0]:
                        value_list.append(items[3])  # User's item level
                        # TODO: Include item acquisition order only if it's the primary character
                        value_list.append(items[4])  # User's item acquisition order

            self.tree.insert("", "end", image=self.list_of_images[index], values=value_list)
            if self.import_name.get() != "":
                self.tree.column(self.import_name.get(), anchor=CENTER, minwidth=0, width=80)
            self.tree.grid(row=0, column=2, rowspan=4, sticky="nsew")  # TODO: Adjust rowspan?

            # Append the user data
            for user_stats in self.list_of_imports:
                self.tree.insert("", "end", )

            # Make the rows for the cumulative statistics
            index += 1

    def get_item_order_and_stats(self, image):
        # Check if a name is inputted
        if self.import_name.get() == "":
            messagebox.showerror("Import Name Missing", "Please enter a name for the data being imported.")

        # Reset the lists
        self.item_statistics = list()
        self.cumulative_statistics = list()

        # Add the titles (Item Name, Tier, Importance, Level, Item Acquisition Order)
        self.item_statistics.append(("Item Name", "Tier", "Importance", "Level", "Item Acquisition Order"))

        # Start the progress bar
        self.progress_bar.pack()
        self.progress_window.update()
        self.progress_window.deiconify()

        # Iterate through the items
        total_levels = 0
        start_time = time()
        for item in GAME_ITEMS:
            # Match the template and if it's >= 80%, run with it
            result = cv2.matchTemplate(image, item[1], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= 0.7:
                # Get the region of the text
                x = max_loc[0] - 2
                y = max_loc[1] + 51
                width = 95
                height = 24

                # Find the location of the item to get the item acquisition order
                row_number = floor((max_loc[0] - 34) / 92) + 1
                column_number = floor((max_loc[1] - 1150) / 80)
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

                # Add to the total levels
                total_levels += int(item_level_number)

                # Add to the item list (Item name, Tier, Importance, Level, Item Acquisition Order)
                self.item_statistics.append((item[0], item[2], item[3], item_level_number, item_acquisition_order))

                # Update the progress bar
                self.progress_bar["value"] += 1
                self.progress_bar.update()

                # Print the time it took
                seconds = time() - start_time
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                print("Found %s (%s) after %d:%02d:%02d" % (item[0], item_level_number, hours, minutes, seconds))
            else:
                print("ERROR: Couldn't see %s. Either the item doesn't exist or the image is of too poor quality." % item[0])
                self.item_statistics.append((item[0], item[2], item[3], "?", "?"))

        # Add the total
        item_acquisition_order = len(self.item_statistics) + 1
        self.item_statistics.append(("Total", "N/A", "N/A", str(total_levels), item_acquisition_order))
        self.progress_bar["value"] += 1
        self.progress_bar.update()

        # Reset the cumulative statistics list
        self.cumulative_statistics = list()

        # Add the titles (Cumulative Stat, Number)
        self.cumulative_statistics.append(("Cumulative Stat", "-", "-", "Number", "Order"))

        # Match the template and if it's >= 80%, run with it
        result = cv2.matchTemplate(image, IMG_CUMULATIVE_STATS, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.8:
            # Get the region of the text
            y = max_loc[1]  # Pixel 718 for 1920x1080

            for stat in CUMULATIVE_STATS:
                # Grab the images of the text
                if stat == "Coins":
                    number_image = image[y + 31:y + 66, 270:490]
                elif stat == "Play Time":
                    number_image = image[y + 66:y + 99, 270:490]
                elif stat == "Summoned Heroes":
                    number_image = image[y + 99:y + 130, 348:490]
                elif stat == "Top Floor":
                    number_image = image[y + 130:y + 165, 370:490]
                elif stat == "Acquired Items":
                    number_image = image[y + 165:y + 198, 440:490]
                elif stat == "New Dungeon":
                    number_image = image[y + 198:y + 231, 380:490]
                else:
                    number_image = None

                # Optimize the image for Tesseract OCR to accurately get the data
                optimized_image_binary = cv2.inRange(number_image, numpy.array([200, 200, 200]), numpy.array([255, 255, 255]))
                optimized_image = cv2.resize(optimized_image_binary, (0, 0), fx=2.0, fy=2.0)
                if True:
                    cv2.imshow("test", optimized_image)
                    cv2.waitKey(0)

                # Optical character recognition
                ocr_image = Image.fromarray(optimized_image)
                text = ""
                if stat == "Coins":
                    text = pytesseract.image_to_string(ocr_image,
                                                       config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzKM -psm 6")
                elif stat == "Play Time":
                    text = pytesseract.image_to_string(ocr_image,
                                                       config="-c tessedit_char_whitelist=0123456789: -psm 7")
                    # TODO: If after one colon, we over 3 digits, add a colon before the third/etc. digit
                elif stat == "Summoned Heroes":
                    text = pytesseract.image_to_string(ocr_image,
                                                       config="-c tessedit_char_whitelist=0123456789KM -psm 6")
                elif stat == "Top Floor":
                    text = pytesseract.image_to_string(ocr_image,
                                                       config="-c tessedit_char_whitelist=0123456789 -psm 6")
                elif stat == "Acquired Items":
                    text = pytesseract.image_to_string(ocr_image,
                                                       config="-c tessedit_char_whitelist=0123456789 -psm 6")
                elif stat == "New Dungeon":
                    text = pytesseract.image_to_string(ocr_image,
                                                       config="-c tessedit_char_whitelist=0123456789 -psm 6")
                if text is "":
                    messagebox.showerror("Optical Character Recognition Failure",
                                         "Couldn't read the number for the {}. Try lowering the "
                                         "match % for images or changing the config file.".format(stat))

                # Remove spaces
                final_text = text.translate({ord(char): None for char in " "})
                seconds = time() - start_time
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                print("Found %s (%s) after %d:%02d:%02d" % (stat, final_text, hours, minutes, seconds))

                # Convert the character format to scientific
                if stat == "Coins" or stat == "Summoned Heroes":
                    '''
                    So each letter increment adds 10^3.
                    K = 1 (10^3)
                    M = 2 (10^6)
                    B = 3 (10^9)
                    T = 4 (10^12)
                    a = 5 (10^15)
                    ...
                    z = 30 (10^90)
                    aa = 31 (10^93)
                    ab = 32 (10^96)
                    ...
                    az = 56 (10^168)
                    ba = 57 (10^171)

                    So 100ab200aa would be 100 * 1096 + 200 * 1093 or 100.2 * 1096 (1.002E98 in scientific notation)
                    '''
                    original_text = final_text

                    # Check if the format is less than or greater than 1 million
                    incremental_format_first_letters = findall(r"\d+([a-zA-Z]+)\d+[a-zA-Z]", final_text)
                    if incremental_format_first_letters:
                        incremental_format_first_letters = findall(r"\d+([a-zA-Z]+)\d+[a-zA-Z]+", final_text)[0]  # > million
                        incremental_format_second_letters = findall(r"\d+[a-zA-Z]+\d+([a-zA-Z]+)", final_text)[0]
                    else:
                        incremental_format_first_letters = findall(r"\d+([a-zA-Z]+)\d+", final_text)[0]
                        incremental_format_second_letters = ""

                    # Format: __K__ (under one million)
                    if incremental_format_first_letters == "K":
                        alphabetic_notation = int(findall(r"(\d+)[a-zA-Z]+\d+", final_text)[0]) * 1000 + int(findall(r"\d+[a-zA-Z]+(\d+)", final_text)[0])
                        final_text = "%.3E" % Decimal(str(alphabetic_notation))
                    # Format: __a__b (only one letter)
                    elif incremental_format_first_letters in MATH_NOTATION and incremental_format_second_letters in MATH_NOTATION:
                        # formula = 10^(3*(x+1))
                        first_letter_multiplier = 10 ** (3 * (MATH_NOTATION.index(incremental_format_first_letters) + 1))
                        second_letter_multiplier = 10 ** (3 * (MATH_NOTATION.index(incremental_format_second_letters) + 1))
                        alphabetic_notation = int(
                            findall(r"(\d+)[a-zA-Z]+\d+[a-zA-Z]+", final_text)[0]) * first_letter_multiplier + int(
                            findall(r"\d+[a-zA-Z]+(\d+)[a-zA-Z]+", final_text)[0]) * second_letter_multiplier
                        final_text = "%.3E" % Decimal(str(alphabetic_notation))
                    # Format: __ab__aa (two letters)
                    elif len(incremental_format_first_letters) > 1 and len(incremental_format_second_letters) > 1:
                        # formula = 10^(3 * (26*(x-3) + 5) + (3*(y-4)))
                        first_letter_multiplier = 10 ** (3 * ((26 * (MATH_NOTATION.index(incremental_format_first_letters[0]) - 3)) + 5)
                                                         + (3 * (MATH_NOTATION.index(incremental_format_first_letters[1]) - 4)))

                        second_letter_multiplier = 10 ** (3 * ((26 * (MATH_NOTATION.index(incremental_format_second_letters[0]) - 3)) + 5)
                                                          + (3 * (MATH_NOTATION.index(incremental_format_second_letters[1]) - 4)))
                        alphabetic_notation = int(
                            findall(r"(\d+)[a-zA-Z]+\d+[a-zA-Z]+", final_text)[0]) * first_letter_multiplier + int(
                            findall(r"\d+[a-zA-Z]+(\d+)[a-zA-Z]+", final_text)[0]) * second_letter_multiplier
                        final_text = "%.3E" % Decimal(str(alphabetic_notation))
                    # Error
                    else:
                        messagebox.showerror("Calculation Failure",
                                             "Unable to calculate the scientific notation of " + stat + ". Using the alphabetic notation instead.")
                    print("[%s] Changed %s to %s after %d:%02d:%02d" % (stat, original_text, final_text, hours, minutes, seconds))

                # Add to the cumulative stats list (Cumulative Stat, Tier, Importance, Number, Item Acquisition Order)
                item_acquisition_order += 1
                self.cumulative_statistics.append((stat, "N/A", "N/A", final_text, item_acquisition_order))

                # Update the progress bar
                self.progress_bar["value"] += 1
                self.progress_bar.update()

                # Print the time it took
                seconds = time() - start_time
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                print("Found %s after %d:%02d:%02d" % (final_text, hours, minutes, seconds))
        else:
            messagebox.showerror("Image Recognition Failure",
                                 "Couldn't see Cumulative. Try lowering the match % for images.")

        # Add the imported stats
        # Note: Since each item is a column, we do the name and then a tuple of the stats
        self.list_of_imports.append(self.import_name.get())
        self.list_of_imports.append((self.item_statistics, self.cumulative_statistics))

        # Stop the progress bar
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_window.withdraw()

        self.open_stats_in_default_text_editor()

        return True

    # TODO: Have a button for text save file. And openaskfilename for saving.
    def open_stats_in_default_text_editor(self):
        # Overwrite the temp file
        my_file_name = gettempdir() + "\\tower_of_hero_statistics.txt"
        my_file = open(my_file_name, "w")
        my_file.close()

        # Write only the Item Name, Item Level, and Item Aquisition Order
        for game_stat in self.item_statistics:
            with open(my_file_name, "a") as my_file:
                my_file.writelines("%s\t%s\t%s\n" % (game_stat[0], game_stat[3], game_stat[4]))

        with open(my_file_name, "a") as my_file:
            my_file.writelines("\n")

        # Write cumulative stats
        for cumulative_stat in self.cumulative_statistics:
            with open(my_file_name, "a") as my_file:
                my_file.writelines("%s\t%s\t%s\n" % (cumulative_stat[0], cumulative_stat[3], cumulative_stat[4]))

        # Open the temporary file in the native text editor
        system(my_file_name)

    def insert_stats(self):
        # Error check if the user didn't use a name
        if self.import_name.get() is None or self.import_name.get() == "":
            messagebox.showerror("Import Name Missing", "Please enter a name for the data being imported.")
            return None

        # Open a file
        filename = filedialog.askopenfilename(initialdir="/", title="Choose a Tower of Hero Records image file.",
                                              filetypes=[("JPG Files", "*.jpg")])
        if not filename:  # If the user cancels
            return None

        image = cv2.imread(filename)
        self.get_item_order_and_stats(image)

        # Recreate the table (treeview)
        self.make_the_treeview()

        print("Successfully imported the Records.")

    # TODO
    def delete_column(self):
        selected_column = self.tree.selection()[0]
        self.tree.delete(selected_column)


if __name__ == "__main__":
    root = Tk()
    assistant = TowerOfHeroGUI(root)
