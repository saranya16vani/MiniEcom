from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Product, Cart, CartItem, Order, OrderItem, Customer

# -------------------------
# Product Views
# -------------------------
def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Session management: track recently viewed products
    viewed = request.session.get("recently_viewed", [])
    if product_id not in viewed:
        viewed.append(product_id)
    request.session["recently_viewed"] = viewed[-5:]  # keep last 5

    return render(request, "product_detail.html", {"product": product})

def recently_viewed(request):
    ids = request.session.get("recently_viewed", [])
    products = Product.objects.filter(id__in=ids)
    return render(request, "recently_viewed.html", {"products": products})

# -------------------------
# Product CRUD (outside admin)
# -------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "image"]

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully!")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form})

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("product_list")

# -------------------------
# Cart Views
# -------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += 1
    item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect("view_cart")

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})

@login_required
def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect("view_cart")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("view_cart")

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def clear_cart(request):
    cart = request.user.cart
    cart.cartitem_set.all().delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.user.cart
    return render(request, "cart.html", {
        "cart": cart,
        "total_price": cart.total_price
    })


# -------------------------
# Order Views
# -------------------------
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("product_list")

    customer, created = Customer.objects.get_or_create(user=request.user)
    order = Order.objects.create(customer=customer)

    for item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart.cartitem_set.all().delete()
    messages.success(request, "Order placed successfully!")
    return redirect("order_list")

@login_required
def order_list(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(customer=customer)
    return render(request, "order_list.html", {"orders": orders})


@login_required
def profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"customer": customer})
