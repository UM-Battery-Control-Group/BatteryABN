from flask import Flask
from flask_injector import FlaskInjector
from apis import projects_bp, cells_bp, trs_bp
from injector import singleton, Binder
from repositories import ProjectRepository, CellRepository, TestRecordRepository
from services import ProjectService, CellService, TestRecordService
from models import Session

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(cells_bp, url_prefix='/api/cells')
    app.register_blueprint(trs_bp, url_prefix='/api/trs')

    return app

# Dependency Injection setup
def configure(binder: Binder):
    binder.bind(ProjectRepository, to=ProjectRepository(Session()), scope=singleton)
    binder.bind(CellRepository, to=CellRepository(Session()), scope=singleton)
    binder.bind(TestRecordRepository, to=TestRecordRepository(Session()), scope=singleton)
    binder.bind(ProjectService, to=ProjectService, scope=singleton)
    binder.bind(CellService, to=CellService, scope=singleton)
    binder.bind(TestRecordService, to=TestRecordService, scope=singleton)

if __name__ == '__main__':
    app = create_app()
    FlaskInjector(app=app, modules=[configure])
    app.run(debug=True)
