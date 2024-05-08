from flask import Blueprint, jsonify, request
from ..models.models import Taxi

taxi_routes = Blueprint('taxis', __name__)

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10

# Route to list all taxis
@taxi_routes.route('/taxis', methods=['GET'])
def get_taxis():
    """
    Gets the list of all taxis.
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Page number for pagination.
      - name: per_page
        in: query
        type: integer
        required: false
        description: Number of items per page.
    responses:
      200:
        description: A list of taxis.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The ID of the taxi.
              plate:
                type: string
                description: The license plate of the taxi.
    """
    # Pagination parameters
    page = int(request.args.get('page', DEFAULT_PAGE))
    per_page = int(request.args.get('per_page', DEFAULT_PER_PAGE))

    # Calculate start and end index for pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Query taxis from the database
    taxis = Taxi.query.all()

    # Get the subset of taxis for the current page
    taxis_subset = taxis[start_index:end_index]

    # Convert taxis to JSON format
    taxis_list = [{'id': taxi.id, 'plate': taxi.plate} for taxi in taxis_subset]

    return jsonify(taxis_list)
