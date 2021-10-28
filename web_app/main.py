from flask import Flask, render_template, request
import purpose

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
    return render_template("data.html", facility=request.args["facility"])

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/remove')
def remove():
    return render_template("remove.html")

@app.route('/run')
def run():
  return render_template("run.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="8080")