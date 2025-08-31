from django.urls import path
from . import views

app_name = 'resume_builder'

urlpatterns = [
    path('', views.ResumeListView.as_view(), name='list'),
    path('create/', views.ResumeCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ResumeDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ResumeEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ResumeDeleteView.as_view(), name='delete'),
    path('<int:pk>/download/pdf/', views.ResumeDownloadPDFView.as_view(), name='download_pdf'),
    path('<int:pk>/download/doc/', views.ResumeDownloadDocView.as_view(), name='download_doc'),
    path('templates/', views.TemplateListView.as_view(), name='templates'),
    path('builder/', views.ResumeBuilderView.as_view(), name='builder'),
]
