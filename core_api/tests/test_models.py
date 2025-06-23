import pytest
from django.contrib.auth.models import User
from core_api.models import UserProfile, TradeItem, Review, Wishlist
from rest_framework.exceptions import ValidationError

@pytest.mark.django_db
def test_user_profile_creation():
    user = User.objects.create_user(username='testuser', password='pass')
    profile = user.userprofile
    profile.bio = 'Anime fan'
    profile.save()
    assert profile.user.username == 'testuser'
    assert profile.bio == 'Anime fan'
    assert str(profile) == "testuser's Profile"

@pytest.mark.django_db
def test_trade_item_creation_and_owner():
    user = User.objects.create_user(username='owner', password='pass')
    item = TradeItem.objects.create(
        title='Naruto Figure',
        description='Limited edition',
        interests='One Piece Figure',
        owner=user
    )
    assert item.owner == user
    assert item.status == 'available'
    assert str(item) == 'Naruto Figure'

@pytest.mark.django_db
def test_review_validation_and_methods():
    reviewer = User.objects.create_user(username='reviewer', password='pass')
    reviewee = User.objects.create_user(username='reviewee', password='pass')
    review = Review.objects.create(
        reviewer=reviewer,
        reviewee=reviewee,
        rating=5,
        comment='Great trader!'
    )
    assert review.rating == 5
    assert str(review) == f"Review by {reviewer.username} for {reviewee.username} (5 stars)"
    # Test self-review validation
    review_self = Review(
        reviewer=reviewer,
        reviewee=reviewer,
        rating=4,
        comment='Self review'
    )
    with pytest.raises(ValidationError):
        review_self.clean()

@pytest.mark.django_db
def test_wishlist_unique_constraint():
    user = User.objects.create_user(username='wishuser', password='pass')
    item = TradeItem.objects.create(
        title='Bleach Poster',
        description='Cool poster',
        interests='Naruto Poster',
        owner=user
    )
    Wishlist.objects.create(user=user, item=item)
    with pytest.raises(Exception):
        # Should fail due to unique_together constraint
        Wishlist.objects.create(user=user, item=item)