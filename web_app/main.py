import sys
sys.path.append("C:/Users/Victor Momodu/Documents/Programming/Arduino/Code/RFID-data-management")

from flask import Flask, render_template, request, jsonify
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
        active(facility)
        result = facility_data_findr(facility, existing=True)
        if result[facility][:5] == "Error":
            return render_template("error.html", error=result[facility])
        else:
            instance = purpose_pickr(facility, result[facility])
            dataframe = instance.data
            return render_template("data.html", facility=facility, use_case=result[facility], dataframe=dataframe)
    else:       
        facility = request.form["facility"]
        active(facility)
        result = facility_data_findr(facility, use_case=use_case)
        if result[facility][:5] == "Error":
            return render_template("error.html", error=result[facility])
        else:
            instance = purpose_pickr(facility, result[facility], form_data.splitlines())
            dataframe = instance.data
            return render_template("data.html", facility=facility, use_case=result[facility], dataframe=dataframe)

@app.route('/register', methods=["GET", "POST"])
def register():
    name = active()
    result = facility_data_findr(name, existing=True)
    instance = purpose_pickr(name, result[name])
    args = []
    places = instance.accss_plcs if result[name] == "Access" else ""
    try:
        idntfr = request.form["id"]
    except KeyError:
        pass
    else:
        args.append(idntfr)
        for i in instance.data.columns:
            args.append(request.form[i])
        if result[name] == "Access":
            instance.register(args=args, place_data=request.form["places"])
        else:
            instance.register(args=args)
    return render_template("register.html", name=name, use_case=result[name], dataframe=instance.data, places=places)

@app.route('/remove', methods=["GET", "POST"])
def remove():
    name = active()
    result = facility_data_findr(name, existing=True)
    instance = purpose_pickr(name, result[name])
    try:
        idntfr = request.form["id"]
    except KeyError:
        pass
    else:
        instance.remove(idntfr)
    return render_template("remove.html", name=name, use_case=result[name], dataframe=instance.data)

@app.route('/run', methods=["GET", "POST"])
def run():
    name = active()
    result = facility_data_findr(name, existing=True)
    instance = purpose_pickr(name, result[name])
    places = instance.accss_plcs if result[name] == "Access" else ""
    idntfr = {'idntfr': "1249"}
    try:
        request.form["id"]
    except KeyError:
        pass
    else:
        if result[name] == "Access":
            instance.access_checkr(request.form['id'], request.form["places"])
        elif result[name] == "Attendance":
            instance.attendance_logger(request.form["id"])
        elif result[name] == "Record":
            instance.record_editor(request.form["id"], request.form["data"])
    return render_template("run.html", name=name, use_case=result[name], places=places, idntfr=idntfr)

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
                return facility_data
            else:
                return {name: "Error: instance of this facililty exists in our database. Try using another name."}

def active(name=''):
    if name == '':
        try:
            with open("active.txt", 'r') as active:
                active_file = active.read()
        except FileNotFoundError:
            with open("active.txt", 'w') as active:
                active.write(name)
            return name
        else:
            return active_file
    else:
        with open("active.txt", 'w') as active:
                active.write(name)

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
                if TYPES[i.split(": ")[0]] == "cat":
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
