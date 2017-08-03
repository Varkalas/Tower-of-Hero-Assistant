# Tower of Hero Assitant
A tool to assist in data gathering for Tower of Hero.

# Implemented Features
* Finds where each item is in Records (OpenCV)
    - Currently only tested for 1080x1920, haven't tested lower resolutions
* Grabs the level of each item via optimal character recognition (Tesseract)
* Writes the item name, level, and acquisition order to a file with tab spacing in between
* A tree view that shows the item, name, tier, and importance 

# To-Do List
* Acquire the Cumulative statistics by OCRing that word and then gathering the data underneath
* Don't be stupid and change to modular class form
* Improve the GUI
    - Add the scrollbar
    - Make it look less stupid
* Ability to add other people's Records: append a column with their name at the top
    - Browse files, prompt enter name edit box, and match % (default is 80% for 1080x1920)
    - Use color coding to indicate best stats
        - Is this possible with ttk?
* Save functionality
* Export to Excel/OpenOffice
* Copy to clipboard?
* Add Tower of Hero icon
* Make into a standalone executable using pip installer
