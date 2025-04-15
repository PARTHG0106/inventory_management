from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('inventory/', include('inventory.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('customers/', include('customers.urls')),
    path('orders/', include('orders.urls')),
    path('reports/', include('reports.urls')),
    path('api/', include('api.urls')),
    path('accounts/', include('allauth.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 