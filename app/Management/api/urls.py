from django.urls import path, include
from rest_framework import routers
from .views import CandidateCreate, CandidateViewSet, getRoutes, EmailStatus, MyTokenObtainPairView, PdfView, dashboardcount
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


router = routers.DefaultRouter()
router.register(r'candidate', CandidateViewSet)

urlpatterns = [
    path('', getRoutes),
    # Candidate total Count for dashboard
    path('dashboardcount/', dashboardcount),
    # Candidate Registration
    path('register/', CandidateCreate.as_view()),
    # For Email and Situation(only Approved)
    path('email/<int:pk>/', EmailStatus.as_view()),
        # For PDF
    path('pdf/<int:pk>/', PdfView.as_view()),
    # For MainPage(candidate, candidate.pk)
    path('', include(router.urls)),
    # Simple JWT
    path('gettoken/', MyTokenObtainPairView.as_view()),
    path('refreshtoken/', TokenRefreshView.as_view()),
    path('verifytoken/', TokenVerifyView.as_view()),
]

# httpie shortcuts
# http POST http://127.0.0.1:8000/api/gettoken/ username="amoldhoke" password="root"
# http POST http://127.0.0.1:8000/api/verifytoken/ token=""
# http POST http://127.0.0.1:8000/api/refreshtoken/ refresh=""
# http http://127.0.0.1:8000/api/candidate/ 'Authorization:Bearer '
# http http://127.0.0.1:8000/api/candidate/8/ 'Authorization:Bearer '
# http POST http://127.0.0.1:8000/api/gettoken/ username="sagarika" password="Amol@8898965229"
# http http://127.0.0.1:8000/api/email/8/ 'Authorization:Bearer '
