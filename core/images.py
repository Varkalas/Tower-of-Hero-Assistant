from definitions import ROOT_DIR
from tkinter import messagebox
from cv2 import imread


IMAGE_PATH = ROOT_DIR + "\\images\\"


def read_image(image_name):
    full_name = IMAGE_PATH + image_name
    the_image = imread(full_name)
    if the_image is None:
        messagebox.showerror("Incorrect File Name", "{} could not be read.".format(full_name))
    return the_image


IMG_CUMULATIVE_STATS = read_image("cumulative_statistics.png")

IMG_A_KINGS_CROWN = read_image("a_king's_crown.png")
IMG_AEGIS = read_image("aegis.png")
IMG_AWAKENING_ARMOR = read_image("awakening_armor.png")
IMG_AWAKENING_ARMOR_PLUS_1 = read_image("awakening_sword_plus_1.png")
IMG_AWAKENING_SWORD = read_image("awakening_sword.png")
IMG_AWAKENING_SWORD_PLUS_1 = read_image("awakening_armor_plus_1.png")
IMG_BLACK_ESSENCE = read_image("black_essence.png")
IMG_BLUE_CRYSTAL = read_image("blue_crystal.png")
IMG_BLUE_ELIXIR = read_image("blue_elixir.png")
IMG_CADUCEUS = read_image("caduceus.png")
IMG_CLAYMORE = read_image("claymore.png")
IMG_COAT_OF_GOLD = read_image("coat_of_gold.png")
IMG_DARK_BOOTS = read_image("dark_boots.png")
IMG_DARK_GATE = read_image("dark_gate.png")
IMG_DARK_KNIGHT_ARMOR = read_image("dark_knight_armor.png")
IMG_DEMON_EYE = read_image("demon_eye.png")
IMG_DURANDAL = read_image("durandal.png")
IMG_EARTH_ARMOR = read_image("earth_armor.png")
IMG_EXCALIBUR = read_image("excalibur.png")
IMG_FIRE_SWORD = read_image("fire_sword.png")
IMG_FLAMBERGE = read_image("flamberge.png")
IMG_FLAME_POT = read_image("flame_pot.png")
IMG_FREYRS_SWORD = read_image("freyr's_sword.png")
IMG_FULL_HELMET = read_image("full_helmet.png")
IMG_FULL_PLATE = read_image("full_plate.png")
IMG_GAE_BOLG = read_image("gae_bolg.png")
IMG_GATE = read_image("gate.png")
IMG_GOLD_BOX = read_image("gold_box.png")
IMG_GOLD_VESSELS = read_image("gold_vessels.png")
IMG_GOLDEN_GLOVES = read_image("golden_gloves.png")
IMG_GOLDEN_POT = read_image("golden_pot.png")
IMG_GOLDEN_ROD = read_image("golden_rod.png")
IMG_GREEN_ELIXIR = read_image("green_elixir.png")
IMG_GUILD_HAT = read_image("guild_hat.png")
IMG_GUNGNIR = read_image("gungnir.png")
IMG_HALBERD = read_image("halberd.png")
IMG_HYDRAS_POISON_ARROWS = read_image("hydra's_poison_arrows.png")
IMG_ICE_POT = read_image("ice_pot.png")
IMG_LAEVATEINN = read_image("laevateinn.png")
IMG_LANCE = read_image("lance.png")
IMG_MAGIC_LAMP = read_image("magic_lamp.png")
IMG_MISTILTEINN = read_image("mistilteinn.png")
IMG_MITHRIL_ARMOUR = read_image("mithril_armor.png")
IMG_MITHRIL_SWORD = read_image("mithril_sword.png")
IMG_MJOLNIR = read_image("mjolnir.png")
IMG_PHILOSOPHERS_STONE = read_image("philosopher's_stone.png")
IMG_RAPIER = read_image("rapier.png")
IMG_RED_ELIXIR = read_image("red_elixir.png")
IMG_RED_HAND = read_image("red_hand.png")
IMG_SOLOMONS_KEY = read_image("solomon's_key.png")
IMG_SOLOMONS_STAFF = read_image("solomons_staff.png")
IMG_SUMMONING_LETTER = read_image("summoning_letter.png")
IMG_TOMAHAWK = read_image("tomahawk.png")
IMG_TRAINING_BOOK = read_image("training_book.png")
IMG_VETERANS_HAT = read_image("veteran's_hat.png")
IMG_WING_BOOTS = read_image("wing_boots.png")
