# yearbook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ogrenci/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Anı URL'leri - Hatanın çözümü için eklenen kısım
    path('ani/<int:memory_id>/duzenle/', views.edit_memory_view, name='edit_memory'),
    path('ani/<int:memory_id>/sil/', views.delete_memory_view, name='delete_memory'),

    # Üyelik URL'leri
    path('kayit/', views.register_view, name='register'),
    path('giris/', views.login_view, name='login'),
    path('cikis/', views.logout_view, name='logout'),
    path('profil/duzenle/', views.edit_profile_view, name='edit_profile'),
]