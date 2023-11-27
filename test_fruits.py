import pytest
from app import app, db, Fruit


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_get_all_fruits(client):
    response = client.get('/fruits')
    assert response.status_code == 200
    assert len(response.get_json()) >= 0


def test_get_specific_fruit(client):
    # Assuming there's no fruit in the database yet
    response = client.get('/fruits/1')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Fruit not found"}

    # Add a fruit to the database
    client.post('/fruits', json={"fruit": "Apple", "color": "Red"})

    # Retrieve the added fruit
    response = client.get('/fruits/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "fruit": "Apple", "color": "Red"}


def test_add_fruit_to_basket(client):
    # Test with valid JSON payload
    response = client.post('/fruits', json={"fruit": "Banana", "color": "Yellow"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "Fruit added successfully"}

    # Test with invalid JSON payload
    response = client.post('/fruits', json={"fruit": "Grapes"})  # Missing 'color'
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid request"}

    # Check if the fruit is added to the database
    fruit = Fruit.query.first()
    assert fruit.fruit == "Banana"
    assert fruit.color == "Yellow"
