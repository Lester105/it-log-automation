from flask import Flask, render_template, request # type: ignore

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    issue = request.form["issue"]

    print("New Log:")
    print("Name:", name)
    print("Issue:", issue)

    return f"Log saved!<br>Name: {name}<br>Issue: {issue}"

@app.route("/tools")
def tools():
    return render_template("tools.html")

if __name__ == "__main__":
    app.run(debug=True)