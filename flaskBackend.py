from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

@app.route("/")
def hello():
    return render_template("webpage.html")

@app.route("/process", methods = ["post"])
def printer():
  data = request.get_json()
  return data

@app.route("/wheels/<int:value>")
def getWheelsValue(value):
    print("v", str(value))
    return str(value)
app.run(host="0.0.0.0")