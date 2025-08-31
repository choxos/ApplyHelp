from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('', views.CommunicationsDashboard.as_view(), name='dashboard'),
    path('templates/', views.EmailTemplateListView.as_view(), name='templates'),
    path('templates/<int:pk>/', views.EmailTemplateDetailView.as_view(), name='template_detail'),
    path('compose/', views.EmailComposeView.as_view(), name='compose'),
    path('applications/', views.ApplicationTrackerListView.as_view(), name='applications'),
    path('applications/create/', views.ApplicationTrackerCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/', views.ApplicationTrackerDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/edit/', views.ApplicationTrackerEditView.as_view(), name='application_edit'),
    path('tips/', views.CommunicationTipsView.as_view(), name='tips'),
    path('email-log/', views.EmailLogView.as_view(), name='email_log'),
]
