import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core_api.models import UserProfile, TradeItem, Review, Wishlist

@pytest.mark.django_db
def test_userprofile_view_authentication():
    client = APIClient()
    response = client.get('/api/profiles/')
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_tradeitem_crud_operations():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    # Create
    data = {
        'title': 'Naruto Figure',
        'description': 'Limited edition',
        'interests': 'One Piece Figure'
    }
    response = client.post('/api/items/', data)
    assert response.status_code == 201
    item_id = response.data['id']

    # Read
    response = client.get(f'/api/items/{item_id}/')
    assert response.status_code == 200
    assert response.data['title'] == 'Naruto Figure'

    # Update
    update_data = {'title': 'Updated Naruto Figure'}
    response = client.patch(f'/api/items/{item_id}/', update_data)
    assert response.status_code == 200
    assert response.data['title'] == 'Updated Naruto Figure'

    # Delete
    response = client.delete(f'/api/items/{item_id}/')
    assert response.status_code == 204

@pytest.mark.django_db
def test_review_permissions():
    client = APIClient()
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    client.force_authenticate(user=user1)

    # Create a review
    data = {
        'reviewee_id': user2.id,
        'rating': 5,
        'comment': 'Great trader!'
    }
    response = client.post('/api/reviews/', data)
    assert response.status_code == 201

    # Try to delete the review as a different user
    client.force_authenticate(user=user2)
    review_id = response.data['id']
    response = client.delete(f'/api/reviews/{review_id}/')
    assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
def test_tradeitem_filtering_and_search():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    # Create items
    TradeItem.objects.create(title='Naruto Figure', description='Limited edition', owner=user)
    TradeItem.objects.create(title='One Piece Figure', description='Rare item', owner=user)

    # Filter by title
    response = client.get('/api/items/?title=Naruto')
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'Naruto Figure'

    # Search by description
    response = client.get('/api/items/?search=Rare')
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'One Piece Figure'