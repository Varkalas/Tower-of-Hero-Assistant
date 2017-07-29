import math

import numpy
from PIL import Image
import pytesseract

from images import *


GAME_ITEMS = [("A King's Crown", IMG_A_KINGS_CROWN),
              ("Aegis", IMG_AEGIS),
              ("Awakening Armor", IMG_AWAKENING_ARMOR),
              ("Awakening Armor +1", IMG_AWAKENING_ARMOR_PLUS_1),
              ("Awakening Sword", IMG_AWAKENING_SWORD),
              ("Awakening Sword +1", IMG_AWAKENING_SWORD_PLUS_1),
              ("Black Essence", IMG_BLACK_ESSENCE),
              ("Blue Elixir", IMG_BLUE_ELIXIR),
              ("Caduceus", IMG_CADUCEUS),
              ("Claymore", IMG_CLAYMORE),
              ("Coat of Gold", IMG_COAT_OF_GOLD),
              ("Dark Boots", IMG_DARK_BOOTS),
              ("Dark Gate", IMG_DARK_GATE),
              ("Dark Knight Armor", IMG_DARK_KNIGHT_ARMOR),
              ("Demon Eye", IMG_DEMON_EYE),
              ("Durandal", IMG_DURANDAL),
              ("Earth Armor", IMG_EARTH_ARMOR),
              ("Excalibur", IMG_EXCALIBUR),
              ("Fire Sword", IMG_FIRE_SWORD),
              ("Flamberge", IMG_FLAMBERGE),
              ("Flame Pot", IMG_FLAME_POT),
              ("Freyr's Sword", IMG_FREYRS_SWORD),
              ("Full Helmet", IMG_FULL_HELMET),
              ("Full Plate", IMG_FULL_PLATE),
              ("Gae Bolg", IMG_GAE_BOLG),
              ("Gate", IMG_GATE),
              ("Gold Box", IMG_GOLD_BOX),
              ("Gold Vessels", IMG_GOLD_VESSELS),
              ("Golden Gloves", IMG_GOLDEN_GLOVES),
              ("Golden Rod", IMG_GOLDEN_ROD),
              ("Golden Pot", IMG_GOLDEN_POT),
              ("Green Elixir", IMG_GREEN_ELIXIR),
              ("Guild Hat", IMG_GUILD_HAT),
              ("Gungnir", IMG_GUNGNIR),
              ("Halberd", IMG_HALBERD),
              ("Hydra's Poison Arrows", IMG_HYDRAS_POISON_ARROWS),
              ("Ice Pot", IMG_ICE_POT),
              ("Lævateinn", IMG_LAEVATEINN),
              ("Lance", IMG_LANCE),
              ("Magic Lamp", IMG_MAGIC_LAMP),
              ("Mistilteinn", IMG_MISTILTEINN),
              ("Mithril Armour", IMG_MITHRIL_ARMOUR),
              ("Mithril Sword", IMG_MITHRIL_SWORD),
              ("Mjolnir", IMG_MJOLNIR),
              ("Philosopher's Stone", IMG_PHILOSOPHERS_STONE),
              ("Rapier", IMG_RAPIER),
              ("Red Elixir", IMG_RED_ELIXIR),
              ("Solomon's Key", IMG_SOLOMONS_KEY),
              ("Solomon's Staff", IMG_SOLOMONS_STAFF),
              ("Summoning Letter", IMG_SUMMONING_LETTER),
              ("Tomahawk", IMG_TOMAHAWK),
              ("Training Book", IMG_TRAINING_BOOK),
              ("Wing Boots", IMG_WING_BOOTS)]


if __name__ == "__main__":
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
