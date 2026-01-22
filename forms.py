from django import forms
from .models import Category, MenuItem, Reservation

# ================= Reservation Form =================
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'phone', 'email', 'date', 'time', 'guests', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Any special request?',
                'rows': 3
            }),
        }

# ================= Category Form =================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'display_order']

# ================= Menu Item Form =================
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'name',
            'description',
            'price',
            'category',
            'is_available',
            'image'
        ]
