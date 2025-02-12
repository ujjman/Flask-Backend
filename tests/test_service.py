import unittest
from app import create_app
from models import db
from repository import TaskRepository, EventRepository
from service import TaskService

class TaskServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.session = db.session
        self.task_repo = TaskRepository(self.session)
        self.event_repo = EventRepository(self.session)
        self.task_service = TaskService(self.task_repo, self.event_repo)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_task(self):
        task_dict = self.task_service.create_task("New Task", "Task Description")
        self.assertEqual(task_dict["title"], "New Task")
        self.assertEqual(task_dict["status"], "PENDING")
        events = self.event_repo.get_all_events()
        self.assertTrue(any(e.event == "Task Created" for e in events))

    def test_get_all_tasks(self):
        self.task_service.create_task("Task1", "Desc1")
        self.task_service.create_task("Task2", "Desc2")
        tasks = self.task_service.get_all_tasks(page=1, per_page=10)
        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        task_dict = self.task_service.create_task("Task1", "Desc1")
        task_id = task_dict["id"]
        updated_task = self.task_service.update_task(task_id, {"status": "COMPLETED"})
        self.assertEqual(updated_task["status"], "COMPLETED")
        events = self.event_repo.get_all_events()
        self.assertTrue(any(e.event == "Task Updated" for e in events))

    def test_delete_task(self):
        task_dict = self.task_service.create_task("Task1", "Desc1")
        task_id = task_dict["id"]
        self.task_service.delete_task(task_id)
        tasks = self.task_service.get_all_tasks(page=1, per_page=10)
        self.assertEqual(len(tasks), 0)
        events = self.event_repo.get_all_events()
        self.assertTrue(any(e.event == "Task Deleted" for e in events))

if __name__ == '__main__':
    unittest.main()
