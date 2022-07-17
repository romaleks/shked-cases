from urllib import response
import requests
import re
from sqlalchemy import create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker
import datetime


from .models import Case, CSGO_Item, User_info
from . import db


# engine = create_engine('sqlite:///kentofariki.db?check_same_thread=False')
# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     email = Column(String, unique = True)
#     password = Column(String)

# class User_price(Base):
#     __tablename__ = 'user_price'
#     id = Column(Integer, primary_key=True)
#     user = Column(String)
#     price = Column(Integer)

# class User_info(Base):
#     __tablename__ = 'user_info'
#     id = Column(Integer, primary_key=True)
#     user = Column(String)
#     item = Column(String)
#     opened_at = Column(DateTime)

# class Case(Base):
#     __tablename__ = 'case'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     icon_url = Column(String)

# class CSGO_Item(Base):
#     __tablename__ = 'csgo_items'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     rarity = Column(String)
#     quality = Column(String)
#     stattrak = Column(Boolean)
#     case = Column(String, default="No collection")
#     icon_url = Column(String)
#     price = Column(Integer)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

pattern = r"(★?[a-zA-Z0-9- ]* \| [a-zA-Z0-9- ]*) (\([a-zA-Z- ]*\))"
pattern_skin = r"(★?[a-zA-Z0-9- ]* \| [a-zA-Z0-9- ]*)"
pattern_float = r"(\([a-zA-Z- ]*\))"
image_url = "http://cdn.steamcommunity.com/economy/image/"
currency = 57.62


