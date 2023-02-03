from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
tasks = db["tasks"]


@app.post("/tasks")
async def create_task(task: dict):
    result = tasks.insert_one(task)
    return {"task_id": str(result.inserted_id)}

@app.get("/tasks")
async def read_tasks():
    tasks_data = list(tasks.find({}))
    for task in tasks_data:
        task["_id"] = str(task["_id"])
    return tasks_data

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: dict):
    result = tasks.update_one({"_id": task_id}, {"$set": task})
    return {"modified_count": result.modified_count}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    result = tasks.delete_one({"_id": task_id})
    return {"deleted_count": result.deleted_count}
