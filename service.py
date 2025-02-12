from models import Task, EventLog
from datetime import datetime

class TaskService:
    def __init__(self, task_repository, event_repository):
        self.task_repository = task_repository
        self.event_repository = event_repository

    def create_task(self, title, description, status="PENDING"):
        task = Task(title=title, description=description, status=status, created_at=datetime.utcnow())
        created_task = self.task_repository.add(task)
        self.event_repository.add(EventLog(event="Task Created", task_id=created_task.id))
        return created_task.to_dict()

    def get_all_tasks(self, page, per_page):
        tasks = self.task_repository.get_all(page, per_page)
        return [task.to_dict() for task in tasks]

    def update_task(self, task_id, update_data):
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        if "title" in update_data:
            task.title = update_data["title"]
        if "description" in update_data:
            task.description = update_data["description"]
        if "status" in update_data:
            task.status = update_data["status"]
        updated_task = self.task_repository.update(task)
        self.event_repository.add(EventLog(event="Task Updated", task_id=task_id))
        return updated_task.to_dict()

    def delete_task(self, task_id):
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        self.task_repository.delete(task)
        self.event_repository.add(EventLog(event="Task Deleted", task_id=task_id))
