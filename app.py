from flask import Flask
from controller.metadata_controller import metadata_blueprint


app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(metadata_blueprint)

if __name__ == "__main__":
    app.run()
