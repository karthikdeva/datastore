from django.urls import include, path

from app.citizenData.views import CitizenView, MyTokenObtainPairView, CustomTokenObtainView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/citizenData/citizen/import_google_sheets_data/', views.import_google_sheets_data,
         name='admin:dataStore_citizen_import_google_sheets_data'),
    # path('', CitizenView.as_view(), name="citizen"),
    # path('auth/', MyTokenObtainPairView.as_view(), name="auth"),
]
