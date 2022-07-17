# from requests import request
# from sqlalchemy import create_engine, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Date, Boolean
# from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request
from sqlalchemy import case
from website import create_app, db, models, chances_csgo

import re
pattern_skin = r"(★?[a-zA-Z0-9- ]* \| [a-zA-Z0-9- ]*)"
pattern_float = r"(\([a-zA-Z- ]*\))"

app = create_app()

  
@app.route("/")
def home():
    loh = False
    if loh:
        from website import parser_csgo
        

    data_cases = {}
    cases = db.session.query(models.Case).all()
    for case in cases:
        data_cases[case.id] = [case.name, case.icon_url]


    last_items = db.session.query(models.User_info).order_by(models.User_info.opened_at.desc()).limit(15)
    data_drop = {}

    for last_item in last_items:

        item = re.findall(pattern_skin, last_item.item)[0]
        weapon = item.split("|")[0]
        skin = item.split("|")[1]
        quality = re.findall(pattern_float, last_item.item)[0]
        last_item_row = db.session.query(models.CSGO_Item).filter(models.CSGO_Item.name==item and models.CSGO_Item.quality==quality).first()
        url = last_item_row.icon_url
        rarity = last_item_row.rarity
        id = last_item.id
        data_drop[id] = [weapon, skin, url, rarity]

    return render_template("index.html", mydict=data_cases, drop=data_drop)


@app.route("/case/<usercase>")
def case_items(usercase):
    current_case = db.session.query(models.Case).filter(models.Case.id==usercase).first()
    name_list = current_case.name.split()
    name_list.remove("Case")
    name = " ".join(name_list)
    data_case = {name: current_case.icon_url}


    case_items = db.session.query(models.CSGO_Item).filter(models.CSGO_Item.case==current_case.name).order_by(models.CSGO_Item.priority)
    data_case_items = {}
    for item in case_items:
        weapon = item.name.split("|")[0]
        skin = item.name.split("|")[1]
        url = item.icon_url
        rarity = item.rarity
        data_case_items[weapon] = [skin, url, rarity]


    last_items = db.session.query(models.User_info).order_by(models.User_info.opened_at.desc()).limit(15)
    data_drop = {}

    for last_item in last_items:

        item = re.findall(pattern_skin, last_item.item)[0]
        weapon = item.split("|")[0]
        skin = item.split("|")[1]
        quality = re.findall(pattern_float, last_item.item)[0]
        last_item_row = db.session.query(models.CSGO_Item).filter(models.CSGO_Item.name==item and models.CSGO_Item.quality==quality).first()
        url = last_item_row.icon_url
        rarity = last_item_row.rarity
        id = last_item.id
        data_drop[id] = [weapon, skin, url, rarity]


    return render_template("case.html", mydict=data_case_items, case=data_case, drop=data_drop)


if __name__ == '__main__':
    app.run()