from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

tasks = []

# Create folders automatically
MISSION_FOLDER = "mission"
DELETE_FOLDER = "delete"

MISSION_FILE = os.path.join(MISSION_FOLDER, "mission_task.txt")
DELETE_FILE = os.path.join(DELETE_FOLDER, "deleted_text.txt")

os.makedirs(MISSION_FOLDER, exist_ok=True)
os.makedirs(DELETE_FOLDER, exist_ok=True)

# Load saved tasks when app starts
if os.path.exists(MISSION_FILE):
    with open(MISSION_FILE, "r", encoding="utf-8") as file:
        for line in file:
            task = line.strip()
            if task and task not in tasks:
                tasks.append(task)


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")

    if task:
        task = task.strip()
        # Prevent duplicate tasks
        if task not in tasks:
            # Add to memory list
            tasks.append(task)
            # Save to file
            with open(MISSION_FILE, "a", encoding="utf-8") as file:
                file.write(task + "\n")
            return jsonify({
                "success": True,
                "message": "Task added"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Task already exists"
            })

    return jsonify({
        "success": False,
        "message": "Empty task"
    })


@app.route("/delete", methods=["POST"])
def delete_task():
    data = request.get_json()
    deleted_text = data.get("task")

    if deleted_text:
        # Save deleted task into deleted_text.txt
        with open(DELETE_FILE, "a", encoding="utf-8") as file:
            file.write(deleted_text + "\n")

        # Remove from task memory
        if deleted_text in tasks:
            tasks.remove(deleted_text)

        # Rewrite mission_task.txt without deleted task
        with open(MISSION_FILE, "w", encoding="utf-8") as file:
            for task in tasks:
                file.write(task + "\n")

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
