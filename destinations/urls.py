from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationsView.as_view(), name='list'),
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('countries/<str:code>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('universities/', views.UniversityListView.as_view(), name='universities'),
    path('universities/<int:pk>/', views.UniversityDetailView.as_view(), name='university_detail'),
    path('programs/', views.ProgramListView.as_view(), name='programs'),
    path('programs/<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('scholarships/', views.ScholarshipListView.as_view(), name='scholarships'),
    path('compare/', views.DestinationCompareView.as_view(), name='compare'),
    path('quiz/', views.DestinationQuizView.as_view(), name='quiz'),
]
