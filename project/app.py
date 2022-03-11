from init import create_app
from API_v1 import blueprint


app = create_app(__name__)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run()
