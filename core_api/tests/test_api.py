import base64

import pytest
from PIL import Image
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core_api.models import TradeItem

@pytest.mark.django_db
def test_user_registration_and_login():
    client = APIClient()
    # Register
    data = {
        "username": "newuser",
        "password": "testpass123",
        "password2": "testpass123",
        "email": "newuser@example.com"
    }
    response = client.post('/api/auth/register/', data)
    print("Registration response:", response.data)
    assert response.status_code == 201
    # Login
    response = client.post('/api/auth/login/', {"username": "newuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "access" in response.data

@pytest.mark.django_db
def test_full_tradeitem_workflow():
    client = APIClient()
    user = User.objects.create_user(username='workflow', password='pass')
    client.force_authenticate(user=user)
    # Create
    data = {
        "title": "Gundam Model",
        "description": "MG RX-78-2",
        "interests": "Evangelion Model"
    }
    response = client.post('/api/items/', data)
    assert response.status_code == 201
    item_id = response.data['id']
    # Add to wishlist
    response = client.post(f'/api/wishlist/{item_id}/add/')
    assert response.status_code == 201
    # Remove from wishlist
    response = client.delete(f'/api/wishlist/{item_id}/remove/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_file_upload_to_tradeitem(tmp_path):
    client = APIClient()
    user = User.objects.create_user(username='fileuser', password='pass')
    client.force_authenticate(user=user)

    file_path = tmp_path / "test.png"
    image = Image.new('RGB', (100, 100), color='blue')
    image.save(file_path)
    with open(file_path, "rb") as fp:
        data = {
            "title": "Poster",
            "description": "Anime poster",
            "interests": "Figure",
            "image": fp
        }
        response = client.post('/api/items/', data, format='multipart')
    print(response.data)
    assert response.status_code == 201
    assert "image" in response.data

@pytest.mark.django_db
def test_authentication_required_for_wishlist():
    client = APIClient()
    user = User.objects.create_user(username='wishuser', password='pass')
    item = TradeItem.objects.create(title='Poster', description='desc', interests='fig', owner=user)
    # Not authenticated
    response = client.post(f'/api/wishlist/{item.id}/add/')
    assert response.status_code == 401