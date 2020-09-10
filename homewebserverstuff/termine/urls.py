from django.urls import path
from . import views

urlpatterns = [
    path('', views.termineView, name='termine_home'),
    path('<int:pk>/', views.terminDetailView.as_view(), name='termine_details'),
    path('neu/', views.new_termin, name='termine_new'),
    path('<int:pk>/del', views.terminDeleteView.as_view(), name='termine_delete'),
]