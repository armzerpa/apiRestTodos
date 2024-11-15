from flask import Flask
from flask_cors import CORS
from db import Connection

from uuid import uuid1
from flask import request

app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:3000", "http://localhost:3000"])

db = Connection('flask_mongo_crud')

@app.get("/tasks")
def get_tasks():
    tasks = db.task.find({})
    return {
        "data": list(tasks)
    }, 200

@app.post("/task")
def insert_task():
    _id = str(uuid1().hex)

    content = dict(request.json)
    content.update({"_id": _id})

    result = db.task.insert_one(content)
    if not result.inserted_id:
        return {"message": "Failed to insert value"}, 500

    tasks = db.task.find({})
    return {
        "message": "Success",
        "data": list(tasks)
    }, 200


@app.get("/task/<task_id>/")
def get_task(task_id):
    query = {
        "_id": task_id
    }
    task = db.task.find_one(query)

    if not task:
        return {
            "message": "Task not found"
        }, 404

    return {
        "data": task
    }, 200


@app.delete("/task/<task_id>/")
def delete_task(task_id):
    query = {
        "_id": task_id
    }
    result = db.task.delete_one(query)

    if not result.deleted_count:
        return {
            "message": "Failed to delete"
        }, 500

    return {"message": "Delete success"}, 200


@app.put("/task/<task_id>/")
def update_task(task_id):
    query = {
        "_id": task_id
    }
    content = {"$set": dict(request.json)}
    result = db.task.update_one(query, content)

    if not result.matched_count:
        return {
            "message": "Failed to update. Record is not found"
        }, 404

    if not result.modified_count:
        return {
            "message": "No changes applied"
        }, 500

    return {"message": "Update success"}, 200


if __name__ == "__main__":
    app.run(port=8887, debug=True)