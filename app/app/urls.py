from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView,)

# Admin Panel (replace)
admin.site.site_header = "HR ADMIN"
admin.site.index_title = "Table of candidates"

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('', include('Management.urls')),
    path('api/', include('Management.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs',),
]
