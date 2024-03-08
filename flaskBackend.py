from flask import Flask, render_template, request
import controller

def main():
  app = Flask(__name__, template_folder="templates")
  controller.main()
  @app.route("/")
  def hello():
      return render_template("webpage.html")

  @app.route("/process", methods = ["post"])
  def receive():
    data = request.get_json()
    print(data)
    controller.find(data)
    return data

  app.run(host="0.0.0.0")

if __name__ == "__main__":
   main()