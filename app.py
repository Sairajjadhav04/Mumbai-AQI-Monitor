from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("login.html", error=None)
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", error=None)
@app.route("/register" , methods=["GET", "POST"])
def register():
    return render_template("register.html", error=None)
if __name__ == "__main__":
    app.run(debug=True)
