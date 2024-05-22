from flask import Blueprint, jsonify
from sqlalchemy import func
from ..models.models import Taxi, Trajectory

last_location_routes = Blueprint('last_location', __name__)

@last_location_routes.route('/last_location', methods=['GET'])
def get_last_location():
    """
    Gets the last reported location of each taxi.
    ---
    responses:
      200:
        description: A list of the last reported locations of each taxi.
        schema:
          type: array
          items:
            type: object
            properties:
              taxi_id:
                type: integer
                description: The ID of the taxi.
              plate:
                type: string
                description: The plate of the taxi.
              latitude:
                type: float
                description: The latitude of the last reported location.
              longitude:
                type: float
                description: The longitude of the last reported location.
              timestamp:
                type: string
                format: date-time
                description: The timestamp of the last reported location.
    """

    # Subquery to obtain the last locations by taxi_id
    last_locations_subquery = Trajectory.query \
        .with_entities(
            Trajectory.taxi_id,
            func.max(Trajectory.date).label('timestamp')
        ) \
        .group_by(Trajectory.taxi_id) \
        .subquery()

    # Main query that joins the subquery with the trajectories table
    last_locations_query = Trajectory.query \
        .join(
            last_locations_subquery,
            (Trajectory.taxi_id == last_locations_subquery.c.taxi_id) &
            (Trajectory.date == last_locations_subquery.c.timestamp)
        ) \
        .join(
            Taxi,
            Trajectory.taxi_id == Taxi.id
        ) \
        .with_entities(
            Trajectory.taxi_id,
            Taxi.plate,
            Trajectory.latitude,
            Trajectory.longitude,
            last_locations_subquery.c.timestamp.label('timestamp')
        )\
        .distinct(Trajectory.taxi_id)

    last_locations = last_locations_query.all()

    filtered_locations = []

    for location in last_locations:
        filtered_locations.append({
            'taxi_id': location.taxi_id,
            'plate': location.plate,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'timestamp': location.timestamp
        })

    # processed_taxi_ids = set()
    # filtered_locations = []
    # for location in last_locations:
    #     taxi_id = location.taxi_id
    #     # Verificar si el taxi_id ya ha sido procesado
    #     if taxi_id not in processed_taxi_ids:
    #         # Agregar el taxi_id al conjunto de procesados
    #         processed_taxi_ids.add(taxi_id)
    #         filtered_locations.append({
    #             'taxi_id': taxi_id,
    #             'plate': location.plate,
    #             'latitude': location.latitude,
    #             'longitude': location.longitude,
    #             'timestamp': location.timestamp
    #         })

    return jsonify(filtered_locations)
