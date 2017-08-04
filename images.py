from tkinter import messagebox

from cv2 import cv2

PAT_IMAGES = "img\\"


def image_reader(image_name):
    full_name = PAT_IMAGES + image_name
    read_image = cv2.imread(full_name)
    if read_image is None:
        messagebox.showerror("Incorrect File Name", "{} could not be read.".format(full_name))
    return read_image


# TODO: Import this shit
IMG_GAME_STATS = image_reader("game_stats.png")
IMG_CUMULATIVE_STATS = image_reader("cumulative_statistics.png")

IMG_A_KINGS_CROWN = image_reader("a_king's_crown.png")
IMG_AEGIS = image_reader("aegis.png")
IMG_AWAKENING_ARMOR = image_reader("awakening_armor.png")
IMG_AWAKENING_ARMOR_PLUS_1 = image_reader("awakening_sword_plus_1.png")
IMG_AWAKENING_SWORD = image_reader("awakening_sword.png")
IMG_AWAKENING_SWORD_PLUS_1 = image_reader("awakening_armor_plus_1.png")
IMG_BLACK_ESSENCE = image_reader("black_essence.png")
IMG_BLUE_ELIXIR = image_reader("blue_elixir.png")
IMG_CADUCEUS = image_reader("caduceus.png")
IMG_CLAYMORE = image_reader("claymore.png")
IMG_COAT_OF_GOLD = image_reader("coat_of_gold.png")
IMG_DARK_BOOTS = image_reader("dark_boots.png")
IMG_DARK_GATE = image_reader("dark_gate.png")
IMG_DARK_KNIGHT_ARMOR = image_reader("dark_knight_armor.png")
IMG_DEMON_EYE = image_reader("demon_eye.png")
IMG_DURANDAL = image_reader("durandal.png")
IMG_EARTH_ARMOR = image_reader("earth_armor.png")
IMG_EXCALIBUR = image_reader("excalibur.png")
IMG_FIRE_SWORD = image_reader("fire_sword.png")
IMG_FLAMBERGE = image_reader("flamberge.png")
IMG_FLAME_POT = image_reader("flame_pot.png")
IMG_FREYRS_SWORD = image_reader("freyr's_sword.png")
IMG_FULL_HELMET = image_reader("full_helmet.png")
IMG_FULL_PLATE = image_reader("full_plate.png")
IMG_GAE_BOLG = image_reader("gae_bolg.png")
IMG_GATE = image_reader("gate.png")
IMG_GOLD_BOX = image_reader("gold_box.png")
IMG_GOLD_VESSELS = image_reader("gold_vessels.png")
IMG_GOLDEN_GLOVES = image_reader("golden_gloves.png")
IMG_GOLDEN_POT = image_reader("golden_pot.png")
IMG_GOLDEN_ROD = image_reader("golden_rod.png")
IMG_GREEN_ELIXIR = image_reader("green_elixir.png")
IMG_GUILD_HAT = image_reader("guild_hat.png")
IMG_GUNGNIR = image_reader("gungnir.png")
IMG_HALBERD = image_reader("halberd.png")
IMG_HYDRAS_POISON_ARROWS = image_reader("hydra's_poison_arrows.png")
IMG_ICE_POT = image_reader("ice_pot.png")
IMG_LAEVATEINN = image_reader("laevateinn.png")
IMG_LANCE = image_reader("lance.png")
IMG_MAGIC_LAMP = image_reader("magic_lamp.png")
IMG_MISTILTEINN = image_reader("mistilteinn.png")
IMG_MITHRIL_ARMOUR = image_reader("mithril_armor.png")
IMG_MITHRIL_SWORD = image_reader("mithril_sword.png")
IMG_MJOLNIR = image_reader("mjolnir.png")
IMG_PHILOSOPHERS_STONE = image_reader("philosopher's_stone.png")
IMG_RAPIER = image_reader("rapier.png")
IMG_RED_ELIXIR = image_reader("red_elixir.png")
IMG_SOLOMONS_KEY = image_reader("solomon's_key.png")
IMG_SOLOMONS_STAFF = image_reader("solomons_staff.png")
IMG_SUMMONING_LETTER = image_reader("summoning_letter.png")
IMG_TOMAHAWK = image_reader("tomahawk.png")
IMG_TRAINING_BOOK = image_reader("training_book.png")
IMG_WING_BOOTS = image_reader("wing_boots.png")
