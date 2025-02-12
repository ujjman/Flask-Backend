
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime
from models import db, Task, EventLog
from repository import TaskRepository, EventRepository
from service import TaskService

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'key_ujjwal_mishra'

    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    task_repo = TaskRepository(db.session)
    event_repo = EventRepository(db.session)
    task_service = TaskService(task_repo, event_repo)

    @app.route('/login', methods=['POST'])
    def login():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        if username != "ujjwal" or password != "mishra":
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    @app.route('/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        status = data.get("status", "PENDING")
        if not title or not description:
            return jsonify({"msg": "Title and description are required"}), 400
        task = task_service.create_task(title, description, status)
        return jsonify(task), 201

    @app.route('/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        tasks = task_service.get_all_tasks(page, per_page)
        return jsonify(tasks), 200

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    @jwt_required()
    def update_task(task_id):
        data = request.get_json()
        if not data:
            return jsonify({"msg": "No input data provided"}), 400
        allowed_fields = ['status']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        if not update_data:
            return jsonify({"msg": "No valid fields provided for update"}), 400
        try:
            updated_task = task_service.update_task(task_id, update_data)
            return jsonify(updated_task), 200
        except ValueError as e:
            return jsonify({"msg": str(e)}), 404

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(task_id):
        try:
            task_service.delete_task(task_id)
            return '', 204
        except ValueError as e:
            return '', 404

    @app.route('/events', methods=['GET'])
    @jwt_required()
    def get_events():
        events = event_repo.get_all_events()
        events_list = [event.to_dict() for event in events]
        return jsonify(events_list), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
