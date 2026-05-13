from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

tasks = []

# Create delete folder if it does not exist
os.makedirs("delete", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        tasks.append(task)
    return "", 204

@app.route("/delete_task", methods=["POST"])
def delete_task():
    data = request.get_json()
    deleted_text = data.get("task")
    if deleted_text:
        # Write deleted task into file
        with open("delete/deleted_text.txt", "a", encoding="utf-8") as file:
            file.write(deleted_text + "\n")
        # Remove from task list if exists
        if deleted_text in tasks:
            tasks.remove(deleted_text)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
