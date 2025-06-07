from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('siniflar/', views.class_list, name='class_list'),
    path('sinif/<int:class_id>/', views.student_list, name='student_list'),
    path('ogrenci/<int:student_id>/', views.student_detail, name='student_detail'),
]