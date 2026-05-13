from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []

@app.route("/")

def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():

    task = request.form.get("task")

    if task:
        task.append(task)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
