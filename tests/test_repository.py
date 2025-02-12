import unittest
from app import create_app
from models import db, Task, EventLog
from repository import TaskRepository, EventRepository

class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.session = db.session
        self.task_repo = TaskRepository(self.session)
        self.event_repo = EventRepository(self.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_and_get_task(self):
        task = Task(title="Test Task", description="Test Description", status="PENDING")
        created_task = self.task_repo.add(task)
        self.assertIsNotNone(created_task.id)
        fetched_task = self.task_repo.get_by_id(created_task.id)
        self.assertEqual(fetched_task.title, "Test Task")

    def test_get_all_tasks_pagination(self):
        for i in range(15):
            task = Task(title=f"Task {i}", description="Desc", status="PENDING")
            self.task_repo.add(task)
        tasks_page_1 = self.task_repo.get_all(page=1, per_page=10)
        tasks_page_2 = self.task_repo.get_all(page=2, per_page=10)
        self.assertEqual(len(tasks_page_1), 10)
        self.assertEqual(len(tasks_page_2), 5)

    def test_update_and_delete_task(self):
        task = Task(title="Task", description="Desc", status="PENDING")
        created_task = self.task_repo.add(task)
        created_task.title = "Updated Task"
        self.task_repo.update(created_task)
        updated_task = self.task_repo.get_by_id(created_task.id)
        self.assertEqual(updated_task.title, "Updated Task")
        self.task_repo.delete(updated_task)
        deleted_task = self.task_repo.get_by_id(created_task.id)
        self.assertIsNone(deleted_task)

    def test_event_log(self):
        event = EventLog(event="Task Created", task_id=1)
        created_event = self.event_repo.add(event)
        self.assertIsNotNone(created_event.id)
        events = self.event_repo.get_all_events()
        self.assertGreaterEqual(len(events), 1)

if __name__ == '__main__':
    unittest.main()
