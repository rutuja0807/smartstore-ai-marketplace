from django.db import models
from django.conf import settings  # Required to fix the SystemCheckError

# --- 1. CATEGORY MODEL ---
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# --- 2. THE MAIN POSTING MODEL (Smart Store Products) ---
class Posting(models.Model):
    # 'title' matches your recent view and template updates
    title = models.CharField(max_length=200) 
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# --- 3. CART MODEL ---
class CartItem(models.Model):
    # Using settings.AUTH_USER_MODEL to avoid swapping errors
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Posting, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

# --- 4. ORDER MODEL (Updated for Checkout Form) ---
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Posting)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields to store data from the checkout.html address box and payment radio buttons
    address = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# --- 5. BEHAVIORAL AI TRACKING MODEL ---
class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20) # e.g., 'view', 'click', 'action'
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.post.title}"