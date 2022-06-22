from urllib import response
import requests
import re
from sqlalchemy import create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///kentofariki.db?check_same_thread=False')
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return '''<Item(username={username},
                     email={email},
                     password={password}>'''\
            .format(username=self.username,
                    email=self.email, password=self.password)

class User_price(Base):
    __tablename__ = 'user_price'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    price = Column(Integer)

    def __repr__(self):
        return '''<Item(user={user},
                     price={price}>'''\
            .format(user=self.user,
                    price=self.price)

class User_info(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    item = Column(String)
    opened_at = Column(DateTime)

    def __repr__(self):
        return '''<Item(user={user},
                     item={item},
                     opened_at={opened_at}>'''\
            .format(user=self.user,
                    item=self.item,
                    opened_at=self.opened_at)

class Case(Base):
    __tablename__ = 'case'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_url = Column(String)

    def __repr__(self):
        return '''<Item(name={name}, icon_url={icon_url}>'''\
            .format(name=self.name, icon_url=self.icon_url)

class CSGO_Item(Base):
    __tablename__ = 'csgo_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rarity = Column(String)
    quality = Column(String)
    stattrak = Column(Boolean)
    case = Column(String, default="No collection")
    icon_url = Column(String)
    price = Column(Integer)

    def __repr__(self):
        return '''<Item(name={name},
                     rarity={rarity},
                     quality={quality},
                     stattrak={stattrak},
                     case={case},
                     price={price}>'''\
            .format(name=self.name,
                    rarity=self.rarity,
                    quality=self.quality,
                    stattrak = self.stattrak,
                    case=self.case, price=self.price)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

pattern = r"(★?[a-zA-Z0-9- ]* \| [a-zA-Z0-9- ]*) (\([a-zA-Z- ]*\))"
pattern_skin = r"(★?[a-zA-Z0-9- ]* \| [a-zA-Z0-9- ]*)"
pattern_float = r"(\([a-zA-Z- ]*\))"
image_url = "http://cdn.steamcommunity.com/economy/image/" #собираем ссылку для иконки предмета
currency = 57.62 #курс доллара


# def get_case(skin):
#     case_url = f"https://steamcommunity.com/market/listings/730/{skin}/render?start=0&count=1&currency=3&language=english"
#     r = requests.get(case_url)
#     d = r.json()
#     if d: 
#         try:
#             descriptions = d["assets"]["730"]["2"][list(d["assets"]["730"]["2"].keys())[0]]["descriptions"]
#             for description in descriptions:
#                 if "Collection" in description["value"] and "Case" in description["value"]:
#                     c = " ".join(description["value"].split()[:len(description["value"].split()) - 1])
#                     break
#                 elif "Case" in description["value"]:
#                     c = description["value"]
#                     break
#                 elif "Collection" in description["value"]:
#                     c = " ".join(description["value"].split()[:len(description["value"].split()) - 1]) + " Case"
#                     break
#         except:
#             c = None
#             print(d)
#             print(skin)
#     else:
#         c = None
#     return c


response = requests.get("http://csgobackpack.net/api/GetItemsList/v2/")
data = response.json()
items_list = list(data["items_list"].keys())
for key in items_list:
    if data["items_list"][key]["type"] == "Weapon":

        case = "LOL"

        skin = re.findall(pattern_skin, key)
        if skin:
            name = skin[0]
            quality = re.findall(pattern_float, key)[0]
        else:
            name = key
            quality = None

        rarity = data["items_list"][key]["rarity"]
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

        row = CSGO_Item(name=name, rarity=rarity, quality=quality, stattrak=stattrak, case=case, icon_url=icon_url, price=price)
        session.add(row)

    elif data["items_list"][key]["type"] == "Container" and "Case" in key.split():

        icon_url = image_url + data["items_list"][key]["icon_url"]
        row = Case(name=key, icon_url=icon_url)
        session.add(row)

    else:
        continue
session.commit()