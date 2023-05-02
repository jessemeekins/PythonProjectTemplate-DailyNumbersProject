from flask import Flask, render_template, url_for
from main_project_folder import *
from main_project_folder.report_type import (
    ComplimentReport, FullRosterReport
)

from main_project_folder.main import main
battalion_dict = ComplimentReport.BATTALION_DICT


app = Flask(__name__)

@app.route("/full")
def home():
    full = main("FULL")
    return render_template("home.html", DATA=full)

@app.route("/")
@app.route('/numbers')
def daily_numbers():
    als_companies = main("ALS")
    chiefs = main("CHIEFS")
    paycodes = main("PAYCODES")
    compliment = main("COMP")
    off_by_rank = main("RANK")
    shift = main("SHIFT")
   
    div1 = chiefs.get("DC001")
    div2 = chiefs.get("DC002")
    companies = list()
    for batt in als_companies.values():
        for company in batt:
            companies.append(company)
    return render_template(
        'main.html', 
        BATTALION_DICT=battalion_dict,
        NUMBER_OF_ALS=len(companies),
        OFF_BY_RANK=off_by_rank,
        COMPLIMENT=compliment,
        PAYCODES=paycodes,
        ALS=companies, 
        CHIEFS=chiefs,
        DIV1=div1,
        DIV2=div2,
        SHIFT=shift
    )


@app.route("/<arg>")
def general (arg:str):
    data = main(arg.upper())
    return render_template("basic.html", DATA=data)

@app.route("/detailed")
def detailed_personnel():
    detailed = main("DETAILED")
    return render_template("detailed.html", DETAILED=detailed)

    

if __name__ == "__main__":
    app.run(debug=True, port=3000)