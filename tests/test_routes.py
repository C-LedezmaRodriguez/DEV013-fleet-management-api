# test_app.py
from src.models.models import Taxi, Trajectory
from .test_data import TAXIS_DATA, TRAJECTORIES_DATA

def test_invalid_route(client):
    response = client.get('/invalid_route')
    assert response.status_code == 404

def test_taxis_pagination(client):
    response = client.get('/taxis?page=1&per_page=10')
    assert response.status_code == 200
    assert len(response.json) == 10

def test_trajectories_pagination(client):
    response = client.get('/trajectories?taxi_id=10133&date=2008-02-08 16:07:16')
    assert response.status_code == 200
    assert len(response.json) == 22

def test_get_taxis(client, mocker):
    # Crear un mock de la función query.all() para devolver los datos de prueba
    mock_query = mocker.MagicMock()
    mock_query.all.return_value = [Taxi(id=taxi['id'], plate=taxi['plate']) for taxi in TAXIS_DATA]

    mocker.patch('src.routes.taxis.get_taxis', return_value=mock_query)

    response = client.get('/taxis')

    assert response.status_code == 200
    assert response.json[:3]== TAXIS_DATA
    
def test_get_trajectories(client, mocker):
    # Crear un mock de la función query.all() para devolver los datos de prueba
    mock_query = mocker.MagicMock()
    mock_query.all.return_value = [Trajectory(id=trajectory['id'], taxi_id=trajectory['taxi_id'],date=trajectory['date'], latitude=trajectory['latitude'], longitude=trajectory['longitude']) for trajectory in TRAJECTORIES_DATA]

    mocker.patch('src.routes.trajectories.get_trajectories', return_value=mock_query)

    response = client.get('/trajectories')

    assert response.status_code == 200
    assert response.json[:3]== TRAJECTORIES_DATA
    