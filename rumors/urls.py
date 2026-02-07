from django.urls import path
from . import views

app_name = 'rumors'

urlpatterns = [
    path('', views.rumour_list, name='rumour_list'),
    path('rumour/<str:rumour_id>/', views.rumour_detail, name='rumour_detail'),
    path('summary/', views.summary, name='summary'),
    path('report/<str:rumour_id>/', views.add_report, name='add_report'),
]