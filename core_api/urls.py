from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'items', views.TradeItemViewSet, basename='tradeitem')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.UserRegistrationView.as_view(), name='user_register'),

    # Profile endpoints
    path('profiles/', views.UserProfileListView.as_view(), name='profile_list'),
    path('profile/', views.CurrentUserProfileView.as_view(), name='current_profile'),
    path('users/<str:username>/profile/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('users/<str:username>/items/', views.TradeItemsByOwnerView.as_view(), name='user_items'),

    # Wishlist endpoints
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('wishlist/<int:pk>/add/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/<int:pk>/remove/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]