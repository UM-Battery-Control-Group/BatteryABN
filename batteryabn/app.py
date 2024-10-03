import os
from dotenv import load_dotenv
from flask import Flask
from flask_injector import FlaskInjector
from flask_cors import CORS
from injector import singleton, Binder
from batteryabn.repositories import ProjectRepository, CellRepository, TestRecordRepository, FileSystemRepository
from batteryabn.services import ProjectService, CellService, TestRecordService
from batteryabn.models import db
from batteryabn.apis import projects_bp, cells_bp, trs_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load environment variables
    load_dotenv(dotenv_path='dev.env')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(cells_bp, url_prefix='/api/cells')
    app.register_blueprint(trs_bp, url_prefix='/api/trs')

    # Dependency Injection setup
    def configure(binder: Binder):
        binder.bind(ProjectRepository, to=ProjectRepository, scope=singleton)
        binder.bind(CellRepository, to=CellRepository, scope=singleton)
        binder.bind(TestRecordRepository, to=TestRecordRepository, scope=singleton)
        binder.bind(FileSystemRepository, to=FileSystemRepository, scope=singleton)
        binder.bind(ProjectService, to=ProjectService, scope=singleton)
        binder.bind(CellService, to=CellService, scope=singleton)
        binder.bind(TestRecordService, to=TestRecordService, scope=singleton)

    FlaskInjector(app=app, modules=[configure])

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
