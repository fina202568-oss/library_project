from django.contrib import admin
from .models import Category, MenuItem, SpecialItem

# Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)  # optional

# MenuItem admin
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')  # sub_category हटाइयो
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

# SpecialItem admin
@admin.register(SpecialItem)
class SpecialItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'image')


from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests')
    search_fields = ('name',)

