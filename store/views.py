from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, Cart, CartItem, Order, OrderItem, User
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request, 'store/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('browse_books')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('browse_books')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
def browse_books(request):
    books = Book.objects.all()
    return render(request, 'store/browse_books.html', {'books': books})

def search_books(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    return render(request, 'store/browse_books.html', {'books': books})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    cart = get_object_or_404(cart, user=request.user)
    return render(request, 'store/view_cart.html', {'cart': cart})

def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        total_price = sum(item.book.price * item.quantity for item in cart.cartitem_set.all())
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)
            item.book.quantity_in_stock -= item.quantity
            item.book.save()
        cart.cartitem_set.all().delete()
        return redirect('order_confirmation')
    return render(request, 'store/checkout.html', {'cart': cart})


def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_admin, login_url='login')(view_func)
    return decorated_view_func

@admin_required
def manage_inventory(request):
    books = Book.objects.all()
    return render(request, 'store/manage_inventory.html', {'books': books})

@admin_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        Book.objects.create(title=title, author=author, price=price, quantity_in_stock=quantity)
        return redirect('manage_inventory')
    return render(request, 'store/add_book.html')

@admin_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = request.POST.get('price')
        book.quantity_in_stock = request.POST.get('quantity')
        book.save()
        return redirect('manage_inventory')
    return render(request, 'store/edit_book.html', {'book': book})

@admin_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('manage_inventory')

@admin_required
def sales_report(request):
    orders = Order.objects.all()
    return render(request, 'store/sales_report.html', {'orders': orders})

@admin_required
def inventory_report(request):
    books = Book.objects.all()
    return render(request, 'store/inventory_report.html', {'books': books})

@admin_required
def user_activity_report(request):
    users = User.objects.all()
    return render(request, 'store/user_activity_report.html', {'users': users})