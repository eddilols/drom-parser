# This is a sample Python script.
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
import time
import json
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

def tableParsing(src):


    soup = BeautifulSoup(src, "html.parser")
    h1 = soup.find("h1").text.strip().replace("- технические характеристики","")

    table = soup.find('table', class_="b-table b-table_mobile-size-s b-table_text-left")
    rows = table.find_all("tr")

    catList = {}
    catList["Авто"]=h1
    for index, row in enumerate(rows):
        td = row.find_all("td")

        if len(td) == 1:
            catTitle = td[0].text.strip()
            catList[catTitle] = {}

        else:
            title = td[0].text.strip()
            text = td[1]
            if "#yes" in str(text):
                param = True
            elif "span" in str(text):
                param = False
            else:
                tmp = text.text.strip()
                if "   " in tmp:
                    param = tmp.split("   ", 1)[0]

                else:
                    param = text.text.strip()

            catList[catTitle][title]=param

    return jsonify(catList)



def getHtml(url):
    headers = {
        "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers)

    return r.text

@app.route("/car", methods=["GET"])
def getlist():
    url = request.args.get("url")
    print(url)
    data = getHtml(url)
    json = tableParsing(data)

    return url



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
