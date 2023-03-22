from .serializers import CandidateFilterListSerializer, CandidateDetailSerializer, EmailSerializer, RegisterSerializer, SituationSerializer
from Management.models import Candidate

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

# For Pagination
from .paginations import CandidatePagination

# For Filter and Search
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# For Authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from .customauth import IsRegularUser

# Helpers
from rest_framework.decorators import api_view
from rest_framework.response import Response

# For Mail
from django.core.mail import send_mail
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# ROUTE GUIDE
@api_view(['GET'])
def getRoutes(request):
    routes = [
      'For API Documentation: api/docs/',
      'For token Authentication',
      'To get Token: gettoken/',
      'To get Refreshtoken: refreshtoken/',
      'To Verify Token: verifytoken/',
      'For Registration: register/',
      'Get List: candidate/',
      'Invidual Candidate: candidate/<int:pk>/',
      'Email : email/',
    ]
    return Response(routes)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# CANDIDATE REGISTRATON
class CandidateCreate(CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = RegisterSerializer


# FOR ADMIN AND STAFF
class CandidateViewSet(ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateDetailSerializer
    pagination_class = CandidatePagination
    # FOR FILTER AND SEARCH
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['gender','job']
    search_fields = ['email', 'phone', 'firstname', 'lastname']
    # FOR AUTHENTICATION
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # HTTP PROTOCOLS
    http_method_names = ['get', 'delete']
    # TO SHOW FILTER LIST
    def get_serializer_class(self):
        if self.action == 'list':
            return CandidateFilterListSerializer
        return CandidateDetailSerializer
    # PERMISSION TO DELETE TO ADMIN
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


# EMAIL HANDLER
class EmailStatus(RetrieveUpdateAPIView):
    # FOR FILTER AND SEARCH
    pagination_class = CandidatePagination
    filter_backends = [SearchFilter]
    search_fields = ['email', 'name']
    http_method_names = ['get', 'post']
    # FOR AUTHENTICATION
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]
    # TO SHOW LIST
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SituationSerializer
        else:
            return EmailSerializer
    # For Filter
    def get_queryset(self):
        return Candidate.objects.filter(Situation='Approved').order_by('-created_at')
    # To Send email
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.instance
            company_name = 'PINNACA A.I. Solutions'
            send_mail(
                email.subject,
                email.message,
                f"{company_name} <{email.employee}>",
                [email.email],
                fail_silently=False,
            )
            data = serializer.data
            data['email'] = f"{company_name} <{email.email}>"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




