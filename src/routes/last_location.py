from flask import Blueprint, jsonify
from ..models.models import Taxi, Trajectory
from sqlalchemy import func

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
              last_date:
                type: string
                format: date-time
                description: The timestamp of the last reported location.
    """
    # # Query the last reported location of each taxi
    # last_locaotins = Trajectory.query.with_entities(Trajectory.taxi_id,
    #                                                 Taxi.plate,
    #                                                 func.max(Trajectory.date).label('last_date'),
    #                                                 Trajectory.latitude,
    #                                                 Trajectory.longitude) \
    #                                   .join(Taxi, Trajectory.taxi_id == Taxi.id) \
    #                                   .group_by(Trajectory.taxi_id, Taxi.plate, Trajectory.latitude, Trajectory.longitude) \
    #                                   .all()

    # Convert the results to JSON format
    # last_locations_list = [{'taxi_id': loc[0], 'plate': loc[1], 'last_date': loc[2].isoformat(), 'latitude': loc[3], 'longitude': loc[4]} for loc in last_locations]

    # return jsonify(last_locations_list)


    # Subconsulta para obtener las últimas ubicaciones por taxi_id
    last_locations_subquery = Trajectory.query \
        .with_entities(
            Trajectory.taxi_id,
            func.max(Trajectory.date).label('last_date')
        ) \
        .group_by(Trajectory.taxi_id) \
        .subquery()

    # Consulta principal que une la subconsulta con la tabla de trayectorias
    last_locations_query = Trajectory.query \
        .join(
            last_locations_subquery,
            (Trajectory.taxi_id == last_locations_subquery.c.taxi_id) &
            (Trajectory.date == last_locations_subquery.c.last_date)
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
            last_locations_subquery.c.last_date.label('last_date')
        )

    last_locations = last_locations_query.all()

    processed_taxi_ids = set()
    filtered_locations = []
    for location in last_locations:
        taxi_id = location.taxi_id
        # Verificar si el taxi_id ya ha sido procesado
        if taxi_id not in processed_taxi_ids:
            # Agregar el taxi_id al conjunto de procesados
            processed_taxi_ids.add(taxi_id)
            filtered_locations.append({
                'taxi_id': taxi_id,
                'plate': location.plate,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'last_date': location.last_date
            })

    return jsonify(filtered_locations)