case_skins = {
    "CS:GO Weapon Case 2": ['Tec-9 | Blue Titanium', 'M4A1-S | Blood Tiger', 'FAMAS | Hexane', 'P250 | Hive', 'SCAR-20 | Crimson Web', 'Five-SeveN | Case Hardened', 'MP9 | Hypnotic', 'Nova | Graphite', 'Dual Berettas | Hemoglobin', 'P90 | Cold Blooded', 'USP-S | Serum', 'SSG 08 | Blood in the Water'],
    "CS:GO Weapon Case 3": ['CZ75-Auto | Crimson Web', 'P2000 | Red FragCam', 'Dual Berettas | Panther', 'USP-S | Stainless', 'Glock-18 | Blue Fissure', 'CZ75-Auto | Tread Plate', 'Tec-9 | Titanium Bit', 'Desert Eagle | Heirloom', 'Five-SeveN | Copper Galaxy', 'CZ75-Auto | The Fuschia Is Now', 'P250 | Undertow', 'CZ75-Auto | Victoria'],
    "Chroma 2 Case": ['AK-47 | Elite Build', 'MP7 | Armor Core', 'Desert Eagle | Bronze Deco', 'P250 | Valence', "Negev | Man-o'-war", 'Sawed-Off | Origami', 'AWP | Worm God', 'MAG-7 | Heat', 'CZ75-Auto | Pole Position', 'UMP-45 | Grand Prix', 'Five-SeveN | Monkey Business', 'Galil AR | Eco', 'FAMAS | Djinn', 'M4A1-S | Hyper Beast', 'MAC-10 | Neon Rider'],
    "Clutch Case": ['PP-Bizon | Night Riot', 'Five-SeveN | Flame Test', 'MP9 | Black Sand', 'P2000 | Urban Hazard', 'R8 Revolver | Grip', 'SG 553 | Aloha', 'XM1014 | Oxide Blaze', 'Glock-18 | Moonrise', 'Negev | Lionfish', 'Nova | Wild Six', 'MAG-7 | SWAG-7', 'UMP-45 | Arctic Wolf', 'AUG | Stymphalian', 'AWP | Mortis', 'USP-S | Cortex', 'M4A4 | Neo-Noir', 'MP7 | Bloodsport'],
    "Danger Zone Case": ['MP9 | Modest Threat', 'Glock-18 | Oxide Blaze', 'Nova | Wood Fired', 'M4A4 | Magnesium', 'Sawed-Off | Black Sand', 'SG 553 | Danger Close', 'Tec-9 | Fubar', 'G3SG1 | Scavenger', 'Galil AR | Signal', 'MAC-10 | Pipe Down', 'P250 | Nevermore', 'USP-S | Flashback', 'UMP-45 | Momentum', 'Desert Eagle | Mecha Industries', 'MP5-SD | Phosphor', 'AK-47 | Asiimov', 'AWP | Neo-Noir'],
    "Gamma Case": ['Five-SeveN | Violent Daimyo', 'MAC-10 | Carnivore', 'Nova | Exo', 'P250 | Iron Clad', 'PP-Bizon | Harvester', 'SG 553 | Aerial', 'Tec-9 | Ice Cap', 'AUG | Aristocrat', 'AWP | Phobos', 'P90 | Chopper', 'R8 Revolver | Reboot', 'Sawed-Off | Limelight', 'M4A4 | Desolate Space', 'P2000 | Imperial Dragon', 'SCAR-20 | Bloodsport', 'Glock-18 | Wasteland Rebel', 'M4A1-S | Mecha Industries'],
    "Operation Vanguard Weapon Case": ['G3SG1 | Murky', 'MAG-7 | Firestarter', 'MP9 | Dart', 'Five-SeveN | Urban Hazard', 'UMP-45 | Delusion', 'Glock-18 | Grinder', 'M4A1-S | Basilisk', 'M4A4 | Griffin', 'Sawed-Off | Highwayman', 'P250 | Cartel', 'SCAR-20 | Cardiac', 'XM1014 | Tranquility', 'AK-47 | Wasteland Rebel', 'P2000 | Fire Elemental'],
    "CS20 Case": ['Dual Berettas | Elite 1.6', 'Tec-9 | Flash Out', 'MAC-10 | Classic Crate', 'MAG-7 | Popdog', 'SCAR-20 | Assault', 'FAMAS | Decommissioned', 'Glock-18 | Sacrifice', 'M249 | Aztec', 'MP5-SD | Agent', 'Five-SeveN | Buddy', 'P250 | Inferno', 'UMP-45 | Plastique', 'MP9 | Hydra', 'P90 | Nostalgia', 'AUG | Death by Puppy', 'AWP | Wildfire', 'FAMAS | Commemoration'],
    "CS:GO Weapon Case": ['MP7 | Skulls', 'AUG | Wings', 'SG 553 | Ultraviolet', 'Glock-18 | Dragon Tattoo', 'USP-S | Dark Water', 'M4A1-S | Dark Water', 'AK-47 | Case Hardened', 'Desert Eagle | Hypnotic', 'AWP | Lightning Strike'],
    "Chroma 3 Case": ['Dual Berettas | Ventilators', 'G3SG1 | Orange Crash', 'M249 | Spectre', 'MP9 | Bioleak', 'P2000 | Oceanic', 'Sawed-Off | Fubar', 'SG 553 | Atlas', 'CZ75-Auto | Red Astor', 'Galil AR | Firefight', 'SSG 08 | Ghost Crusader', 'Tec-9 | Re-Entry', 'XM1014 | Black Tie', 'AUG | Fleet Flock', 'P250 | Asiimov', 'UMP-45 | Primal Saber', 'PP-Bizon | Judgement of Anubis', "M4A1-S | Chantico's Fire"],
    "Chroma Case": ['Glock-18 | Catacombs', 'M249 | System Lock', 'MP9 | Deadly Poison', 'SCAR-20 | Grotto', 'XM1014 | Quicksilver', 'Dual Berettas | Urban Shock', 'Desert Eagle | Naga', 'MAC-10 | Malachite', 'Sawed-Off | Serenity', 'AK-47 | Cartel', 'M4A4 | 龍王 (Dragon King)', 'P250 | Muertos', "AWP | Man-o'-war", 'Galil AR | Chatterbox'],
    "Dreams & Nightmares Case": ['Five-SeveN | Scrawl', 'MAC-10 | Ensnared', 'MAG-7 | Foresight', 'MP5-SD | Necro Jr.', 'P2000 | Lifted Spirits', 'SCAR-20 | Poultrygeist', 'Sawed-Off | Spirit Board', 'PP-Bizon | Space Cat', 'G3SG1 | Dream Glade', 'M4A1-S | Night Terror', 'XM1014 | Zombie Offensive', 'USP-S | Ticket to Hell', 'Dual Berettas | Melondrama', 'FAMAS | Rapid Eye Movement', 'MP7 | Abyssal Apparition', 'AK-47 | Nightwish', 'MP9 | Starlight Protector'],
    "Falchion Case": ['Galil AR | Rocket Pop', 'Glock-18 | Bunsen Burner', 'Nova | Ranger', 'P90 | Elite Build', 'UMP-45 | Riot', 'USP-S | Torque', 'FAMAS | Neural Net', 'M4A4 | Evil Daimyo', 'MP9 | Ruby Poison Dart', 'Negev | Loudmouth', 'P2000 | Handgun', 'CZ75-Auto | Yellow Jacket', 'MP7 | Nemesis', 'SG 553 | Cyrex', 'AK-47 | Aquamarine Revenge', 'AWP | Hyper Beast'],
    "Fracture Case": ['Negev | Ultralight', 'P2000 | Gnarled', "SG 553 | Ol' Rusty", 'SSG 08 | Mainframe 001', 'P250 | Cassette', 'P90 | Freight', 'PP-Bizon | Runic', 'MAG-7 | Monster Call', 'Tec-9 | Brother', 'MAC-10 | Allure', 'Galil AR | Connexion', 'MP5-SD | Kitbash', 'M4A4 | Tooth Fairy', 'Glock-18 | Vogue', 'XM1014 | Entombed', 'Desert Eagle | Printstream', 'AK-47 | Legion of Anubis'],
    "Gamma 2 Case": ['CZ75-Auto | Imprint', 'Five-SeveN | Scumbria', 'G3SG1 | Ventilator', 'Negev | Dazzle', 'P90 | Grim', 'UMP-45 | Briefing', 'XM1014 | Slipstream', 'Desert Eagle | Directive', 'Glock-18 | Weasel', 'MAG-7 | Petroglyph', 'SCAR-20 | Powercore', 'SG 553 | Triarch', 'AUG | Syd Mead', 'MP9 | Airlock', 'Tec-9 | Fuel Injector', 'AK-47 | Neon Revolution', 'FAMAS | Roll Cage'],
    "Glove Case": ['CZ75-Auto | Polymer', 'Glock-18 | Ironwork', 'MP7 | Cirrus', 'Galil AR | Black Sand', 'MP9 | Sand Scale', 'MAG-7 | Sonar', 'P2000 | Turf', 'Dual Berettas | Royal Consorts', 'G3SG1 | Stinger', 'M4A1-S | Flashback', 'Nova | Gila', 'USP-S | Cyrex', 'FAMAS | Mecha Industries', 'P90 | Shallow Grave', 'Sawed-Off | Wasteland Princess', 'SSG 08 | Dragonfire', 'M4A4 | Buzz Kill'],
    "Horizon Case": ['AUG | Amber Slipstream', 'Dual Berettas | Shred', 'Glock-18 | Warhawk', 'MP9 | Capillary', 'P90 | Traction', 'R8 Revolver | Survivalist', 'Tec-9 | Snek-9', 'CZ75-Auto | Eco', 'G3SG1 | High Seas', 'Nova | Toy Soldier', 'AWP | PAW', 'MP7 | Powercore', 'M4A1-S | Nightmare', 'Sawed-Off | Devourer', 'FAMAS | Eye of Athena', 'AK-47 | Neon Rider', 'Desert Eagle | Code Red'],
    "Huntsman Weapon Case": ['Tec-9 | Isaac', 'SSG 08 | Slashed', 'Galil AR | Kami', 'CZ75-Auto | Twist', 'P90 | Module', 'P2000 | Pulse', 'AUG | Torque', 'PP-Bizon | Antique', 'XM1014 | Heaven Guard', 'MAC-10 | Tatter', 'M4A1-S | Atomic Alloy', 'SCAR-20 | Cyrex', 'USP-S | Caiman', 'AK-47 | Vulcan', 'M4A4 | Desert-Strike'],
    "Operation Bravo Case": ['SG 553 | Wave Spray', 'Dual Berettas | Black Limba', 'Nova | Tempest', 'Galil AR | Shattered', 'UMP-45 | Bone Pile', 'G3SG1 | Demeter', 'USP-S | Overgrowth', 'M4A4 | Zirka', 'MAC-10 | Graven', 'M4A1-S | Bright Water', 'P90 | Emerald Dragon', 'P2000 | Ocean Foam', 'AWP | Graphite', 'AK-47 | Fire Serpent', 'Desert Eagle | Golden Koi'],
    "Operation Breakout Weapon Case": ['MP7 | Urban Hazard', 'Negev | Desert-Strike', 'P2000 | Ivory', 'SSG 08 | Abyss', 'UMP-45 | Labyrinth', 'PP-Bizon | Osiris', 'CZ75-Auto | Tigris', 'Nova | Koi', 'P250 | Supernova', 'Desert Eagle | Conspiracy', 'Five-SeveN | Fowl Play', 'Glock-18 | Water Elemental', 'P90 | Asiimov', 'M4A1-S | Cyrex'],
    "Operation Broken Fang Case": ['CZ75-Auto | Vendetta', 'P90 | Cocoa Rampage', 'G3SG1 | Digital Mesh', 'Galil AR | Vandal', 'P250 | Contaminant', 'M249 | Deep Relief', 'MP5-SD | Condition Zero', 'AWP | Exoskeleton', 'Dual Berettas | Dezastre', 'Nova | Clear Polymer', 'SSG 08 | Parallax', 'UMP-45 | Gold Bismuth', 'Five-SeveN | Fairy Tale', 'M4A4 | Cyber Security', 'USP-S | Monster Mashup', 'M4A1-S | Printstream', 'Glock-18 | Neo-Noir'],
    "Operation Hydra Case": ['USP-S | Blueprint', 'FAMAS | Macabre', 'M4A1-S | Briefing', 'MAC-10 | Aloha', 'MAG-7 | Hard Water', 'Tec-9 | Cut Out', 'UMP-45 | Metal Flowers', 'AK-47 | Orbit Mk01', 'P2000 | Woodsman', 'P250 | Red Rock', 'P90 | Death Grip', "SSG 08 | Death's Head", 'Dual Berettas | Cobra Strike', 'Galil AR | Sugar Rush', 'M4A4 | Hellfire', 'Five-SeveN | Hyper Beast', 'AWP | Oni Taiji'],
    "Operation Phoenix Weapon Case": ['UMP-45 | Corporal', 'Negev | Terrain', 'Tec-9 | Sandstorm', 'MAG-7 | Heaven Guard', 'MAC-10 | Heat', 'SG 553 | Pulse', 'FAMAS | Sergeant', 'USP-S | Guardian', 'AK-47 | Redline', 'P90 | Trigon', 'Nova | Antique', 'AWP | Asiimov', 'AUG | Chameleon'],
    "Operation Wildfire Case": ['PP-Bizon | Photic Zone', 'Dual Berettas | Cartel', 'MAC-10 | Lapis Gator', 'SSG 08 | Necropos', 'Tec-9 | Jambiya', 'USP-S | Lead Conduit', 'FAMAS | Valence', 'Five-SeveN | Triumvirate', 'Glock-18 | Royal Legion', 'MAG-7 | Praetorian', 'MP7 | Impire', 'AWP | Elite Build', 'Desert Eagle | Kumicho Dragon', 'Nova | Hyper Beast', 'AK-47 | Fuel Injector', 'M4A4 | The Battlestar'],
    "Prisma 2 Case": ['AUG | Tom Cat', 'AWP | Capillary', 'CZ75-Auto | Distressed', 'Desert Eagle | Blue Ply', 'MP5-SD | Desert Strike', 'Negev | Prototype', 'R8 Revolver | Bone Forged', 'P2000 | Acid Etched', 'Sawed-Off | Apocalypto', 'SCAR-20 | Enforcer', 'SG 553 | Darkwing', 'SSG 08 | Fever Dream', 'AK-47 | Phantom Disruptor', 'MAC-10 | Disco Tech', 'MAG-7 | Justice', 'M4A1-S | Player Two', 'Glock-18 | Bullet Queen'],
    "Prisma Case": ['FAMAS | Crypsis', 'AK-47 | Uncharted', 'MAC-10 | Whitefish', 'Galil AR | Akoben', 'MP7 | Mischief', 'P250 | Verdigris', 'P90 | Off World', 'AWP | Atheris', 'Tec-9 | Bamboozle', 'Desert Eagle | Light Rail', 'MP5-SD | Gauss', 'UMP-45 | Moonrise', 'R8 Revolver | Skull Crusher', 'AUG | Momentum', 'XM1014 | Incinegator', 'Five-SeveN | Angry Mob', 'M4A4 | The Emperor'],
    "Revolver Case": ['R8 Revolver | Crimson Web', 'AUG | Ricochet', 'Desert Eagle | Corinthian', 'P2000 | Imperial', 'Sawed-Off | Yorick', 'SCAR-20 | Outbreak', 'PP-Bizon | Fuel Rod', 'Five-SeveN | Retrobution', 'Negev | Power Loader', 'SG 553 | Tiger Moth', 'Tec-9 | Avalanche', 'XM1014 | Teclu Burner', 'AK-47 | Point Disarray', 'G3SG1 | The Executioner', 'P90 | Shapewood', 'M4A4 | Royal Paladin', 'R8 Revolver | Fade'],
    "Shadow Case": ['Dual Berettas | Dualing Dragons', 'FAMAS | Survivor Z', 'Glock-18 | Wraiths', 'MAC-10 | Rangeen', 'MAG-7 | Cobalt Core', 'SCAR-20 | Green Marine', 'XM1014 | Scumbria', 'Galil AR | Stone Cold', 'M249 | Nebula Crusader', 'MP7 | Special Delivery', 'P250 | Wingshot', 'AK-47 | Frontside Misty', 'G3SG1 | Flux', 'SSG 08 | Big Iron', 'M4A1-S | Golden Coil', 'USP-S | Kill Confirmed'],
    "Shattered Web Case": ['MP5-SD | Acid Wash', 'Nova | Plume', 'G3SG1 | Black Sand', 'R8 Revolver | Memento', 'Dual Berettas | Balance', 'SCAR-20 | Torn', 'M249 | Warbird', 'PP-Bizon | Embargo', 'AK-47 | Rat Rod', 'AUG | Arctic Wolf', 'MP7 | Neon Ply', 'P2000 | Obsidian', 'Tec-9 | Decimator', 'SG 553 | Colony IV', 'SSG 08 | Bloodshot', 'AWP | Containment Breach', 'MAC-10 | Stalker'],
    "Snakebite Case": ['SG 553 | Heavy Metal', 'Glock-18 | Clear Polymer', 'M249 | O.S.I.P.R.', 'CZ75-Auto | Circaetus', 'UMP-45 | Oscillator', 'R8 Revolver | Junk Yard', 'Nova | Windblown', 'P250 | Cyber Shell', 'Negev | dev_texture', 'MAC-10 | Button Masher', 'Desert Eagle | Trigger Discipline', 'AK-47 | Slate', 'MP9 | Food Chain', 'XM1014 | XOXO', 'Galil AR | Chromatic Aberration', 'USP-S | The Traitor', 'M4A4 | In Living Color'],
    "Spectrum 2 Case": ['Sawed-Off | Morris', 'AUG | Triqua', 'G3SG1 | Hunter', 'Glock-18 | Off World', 'MAC-10 | Oceanic', 'Tec-9 | Cracked Opal', 'SCAR-20 | Jungle Slipstream', 'MP9 | Goo', 'SG 553 | Phantom', 'CZ75-Auto | Tacticat', 'UMP-45 | Exposure', 'XM1014 | Ziggy', 'PP-Bizon | High Roller', 'M4A1-S | Leaded Glass', 'R8 Revolver | Llama Cannon', 'AK-47 | The Empress', 'P250 | See Ya Later'],
    "Spectrum Case": ['PP-Bizon | Jungle Slipstream', 'SCAR-20 | Blueprint', 'Desert Eagle | Oxide Blaze', 'Five-SeveN | Capillary', 'MP7 | Akoben', 'P250 | Ripple', 'Sawed-Off | Zander', 'Galil AR | Crimson Tsunami', 'M249 | Emerald Poison Dart', 'MAC-10 | Last Dive', 'UMP-45 | Scaffold', 'XM1014 | Seasons', 'AWP | Fever Dream', 'CZ75-Auto | Xiangliu', 'M4A1-S | Decimator', 'AK-47 | Bloodsport', 'USP-S | Neo-Noir'],
    "Winter Offensive Weapon Case": ['Galil AR | Sandstorm', 'Five-SeveN | Kami', 'M249 | Magma', 'PP-Bizon | Cobalt Halftone', 'FAMAS | Pulse', 'Dual Berettas | Marina', 'MP9 | Rose Iron', 'Nova | Rising Skull', 'M4A1-S | Guardian', 'P250 | Mehndi', 'AWP | Redline', 'M4A4 | Asiimov', 'Sawed-Off | The Kraken'],
    "eSports 2013 Case": ['M4A4 | Faded Zebra', 'MAG-7 | Memento', 'FAMAS | Doomkitty', 'Galil AR | Orange DDPAT', 'Sawed-Off | Orange DDPAT', 'P250 | Splash', 'AK-47 | Red Laminate', 'AWP | BOOM', 'P90 | Death by Kitty'],
    "eSports 2013 Winter Case": ['Galil AR | Blue Titanium', 'Five-SeveN | Nightshade', 'PP-Bizon | Water Sigil', 'Nova | Ghost Camo', 'G3SG1 | Azure Zebra', 'P250 | Steel Disruption', 'AK-47 | Blue Laminate', 'P90 | Blind Spot', 'FAMAS | Afterimage', 'AWP | Electric Hive', 'Desert Eagle | Cobalt Disruption', 'M4A4 | X-Ray'],
    "eSports 2014 Summer Case": ['SSG 08 | Dark Water', 'MAC-10 | Ultraviolet', 'USP-S | Blood Tiger', 'CZ75-Auto | Hexane', 'Negev | Bratatat', 'XM1014 | Red Python', 'PP-Bizon | Blue Streak', 'P90 | Virus', 'MP7 | Ocean Foam', 'Glock-18 | Steel Disruption', 'Desert Eagle | Crimson Web', 'AUG | Bengal Tiger', 'Nova | Bloomstick', 'AWP | Corticera', 'P2000 | Corticera', 'M4A4 | Bullet Rain', 'AK-47 | Jaguar'],
    "Recoil Case": ['FAMAS | Meow 36', 'Galil AR | Destroyer', 'M4A4 | Poly Mag', 'MAC-10 | Monkeyflage', 'Negev | Drop Me', 'UMP-45 | Roadblock', 'Glock-18 | Winterized', 'R8 Revolver | Crazy 8', 'M249 | Downtown', 'SG 553 | Dragon Tech', 'P90 | Vent Rush', 'Dual Berettas | Flora Carnivora', 'AK-47 | Ice Coaled', 'P250 | Visions', 'Sawed-Off | Kiss♥Love', 'USP-S | Printstream', 'AWP | Chromatic Aberration']
}
rarity_priority = { "Consumer Grade": 0,"Industrial Grade": 1,"Mil-Spec Grade": 2,"Restricted": 3,"Classified": 4,"Covert": 5 }


