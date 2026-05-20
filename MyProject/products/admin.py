from django.contrib import admin
from .models import Posting, Category, CartItem, Order, UserActivity

# Standard registration for simple models
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(UserActivity)

# Custom registration for Posting to show more details in the admin list
@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')