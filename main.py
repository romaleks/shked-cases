from requests import request
from sqlalchemy import create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request

from parser_csgo import Case 

engine = create_engine('sqlite:///kentofariki.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__, template_folder="templates")
    
@app.route('/', methods=["GET", "POST"])
def hello_world():
    d = {}
    cases = session.query(Case).all()
    for case in cases:
        d[case.name] = case.icon_url
    return render_template("index.html", mydict=d)
 
if __name__ == '__main__':
    app.run()