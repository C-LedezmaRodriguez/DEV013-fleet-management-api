import pytest
from datetime import datetime
import requests

# Define la URL base de tu API REST
BASE_URL = "http://localhost:5000"

def test_list_taxis_endpoint():
    """Prueba para verificar si el endpoint /taxis devuelve una lista no vacía de taxis"""

    # Realiza una solicitud GET al endpoint /taxis
    response = requests.get(f"{BASE_URL}/taxis", timeout=5)

    # Verifica que la respuesta tenga el código de estado HTTP 200 (OK)
    assert response.status_code == 200

    # Convierte la respuesta JSON en un diccionario
    taxis = response.json()

    # Verifica que la lista de taxis no esté vacía
    assert len(taxis) > 0

    # Verifica que cada taxi tenga las claves 'id' y 'plate'
    for taxi in taxis:
        assert 'id' in taxi
        assert 'plate' in taxi
        
def test_list_trajectories_endpoint():
    """Prueba para verificar si el endpoint /trajectories devuelve una lista no vacía de jsonify"""

    # Realiza una solicitud GET al endpoint /trajectories
    response = requests.get(f"{BASE_URL}/trajectories", timeout=10)

    # Verifica que la respuesta tenga el código de estado HTTP 200 (OK)
    assert response.status_code == 200

    # Convierte la respuesta JSON en un diccionario
    trajectories = response.json()

    # Verifica que la lista de trayectorias no esté vacía
    assert len(trajectories) > 0

    # Verifica que cada trayectoria tenga las claves 
    for traj in trajectories:
        assert 'id' in traj
        assert 'taxi_id' in traj
        assert 'date' in traj
        assert 'latitude' in traj
        assert 'longitude' in traj

if __name__ == "__main__":
    pytest.main([__file__])
