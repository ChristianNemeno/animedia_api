from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, TradeItem, Review, Wishlist


# Basic User serializer for nested relationships
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)


# UserProfile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'avatar', 'bio', 'favorite_genres', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_avatar(self, value):
        if value and value.size > 2 * 1024 * 1024:  # 2MB limit
            raise serializers.ValidationError("Image size cannot exceed 2MB")
        return value


# TradeItem serializers
class TradeItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = TradeItem
        fields = ('id', 'title', 'description', 'image', 'interests',
                  'status', 'owner', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'owner')

    def validate_image(self, value):
        if value and value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Image size cannot exceed 5MB")
        return value

    def create(self, validated_data):
        # Set the owner to the current user
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


# Optimized list serializer for TradeItems
class TradeItemListSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = TradeItem
        fields = ('id', 'title', 'status', 'owner_username', 'image', 'created_at')
        read_only_fields = ('created_at', 'owner_username')


# Detailed serializer for TradeItems
class TradeItemDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = TradeItem
        fields = ('id', 'title', 'description', 'image', 'interests',
                  'status', 'owner', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'owner')


# Review serializer
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewee = UserSerializer(read_only=True)
    reviewee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='reviewee'
    )

    class Meta:
        model = Review
        fields = ('id', 'reviewer', 'reviewee', 'reviewee_id', 'rating', 'comment', 'created_at')
        read_only_fields = ('created_at', 'reviewer')

    def validate(self, attrs):
        # Check if the reviewee is not the reviewer
        if self.context['request'].user == attrs['reviewee']:
            raise serializers.ValidationError("You cannot review yourself")
        return attrs

    def create(self, validated_data):
        # Set the reviewer to the current user
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


# Wishlist serializer
class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    item = TradeItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=TradeItem.objects.all(),
        write_only=True,
        source='item'
    )

    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'item', 'item_id', 'added_at')
        read_only_fields = ('added_at', 'user')

    def create(self, validated_data):
        # Set the user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        user = self.context['request'].user if 'request' in self.context else attrs.get('user')
        item = attrs.get('item')
        if Wishlist.objects.filter(user=user, item=item).exists():
            raise serializers.ValidationError("This item is already in the user's wishlist.")
        return attrs


# User Registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        return user
