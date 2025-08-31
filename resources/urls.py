from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.ResourcesHomeView.as_view(), name='home'),
    path('guides/', views.GuideListView.as_view(), name='guides'),
    path('guides/<slug:slug>/', views.GuideDetailView.as_view(), name='guide_detail'),
    path('guides/category/<int:category_id>/', views.GuidesByCategoryView.as_view(), name='guides_by_category'),
]
