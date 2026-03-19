from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('about/', include('core.urls_about')),
    path('data/', include('data_insights.urls')),
    path('support/', include('support.urls')),
    path('policy/', include('policy.urls')),
    path('reports/', include('reports.urls')),
    path('contact/', include('contact.urls')),
    path('accounts/', include('accounts.urls')),
    path('volunteers/', include('volunteers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