# def get_case(skin):
#     case_url = f"https://steamcommunity.com/market/listings/730/{skin}/render?start=0&count=1&currency=3&language=english&format=json"
#     r = requests.get(case_url)
#     d = r.json()
#     items = []
#     if d: 
#         if d["assets"]:
#             descriptions = d["assets"]["730"]["2"][list(d["assets"]["730"]["2"].keys())[0]]["descriptions"]
#             for description in descriptions:
#                 if re.findall(pattern_skin, description["value"]):
#                     items.append(description["value"])
#     return items


def get_case(skin):
    for key, value in case_skins.items():
        if skin in value:
            return key
    return None


response = requests.get("http://csgobackpack.net/api/GetItemsList/v2/")
data = response.json()
items_list = list(data["items_list"].keys())
for key in items_list:
    if data["items_list"][key]["type"] == "Weapon":

        skin = re.findall(pattern_skin, key)
        if skin:
            name = skin[0]
            quality = re.findall(pattern_float, key)[0]
        else:
            name = key
            quality = None

        case = get_case(name.rstrip())
        if not case:
            if data["items_list"][key]["weapon_type"] == "Knife":
                case = "Knife"
            else:
                case = "Some Collection"

        rarity = data["items_list"][key]["rarity"]
        if rarity in rarity_priority.keys():
            priority = rarity_priority[rarity]
        else:
            priority = -1
        icon_url = image_url + data["items_list"][key]["icon_url"]

        try:
            price = int(data["items_list"][key]["price"][
                list(data["items_list"][key]["price"].keys())[0]
            ]["average"] * currency)
        except:
            price = 0

        if "stattrak" in list(data["items_list"][key].keys()):
            stattrak = True
        else:
            stattrak = False

        row = CSGO_Item(name=name, rarity=rarity, quality=quality, stattrak=stattrak, case=case, icon_url=icon_url, price=price, priority=priority)
        db.session.add(row)

        continue

    elif data["items_list"][key]["type"] == "Container" and "Case" in key.split():

        icon_url = image_url + data["items_list"][key]["icon_url"]
        row = Case(name=key, icon_url=icon_url)
        db.session.add(row)

    else:
        continue


db.session.commit()