from django.contrib.auth import login
from django.db.models.query import QuerySet
from django.views.generic.base import View
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import datetime, json
from django.utils import timezone

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .serializers import UserSerializer, RegisterSerializer
from rest_framework.views import APIView
from .models import Citizen
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect
from .google_sheets import read_data_from_google_sheets


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        # Check if the user is already authenticated (logged in)
        if request.user.is_authenticated:

            return redirect('')  # Replace 'dashboard' with your desired URL pattern
        else:
            return super().get(request, *args, **kwargs)

from django.template.loader import get_template

def check_template_paths(request):
    template = get_template('change_list.html')  # Replace with the actual template name
    print(template.origin.name)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        # token['last_login'] = user.last_login
        token['status'] = user.is_active
        token['email'] = user.email
        return token

##@login_required
##def import_from_google_sheets(request):
  ##  try:
    ##    data = read_data_from_google_sheets()
        # Process the data as needed
      ##  return redirect('/admin/dataStore/citizen/')
    ##except Exception as e:
        # Handle any exceptions, e.g., display an error message
      ##  return render(request, 'error.html', {'error_message': str(e)})

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # update the created time of the token to keep it valid
            token.created = datetime.datetime.utcnow()
            token.save()
        custom_response = {
            'token': token.key,
            'expires_in':token.created,
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_login':user.last_login,
            'status':user.is_active,
            'email': user.email
        }
        return Response(custom_response)




class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
@login_required
class CitizenView(APIView):

    def get_object(self):
       # try:
        # return Accounts.objects.all()
        # except Accounts.DoesNotExist
        raise status.HTTP_404_NOT_FOUND


    def get(self, request):
        # try:
        queryset = self.get_object()
        serializer = UserSerializer(queryset, many=True)
       # print('Hit by API')
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    @login_required
    def import_from_google_sheets(request):
        try:
            data = read_data_from_google_sheets()
            # Process the data as needed
            return redirect('/admin/citizenData/citizen/')

        except Exception as e:
            # Handle any exceptions, e.g., display an error message
            return render(request, 'error.html', {'error_message': str(e)})

    @login_required
    def logout_view(request):
        # Logout view logic (optional)
        return redirect('/admin/login')  # Redirect to the logout URL
    @login_required
  #  def dashboardView(request):
      #  data = Citizen.objects.all()
     #   return render(request, 'dashboard.html', {'citizens': data})
    @login_required
    def dashboardView(request):
        # Get the search parameters from the request
        query_name = request.GET.get('name', '')
        query_address = request.GET.get('address', '')
        query_phone = request.GET.get('phone', '')
        query_adhar = request.GET.get('adhar', '')
        query_epic = request.GET.get('epic', '')
        query_timestamp = request.GET.get('timestamp', '')

        # Base queryset
        citizen_data = Citizen.objects.all()

        # Apply search filters using Q objects
        citizen_data = citizen_data.filter(
            Q(name__icontains=query_name) |
            Q(address__icontains=query_address) |
            Q(phone__icontains=query_phone) |
            Q(adhar__icontains=query_adhar) |
            Q(epic__icontains=query_epic) |
            Q(timestamp__icontains=query_timestamp)
        )

        items_per_page = 10  # Adjust this as needed

        paginator = Paginator(citizen_data, items_per_page)
        page_number = request.GET.get('page', 1)  # Get the current page number from the request

        # Get the Page object for the current page
        page = paginator.get_page(page_number)

        return render(request, 'dashboard.html', {'citizens': page})


    def search_citizen(request):
        query_name = request.GET.get('name', '')
        query_address = request.GET.get('address', '')
        query_phone = request.GET.get('phone', '')
        query_adhar = request.GET.get('adhar', '')
        query_epic = request.GET.get('epic', '')
        query_timestamp = request.GET.get('timestamp', '')

        # Base queryset
        queryset = Citizen.objects.all()

        # User should be able to query using Name, Address, Phone, Adhar, EPIC, and Timestamp
        queryset = queryset.filter(
            Q(name__icontains=query_name) |
            Q(address__icontains=query_address) |
            Q(phone__icontains=query_phone) |
            Q(adhar__icontains=query_adhar) |
            Q(epic__icontains=query_epic) |
            Q(timestamp__icontains=query_timestamp)
        )

        # Additional specific queries can be added as needed...

        context = {'citizens': queryset}
        return render(request, 'search_results.html', context)
