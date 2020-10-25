from django.urls import path
from . import views

urlpatterns = [
    path('', views.audiobView, name='audiob_home'),
    path('autor/', views.authors_home, name='authors_home'),
    path('autor/neu/', views.new_author, name='author_new'),
    path('autor/<int:pk>/', views.authorDetailView.as_view(), name='author_details'),
    path('autor/<int:pk>/del/', views.authorDeleteView.as_view(), name='author_delete'),
    path('autor/<int:pk>/edit/', views.authorUpdateView.as_view(), name='author_edit'),
    path('hörbuch/neu/', views.new_audiobook, name='audiob_new'),
    path('hörbuch/<int:pk>/', views.audiobDetailView.as_view(), name='audiob_details'),
]