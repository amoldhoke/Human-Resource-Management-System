from django.urls import path, include
from Management import views
from Management import views
from app import settings
from django.conf.urls.static import static



urlpatterns = [
    # Frontend
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', include('django.contrib.auth.urls')),
    # Backend
    path('backend/', views.backend, name='backend'),
    path('<int:id>', views.candidate, name='candidate'),
    path('delete/<int:id>', views.delete, name='delete'),
    # Export to PDF
    path('<int:id>/index/', views.index, name='index'),
    path('pdf/<int:id>/', views.pdf, name='pdf'),
    # Send email
    path('email/', views.email, name='email'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )