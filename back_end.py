__author__ = "Theresa De Ocampo"
__version__ = "3.8.2"
__email__ = "maria.theresa.g.de.ocampo@gmail.com"

import sqlite3
from datetime import date
import analysis


def add_resident(fname, mname, lname, gender, occupation, cp, educ, bmonth, bday, byear, house_num, house_street):
    con = sqlite3.connect("barangay.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS resident(
                    residentID         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    residentFname      TEXT NOT NULL,
                    residentMname      TEXT,
                    residentLname      TEXT NOT NULL,
                    residentGender     TEXT NOT NULL,
                    residentOccupation TEXT NOT NULL,
                    residentCellphone  TEXT,
                    residentEduc       TEXT NOT NULL,
                    residentBmonth     TEXT NOT NULL,
                    residentBday       INT  NOT NULL,
                    residentByear      INT  NOT NULL,
                    residentHouseNum   INT  NOT NULL,
                    residentStreet     TEXT NOT NULL
                    )''')
    cur.execute('''INSERT INTO resident (residentFname, residentMname, residentLname, residentGender, 
                                         residentOccupation, residentCellphone, residentEduc, residentBmonth, 
                                         residentBday, residentByear, residentHouseNum, residentStreet) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (fname, mname, lname, gender, occupation, cp, educ, bmonth, bday, byear, house_num, house_street))
    con.commit()
    con.close()


def view_residents():
    con = sqlite3.connect("barangay.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM resident")
    records = cur.fetchall()
    con.commit()
    con.close()
    return records


def delete_resident(target):
    con = sqlite3.connect("barangay.db")
    cur = con.cursor()
    cur.execute("DELETE FROM resident WHERE residentID=?", (target,))
    con.commit()
    con.close()


def search_residents(fname, mname, lname, gender, occupation, cp, educ, bmonth, bday, byear, house_num, house_street):
    if cp == "":
        cp = "optional"
    if mname == "":
        mname = "optional123"
    con = sqlite3.connect("barangay.db")
    cur = con.cursor()
    cur.execute('''SELECT * FROM resident
                   WHERE residentFname=? OR residentMname=? OR residentLname=? OR residentGender=? OR 
                         residentOccupation=? OR residentCellphone=? OR residentEduc=? OR residentBmonth=? OR 
                         residentBday=? OR residentByear=? OR residentHouseNum=? OR residentStreet=?''',
                (fname, mname, lname, gender, occupation, cp, educ, bmonth, bday, byear, house_num, house_street))
    records = cur.fetchall()
    con.commit()
    con.close()
    return records


def update_resident(target, fname="", mname="", lname="", gender="", occupation="", cp="", educ="", bmonth="", bday=0,
                    byear=0, house_num=0, house_street=""):
    con = sqlite3.connect("barangay.db")
    cur = con.cursor()
    cur.execute('''UPDATE resident 
                   SET residentFname=? OR residentMname=? OR residentLname=? OR residentGender=? OR residentOccupation=? 
                       OR residentCellphone=? OR residentEduc=? OR residentBmonth=? OR residentBday=? OR residentByear=? 
                       OR residentHouseNum=? OR residentStreet=?
                   WHERE residentID=?''',
                (fname, mname, lname, gender, occupation, cp, educ, bmonth, bday, byear, house_num, house_street,
                 target))
    con.commit()
    con.close()


def analyze():
    # =============== Initialization =============== #
    population = 0
    male = 0
    female = 0
    youth = 0
    young_adult = 0
    adult = 0
    senior = 0
    unemployed = 0
    employed = 0
    some_elementary = 0
    elementary = 0
    some_high_school = 0
    high_school = 0
    some_college = 0
    bachelor = 0
    vocational = 0
    advance = 0

    # =============== Statistics =============== #
    con = sqlite3.connect("barangay.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM resident")
    records = cur.fetchall()

    for row in records:
        population += 1
        if row[4] == "Male":
            male += 1
        else:
            female += 1

        age = compute_age(row[8], row[9], row[10])
        if age >= 56:
            senior += 1
        elif age >= 36:
            adult += 1
        elif age >= 18:
            young_adult += 1
        else:
            youth += 1

        if age >= 24 and age <= 59:
            if row[5] == "None":
                unemployed += 1
            else:
                employed += 1

        if row[7] == "Some Elementary":
            some_elementary += 1
        elif row[7] == "Elementary Graduate":
            elementary += 1
        elif row[7] == "Some High School":
            some_high_school += 1
        elif row[7] == "High School Graduate":
            high_school += 1
        elif row[7] == "Some College":
            some_college += 1
        elif row[7] == "Bachelor's Degree":
            bachelor += 1
        elif row[7] == "Vocational":
            vocational += 1
        else:
            advance += 1

    educ_tally = [some_elementary, elementary, some_high_school, high_school, some_college, bachelor, vocational,
                  advance]

    analysis.Statistics(population, male, female, youth, young_adult, adult, senior, unemployed, employed, educ_tally)
    ag_tally = [youth, young_adult, adult, senior]
    highest_ag_index = ag_tally.index(max(ag_tally))
    lowest_ag_index = ag_tally.index(min(ag_tally))
    smallest_percent_ag = (min(ag_tally) / (youth + young_adult + adult + senior)) * 100
    unemployed_percent = (unemployed / (unemployed + employed)) * 100
    text_analysis(population, male, female, get_ag_name(highest_ag_index), smallest_percent_ag,
                  get_ag_name(lowest_ag_index), unemployed_percent)


# =============== Helper Functions =============== #
def compute_age(bmonth, bday, byear):
    bmonth = parse_month(bmonth)
    today = date.today()
    return today.year - byear - ((today.month, today.day) < (bmonth, bday))


def parse_month(month_str):
    months = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    return months.get(month_str, 0)


def get_ag_name(i):
    if i == 0:
        return "youths (< 18 years old)"
    elif i == 1:
        return "young adults (18 to 35 years old)"
    elif i == 2:
        return "adults (36 to 45 years old)"
    else:
        return "seniors (56 & up)"


def text_analysis(population, male, female, highest_ag, smallest_percent_ag, smallest_ag, unemployed_percent):
    width = 70
    print("╔══════════════════════════════════════╗".center(width))
    print("║      Barangay Profiling System       ║".center(width))
    print("║  Dulao, Bago City, Negros Occidental ║".center(width))
    print("╚══════════════════════════════════════╝".center(width))
    print("\nThe total number of residents In Barangay Dulao is {0}, {1} of which are male,".format(population, male))
    print("and {0} are female. Most of the residents are {1}.".format(female, highest_ag))
    print("A small percentage of {0:.2f}% are {1}.".format(smallest_percent_ag, smallest_ag))

    if unemployed_percent <= 50:
        print("Lastly, {0:.2f}% of the population are unemployed".format(unemployed_percent))
    else:
        print("\nThere is a growing number of unemployed residents, and the unit is currently")
        print("coming up with a strategy to bring this number down.")
