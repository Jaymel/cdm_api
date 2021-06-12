import config
from module import db_query
from flask import Flask, request, jsonify
from urllib import parse

db_reader = db_query.DBReader(config.DATABASE_CONFIG)


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    from route import person, visit, concept, search
    app.register_blueprint(person.bp)
    app.register_blueprint(visit.bp)
    app.register_blueprint(concept.bp)
    app.register_blueprint(search.bp)

    @app.route('/')
    def main():
        return 'Hello World!'

    return app
