""" Test cases module """

import pytest
from app import app, flower_data, filter_flowers, get_flower_details_by_id


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """ Testing home_page """
    response = client.get('/')
    assert b"Welcome to the Flower Shop" in response.data
    assert response.status_code == 200


def test_contact_page(client):
    """ Testing contact_page """
    response = client.get('/contact')
    assert b"Contact Us" in response.data
    assert response.status_code == 200


def test_flower_recommender_page(client):
    """ Testing flower_recommender_page """
    response = client.get('/flower_recommender')
    assert b"Flower Recommender" in response.data
    assert response.status_code == 200


def test_flower_details_page(client):
    """ Testing flower_details_page """
    flower_id = 1  # Assuming there is a flower with ID 1
    response = client.get(f'/product-details/{flower_id}')
    assert b"Flower Details" in response.data
    assert response.status_code == 200


def test_invalid_flower_details_page(client):
    """ Testing invalid_flower_details_page """
    flower_id = 1999 
    response = client.get(f'/product-details/{flower_id}')
    assert response.status_code == 404


def test_get_recommendations(client):
    """ Testing get_recommendations """
    data = {
        'gender': 'female',
        'personality': 'romantic',
        'occasion': 'anniversary',
        'budget': '50.0'
    }
    response = client.post('/get_recommendations', data=data)
    assert b"Recommendations" in response.data
    assert response.status_code == 200


def test_filter_flowers():
    """ Testing filter_flowers function """
    filtered_flowers = filter_flowers('female', 'romantic', 'anniversary', '50.0')
    assert len(filtered_flowers) > 0


def test_get_flower_details_by_id():
    """ Testing flower data and IDs """
    flower = get_flower_details_by_id(1, flower_data)
    assert flower is not None
    assert flower['productId'] == 1


if __name__ == '__main__':
    pytest.main()
