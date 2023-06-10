from flask import Flask, render_template, request
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
    BC1 = chiefs.get("BC001")
    BC2 = chiefs.get("BC002")
    BC3 = chiefs.get("BC003")
    BC4 = chiefs.get("BC004")
    BC5 = chiefs.get("BC005")
    BC6 = chiefs.get("BC006")
    BC7 = chiefs.get("BC007")
    BC8 = chiefs.get("BC008")
    BC9 = chiefs.get("BC009")
    BC10 = chiefs.get("BC010")
    BC11 = chiefs.get("BC011")
    BC20 = chiefs.get("BC020")
    BCAC = chiefs.get("AC001")
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
        BC1=BC1,
        BC2=BC2,
        BC3=BC3,
        BC4=BC4,
        BC5=BC5,
        BC6=BC6,
        BC7=BC7,
        BC8=BC8,
        BC9=BC9,
        BC10=BC10,
        BC11=BC11,
        BC20=BC20,
        BCAC=BCAC,
        SHIFT=shift
    )

@app.route('/<date>/<arg>')
def specific_date(date:str, arg:str):
    data= main(arg.upper(), date=date)
    render_template('basic.html', DATA=data)
    
@app.route("/<arg>")
def general (arg:str):
    data = main(arg.upper())
    return render_template("basic.html", DATA=data)

@app.route("/detailed")
def detailed_personnel():
    detailed = main("DETAILED")
    return render_template("detailed.html", DETAILED=detailed)

@app.route("/comp")
def compliment():
    detailed = main("COMP")
    return render_template("compliment.html", DATA=detailed)


@app.route("/assignments", methods=["GET", "POST"])
def assignment():
    detailed = main("PPL")
    search_terms = []
    if request.method == 'POST': 
        search_terms = request.form['search'].split(',')
    return render_template("assignments.html", data=detailed, search_terms=search_terms)

@app.route('/tailwind')
def tailwind_index():
    return render_template('test_index.html')

    

if __name__ == "__main__":
    app.run(debug=True, port=4000)