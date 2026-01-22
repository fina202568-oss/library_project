from django.db import models
from django.contrib.auth.models import User


# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)  # Ordering control

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

# ================= MENU ITEM =================
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category__display_order', 'name']

    def __str__(self):
        return f"{self.name} - ¥{self.price}"

# ================= SPECIAL ITEM =================
class SpecialItem(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='special_items/')

    def __str__(self):
        return self.name

# ================= RESERVATION =================
class Reservation(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['category__display_order', 'name']
    def __str__(self):
        return f"{self.name} - ¥{self.price}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    