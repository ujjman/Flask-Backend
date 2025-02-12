from models import Task, EventLog

class TaskRepository:
    def __init__(self, session):
        self.session = session

    def add(self, task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_all(self, page, per_page):
        query = self.session.query(Task).order_by(Task.id)
        tasks = query.all()
        start = (page - 1) * per_page
        end = start + per_page
        return tasks[start:end]

    def get_by_id(self, task_id):
        return self.session.query(Task).filter_by(id=task_id).first()

    def update(self, task):
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task):
        self.session.delete(task)
        self.session.commit()

class EventRepository:
    def __init__(self, session):
        self.session = session

    def add(self, event_log):
        self.session.add(event_log)
        self.session.commit()
        self.session.refresh(event_log)
        return event_log

    def get_all_events(self):
        return self.session.query(EventLog).order_by(EventLog.timestamp).all()
