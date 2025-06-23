from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import TradeItem, UserProfile, Review, Wishlist
from .serializers import (
    TradeItemSerializer, TradeItemListSerializer, TradeItemDetailSerializer,
    UserProfileSerializer, ReviewSerializer, UserRegistrationSerializer
)
from .permissions import IsOwnerOrReadOnly, IsOwnerOnly, CanReviewUser
from .filters import TradeItemFilter
from rest_framework.pagination import CursorPagination

from django.http import JsonResponse

def health_check(request):
    """
    Simple health check endpoint.
    """
    return JsonResponse({"status": "ok"})



class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'  # Use your actual field name
    cursor_query_param = 'cursor'
    page_size_query_param = 'page_size'

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to register

class TradeItemViewSet(viewsets.ModelViewSet):
    queryset = TradeItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TradeItemFilter
    search_fields = ['title', 'description', 'interests']
    ordering_fields = ['created_at', 'title']
    pagination_class = CustomCursorPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return TradeItemListSerializer
        elif self.action == 'retrieve':
            return TradeItemDetailSerializer
        return TradeItemSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserProfileListView(generics.ListAPIView):
    """
    API endpoint to list all user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend ,filters.SearchFilter]
    search_fields = ['user__username', 'bio']
    pagination_class = CustomCursorPagination
    permission_classes = [IsAuthenticated]


class UserProfileDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a user profile by username.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOnly]

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(UserProfile, user__username=username)



class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update the current user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    Users can only create, update, and delete their own reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['reviewer', 'reviewee']
    ordering_fields = ['created_at', 'rating']
    pagination_class = CustomCursorPagination

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    @action(detail=False, methods=['get'])
    def user_reviews(self, request):
        """
        Get reviews for a specific user.
        """
        username = request.query_params.get('username')
        if not username:
            return Response(
                {"detail": "Username parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, username=username)
        reviews = Review.objects.filter(reviewee=user)

        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        serializer = self.get_serializer(reviews, many=True)
        return Response({
            'average_rating': avg_rating,
            'reviews': serializer.data
        })

class WishListView(generics.ListAPIView):
    serializer_class = TradeItemSerializer
    permission_classes = [IsAuthenticated]

    #a usual getter , gets the wishlist items for the current user
    def get_queryset(self):
        return TradeItem.objects.filter(wishlist__user=self.request.user)

class AddToWishlistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        item = get_object_or_404(TradeItem, pk=pk)

        #validation if alreadt in wishlist
        wishlist_entry, created = Wishlist.objects.get_or_create(
            user = request.user,
            item = item
        )

        if created:
            return Response(
                {"detail": "Item added to wishlist."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "Item already in wishlist."},
            status=status.HTTP_200_OK
        )

class RemoveFromWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(TradeItem, pk=pk)

        try:
            wishlist_entry = Wishlist.objects.get(
                user = request.user,
                item = item
            )
            wishlist_entry.delete()
            return Response(
                {"detail": "Item removed from wishlist."},
                status=status.HTTP_200_OK
            )
        except Wishlist.DoesNotExist:
            return Response(
                {"detail": "Item not found in wishlist."},
                status=status.HTTP_404_NOT_FOUND
            )


class TradeItemsByOwnerView(generics.ListAPIView):
    """
    View for listing all trade items owned by a specific user.
    """
    serializer_class = TradeItemListSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return TradeItem.objects.filter(owner=user)