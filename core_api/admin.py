from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, TradeItem, Review, Wishlist

"""
Admin configuration for core_api models

    basically you register this para makita sa admin UI 
    and the list display , ways to display this sa UI 
    functions also help in viewing the fields

"""

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at', 'updated_at')
    search_fields = ('user__username', 'bio')

    def bio_summary(self, obj):
        return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
    bio_summary.short_description = 'Bio Summary'


@admin.register(TradeItem)
class TradeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'owner', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'interests')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__username', 'reviewee__username', 'comment')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'added_at')
    search_fields = ('user__username', 'item_name')
    list_filter = ('added_at',)

    def item_name(self, obj):
        return obj.item_name
    item_name.short_description = 'Item Name'

