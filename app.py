import pytest
from flask import app


@pytest.fixture(scope='module')
def client():
    with app.app_context():
        yield app.test_client()

def test_get_all_fruits():
    response = client.get('/fruits')
    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "fruit": "apple", "color": "red"},
        {"id": 2, "fruit": "banana", "color": "yellow"},
        {"id": 3, "fruit": "orange", "color": "orange"}
    ]

def test_get_specific_fruit(client):
    response = client.get('/fruits/1')
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "fruit": "apple",
        "color": "red"
    }

    response = client.get('/fruits/4')
    assert response.status_code == 404
    assert response.json == {"error": "Fruit not found"}

def test_add_fruit_to_basket(client):
    response = client.post('/fruits', json={'fruit': 'grape', 'color': 'purple'})
    assert response.status_code == 201
    assert response.json == {"message": "Fruit added successfully"}

    response = client.post('/fruits', json={'color': 'blue'})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid request"}