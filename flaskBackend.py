from flask import Flask, render_template, request
import controller

app = Flask(__name__, template_folder="templates")

@app.route("/")
def hello():
    return render_template("webpage.html")

@app.route("/process", methods = ["post"])
def receive():
  data = request.get_json()
  controller.find(data['servo'])
  return data

app.run(host="0.0.0.0")