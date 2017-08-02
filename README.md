# Tower-of-Hero
A tool to assist in data gathering for Tower of Hero. Current only supports 1080x1920 and with ads at the top of the Records tab.

# To-Do List
* Acquire the Cumulative statistics by OCRing that word and then gathering the data underneath
* GUI
    - Tkinter: tree view
        - Put images of the items in the list (modify display of current pictures?)
    - Add other people's Records: append a column with their name at the top
        - Browse files, enter name edit box, and match % (default is 80% for 1080x1920)
        - Add options for image manipulation?
    - Put corfe83's tier in the table
    - Put my importance level in the table
    - Save functionality
    - Export to Excel
    - Copy to clipboard?
    - Add Tower of Hero icon
* Make into a standalone executable using pip installer
* Adjust for different resolutions
    - Need to modify max_val threshold based on resolution
    - Need to come up with another way of checking text below located images

# Implemented Features
* Finds where each item is in Records (OpenCV)
    - Currently only tested for 1080x1920, haven't tested lower resolutions
* Grabs the level of each item via optimal character recognition (Tesseract)
* Writes the item name, level, and acquisition order to a file with tab spacing in between 
