from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cafe import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', views.home_page, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('reservation/', views.reservation_page, name='reservation'),

    # Cafe app extra urls (order, add-to-cart etc)
    path('', include('cafe.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

path('', include('cafe.urls')),  # ✅ app URLs include गर्नुहोस्
