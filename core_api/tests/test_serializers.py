import types

import pytest
from django.contrib.auth.models import User
from core_api.models import UserProfile, TradeItem, Review, Wishlist
from core_api.serializers import (
    UserProfileSerializer, TradeItemSerializer, ReviewSerializer, WishlistSerializer
)

@pytest.mark.django_db
def test_user_profile_serializer():
    user = User.objects.create_user(username='testuser', password='pass')
    profile = user.userprofile
    profile.bio = 'Anime fan'
    serializer = UserProfileSerializer(profile)
    data = serializer.data
    assert data['user']['id'] == user.id or data['user'] == 'testuser'
    assert data['bio'] == 'Anime fan'

@pytest.mark.django_db
def test_trade_item_serializer_create():
    user = User.objects.create_user(username='owner', password='pass')
    data = {
        'title': 'Naruto Figure',
        'description': 'Limited edition',
        'interests': 'One Piece Figure',
        'owner': user.id
    }
    dummy_request = types.SimpleNamespace(user=user)
    serializer = TradeItemSerializer(data=data, context={'request': dummy_request})
    assert serializer.is_valid(), serializer.errors
    item = serializer.save()
    assert item.title == 'Naruto Figure'

@pytest.mark.django_db
def test_review_serializer_validation():
    reviewer = User.objects.create_user(username='reviewer', password='pass')
    reviewee = User.objects.create_user(username='reviewee', password='pass')
    data = {
        'reviewer': reviewer.id,
        'reviewee_id': reviewee.id,
        'rating': 5,
        'comment': 'Great trader!'
    }
    dummy_request = types.SimpleNamespace(user=reviewer)
    serializer = ReviewSerializer(data=data, context={'request': dummy_request})
    assert serializer.is_valid(), serializer.errors

    data['reviewee_id'] = reviewer.id
    serializer = ReviewSerializer(data=data, context={'request': dummy_request})
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors

@pytest.mark.django_db
def test_wishlist_serializer_unique():
    user = User.objects.create_user(username='wishuser', password='pass')
    item = TradeItem.objects.create(
        title='Bleach Poster',
        description='Cool poster',
        interests='Naruto Poster',
        owner=user
    )
    Wishlist.objects.create(user=user, item=item)
    data = {'item_id': item.id}
    dummy_request = types.SimpleNamespace(user=user)
    serializer = WishlistSerializer(data=data, context={'request': dummy_request})
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors or 'non_field_errors' in serializer.errors.values()