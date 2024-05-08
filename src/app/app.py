from flask import Flask
from flasgger import Swagger
from config.config import config
from ..models.models import db
from ..routes.taxis import taxi_routes
from ..routes.trajectories import trajectory_routes

app = Flask(__name__)

# Configure the Flask application to use the development configuration
app.config.from_object(config['development'])

# Initialize SQLAlchemy
db.init_app(app)

# Register taxi routes
app.register_blueprint(taxi_routes)
app.register_blueprint(trajectory_routes)

# Configure Flasgger
swagger = Swagger(app)

if __name__ == "__main__":
    app.run(debug=True) 