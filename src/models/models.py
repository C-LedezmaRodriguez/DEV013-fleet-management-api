from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Taxi(db.Model):
    __tablename__ = 'taxis'
    """
    Modelo de datos para representar un taxi.

    Atributos:
        id (int): Identificador único del taxi (clave primaria).
        plate (str): Placa del taxi.
    """
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)

class Trajectory(db.Model):
    """
    Modelo de datos para representar una trayectoria de un taxi.

    Atributos:
        id (int): Identificador único de la trayectoria (clave primaria).
        taxi_id (int): ID del taxi asociado a la trayectoria (clave foránea).
        date (datetime): Fecha y hora de la trayectoria.
        latitude (float): Latitud de la ubicación del taxi.
        longitude (float): Longitud de la ubicación del taxi.
    """
    __tablename__ = 'trajectories'
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey('taxis.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)