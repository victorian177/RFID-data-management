import sys
sys.path.append("C:/Users/Victor Momodu/Documents/Programming/Arduino/Code/RFID-data-management")

from flask import Flask, render_template, request
import purpose
import json

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template("landing_page.html")

@app.route('/new')
def new():
    return render_template("new.html", use_cases=["Access", "Attendance", "Record"])

@app.route('/existing')
def existing():
    return render_template("existing.html")

@app.route('/data', methods=["GET", "POST"])
def data():
    try:
        use_case = request.form["use_case"]
        form_data = request.form["data"]
    except KeyError:
        facility = request.form["facility"]
        result = facility_data_findr(facility, existing=True)
        if result[facility][:5] == "Error":
            return render_template("error.html", error=result[facility])
        else:
            instance = purpose_pickr(facility, result[facility])
            dataframe = instance.data
            return render_template("data.html", facility=facility, use_case=result[facility], dataframe=dataframe)
    else:       
        facility = request.form["facility"]
        result = facility_data_findr(facility, use_case=use_case)
        if result[facility][:5] == "Error":
            return render_template("error.html", error=result[facility])
        else:
            instance = purpose_pickr(facility, result[facility], form_data.splitlines())
            dataframe = instance.data
            return render_template("data.html", facility=facility, use_case=result[facility], dataframe=dataframe)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/remove')
def remove():
    return render_template("remove.html")

@app.route('/run')
def run():
  return render_template("run.html")

def facility_data_findr(name, use_case="", existing=False):
    if existing:
        try:
            with open("facility_data.json", 'r') as facility_file:
                facility_data = json.load(facility_file)
        except FileNotFoundError:
            with open("facility_data.json", 'w') as facility_file:
                return {name: "Error: no instance of this facility exists in our database. Database is empty."}
        else:
            try:
                facility_data[name]
            except KeyError:
                return {name: "Error: no instance of this facility exists in our database. Ensure name is correct."}
            else:
                return {name: facility_data[name]}
    else:
        try:
            with open("facility_data.json", 'r') as facility_file:
                facility_data = json.load(facility_file)
        except FileNotFoundError:
            with open("facility_data.json", 'w') as facility_file:
                facility_data = {name: use_case}
                json.dump(facility_data, facility_file)
            return facility_data
        else:
            try:
                facility_data[name]
            except KeyError:
                facility_data[name] = use_case
                with open("facility_data.json", 'w') as facility_file:
                    json.dump(facility_data, facility_file)
            else:
                return {name: "Error: instance of this facililty exists in our database. Try using another name."}

def purpose_pickr(name, use_case, data=None):
    TYPES = {
        's': "obj",
        'i': "int",
        'c': "cat"
    }

    info = {}
    cat_info = {}
    if data != None:
        if use_case == 'Access':
            places = data[-1]
            data = data[:-1]
        for i in data:
            fields = i.split(": ")[-1]
            for j in fields.split(", "):
                if TYPES[i.split(": ")[0]] == 'c':
                    cat_info[j.split('|')[0]] = j.split('|')[1:]
                    info[j.split('|')[0]] = TYPES[i.split(": ")[0]]
                else:
                    info[j] = TYPES[i.split(": ")[0]]

        if use_case == "Access":
            return purpose.Access(name, info=info, cat_info=cat_info, places=places)
        elif use_case == "Attendance":
            return purpose.Attendance(name, info=info, cat_info=cat_info)
        elif use_case == "Record":
            return purpose.Record(name, info=info, cat_info=cat_info)

    else:
        if use_case == "Access":
            return purpose.Access(name)
        elif use_case == "Attendance":
            return purpose.Attendance(name)
        elif use_case == "Record":
            return purpose.Record(name)

if __name__ == "__main__":
    app.run(debug=True)