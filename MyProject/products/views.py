from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Posting, Category, CartItem, Order, UserActivity

# --- 1. PRODUCT LIST (HOME PAGE) ---
def product_list(request):
    """
    Displays products with support for Search and Category filtering.
    """
    posts = Posting.objects.all().order_by('-created_at')
    categories = Category.all() if hasattr(Category, 'all') else Category.objects.all()
    
    # --- SEARCH LOGIC ---
    # Fetches the 'q' parameter from the search bar
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    # --- CATEGORY LOGIC ---
    # Fetches the category ID from the sidebar or hero chips
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)

    context = {
        'products': posts,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

# --- 2. PRODUCT DETAIL ---
def product_detail(request, pk):
    product = get_object_or_404(Posting, pk=pk)
    
    # Record AI View Activity (Score: 1)
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            post=product,
            activity_type='view',
            score=1
        )
    
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

# --- 3. SMART CART & REDIRECT LOGIC ---

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Posting, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # AI Tracking for Click/Interest (Score: 3)
    UserActivity.objects.create(
        user=request.user,
        post=product,
        activity_type='click',
        score=3
    )

    # Advanced Redirect Logic:
    # If the user clicked "Buy Now", the URL contains ?next=checkout
    next_page = request.GET.get('next')
    if next_page == 'checkout':
        return redirect('checkout')
    
    # Otherwise, stay on current page and show success message
    messages.success(request, f"{product.title} added to your cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'products/cart_detail.html', context)

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart_detail')

# --- 4. ADVANCED CHECKOUT ---

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('home')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Create Order record
        order = Order.objects.create(
            user=request.user,
            ordered=True,
            address=address,
            payment_method=payment_method
        )
        
        for item in cart_items:
            order.items.add(item.product)
            # Record Purchase AI Activity (Highest Score: 5)
            UserActivity.objects.create(
                user=request.user,
                post=item.product,
                activity_type='action',
                score=5
            )

        # Clear cart and show success template
        cart_items.delete()
        return render(request, 'products/order_success.html')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'products/checkout.html', context)

# --- 5. STORE INSIGHTS (AI DASHBOARD) ---

@login_required
def store_analytics(request):
    """
    Calculates live data for the analytics_dashboard.html
    """
    # Get user behavioral logs
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:15]
    
    # Calculate Total Revenue from completed orders
    orders = Order.objects.filter(user=request.user, ordered=True)
    total_revenue = sum(sum(p.price for p in order.items.all()) for order in orders)
    
    # Customer Reach (Total views this user has made)
    total_views = UserActivity.objects.filter(user=request.user, activity_type='view').count()
    
    # Inventory Count
    product_count = Posting.objects.count()

    context = {
        'activities': activities,
        'total_revenue': total_revenue,
        'total_views': total_views,
        'product_count': product_count,
    }
    return render(request, 'products/analytics_dashboard.html', context)