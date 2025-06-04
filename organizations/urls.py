from django.urls import path

from .views import ReadOrganizationView

app_name = 'organizations'

urlpatterns = [
    path('organizations/<str:inn>/', ReadOrganizationView.as_view(), name='organization-detail'),
]
