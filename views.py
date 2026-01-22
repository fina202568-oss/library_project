from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Category, MenuItem, SpecialItem

from .forms import CategoryForm, MenuItemForm, ReservationForm

stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'


# ================= HOME PAGE =================
def home_page(request):
    specials = SpecialItem.objects.all()[:3]

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            send_mail(
                'Reservation Confirmation - Sakura Café',
                f'Hello {reservation.name},\n\nYour table reservation is confirmed.\n\n'
                f'Date: {reservation.date}\nTime: {reservation.time}\nGuests: {reservation.guests}\n'
                f'Phone: {reservation.phone}\n\nThank you,\nSakura Café',
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
            )
            return redirect('home')
    else:
        form = ReservationForm()

    return render(request, 'cafe/home.html', {'specials': specials, 'form': form})


# ================= MENU PAGE =================
def menu_page(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'cafe/menu.html', {'categories': categories})


# ================= CONTACT / ABOUT / RESERVATION =================
def about_page(request):
    return render(request, 'cafe/about.html')


def contact_page(request):
    return render(request, 'cafe/contact.html')


def reservation_page(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            send_mail(
                'Reservation Confirmation - Sakura Café',
                f'Hello {reservation.name}, your reservation is confirmed.\n'
                f'Date: {reservation.date}, Time: {reservation.time}, Guests: {reservation.guests}\n'
                f'Phone: {reservation.phone}',
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
            )
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'cafe/reservation.html', {'form': form})


# ================= TODAY SPECIAL =================
def today_special_partial(request):
    items = SpecialItem.objects.all()
    return render(request, 'cafe/special_items_partial.html', {'items': items})


# ================= CATEGORY EDIT/DELETE =================
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'cafe/category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('menu')
    return render(request, 'cafe/category_confirm_delete.html', {'category': category})


# ================= MENU ITEM EDIT/DELETE =================
def menuitem_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'cafe/menuitem_form.html', {'form': form})


def menuitem_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu')
    return render(request, 'cafe/menuitem_confirm_delete.html', {'item': item})


def order_page(request):
    categories = Category.objects.all()
    
    # Prepare items_by_category dictionary
    items_by_category = {cat: cat.items.all() for cat in categories}
    
    # Cart preview from session
    cart = request.session.get('cart', {})
    
    context = {
        'categories': categories,
        'items_by_category': items_by_category,
        'cart_preview': cart
    }
    return render(request, 'cafe/order.html', context)


def add_to_cart(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[item_id] = cart.get(item_id, 0) + quantity
        request.session['cart'] = cart
    return redirect('order_page')
# ================= VIEW CART =================
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # CartItem queryset
    total_price = sum([item.menu_item.price * item.quantity for item in cart_items])

    return render(request, 'cafe/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


# ================= UPDATE CART ITEM QUANTITY =================
@login_required
def update_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, menu_item_id=item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('view_cart')
def checkout_page(request):
    # Cart fetch
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum([item.menu_item.price * item.quantity for item in cart_items])

    if request.method == 'POST':
        # Stripe payment creation
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),  # Stripe expects cents
                currency='usd',
                payment_method_types=['card'],
            )
            return render(request, 'cafe/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'client_secret': intent.client_secret
            })
        except Exception as e:
            return render(request, 'cafe/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'error': str(e)
            })

    return render(request, 'cafe/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# ================= REMOVE ITEM FROM CART =================
@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, menu_item_id=item_id)
    cart_item.delete()
    return redirect('view_cart')
def checkout_success(request, order_id):
    # यहाँ तपाईं order confirmation logic राख्न सक्नुहुन्छ
    return render(request, 'cafe/checkout_success.html', {
        'order_id': order_id
    })
  


