# Tower of Hero Assitant
A tool to assist in data gathering for Tower of Hero.

# Implemented Features
* New and improved progress bar
* Finds where each item is in Records (OpenCV)
    - Currently only tested for 1080x1920, haven't tested lower resolutions
* Grabs the level of each item via optimal character recognition (Tesseract)
* Writes the item name, level, and acquisition order to a file with tab spacing in between
* A GUI that shows the item, name, tier, and importance
* Cumulative statistics OCR
* Coins and Summoned Heroes are displayed in scientific notation

# To-Do List
* Ability to add Records columns
    - Browse files, prompt enter name edit box, and match % (default is 80% for 1080x1920)
    - Use color coding to indicate best stats
        - Is this possible with ttk?
* Save functionality
* Export to Excel/OpenOffice
* Copy to clipboard?
* Change the Cumulative statistics to be an intelligible format (standard math)
* Make into a standalone executable using pip installer
* Ability to remove Records columns
* Implement with wxWidgets and give an option on which GUI to select upon loading
    - Try other GUIs like QT and GTK?
