from flask import Flask
from flasgger import Swagger
from config.config import config
from ..models.models import db
from ..routes.taxis import taxi_routes
from ..routes.trajectories import trajectory_routes
from ..routes.last_location import last_location_routes

app_ = Flask(__name__)

# Configure the Flask application to use the development configuration
app_.config.from_object(config['development'])

# Initialize SQLAlchemy
db.init_app(app_)

# Register taxi routes
app_.register_blueprint(taxi_routes)
app_.register_blueprint(trajectory_routes)
app_.register_blueprint(last_location_routes)

# Configure Flasgger
swagger = Swagger(app_)

if __name__ == "__main__":
    app_.run(debug=True) 