from django.db import models
from django.contrib.auth.models import User

class SchoolClass(models.Model):
    name = models.CharField(max_length=100, verbose_name="Sınıf Adı") # Örn: "12-A"
    year = models.IntegerField(verbose_name="Mezuniyet Yılı") # Örn: 2025

    def __str__(self):
        return f"{self.name} ({self.year})"

    class Meta:
        verbose_name = "Sınıf"
        verbose_name_plural = "Sınıflar"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="İlişkili Kullanıcı")
    first_name = models.CharField(max_length=100, verbose_name="Adı")
    last_name = models.CharField(max_length=100, verbose_name="Soyadı")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name="Dönemi")
    profile_picture = models.ImageField(upload_to='profile_pics/2025/', blank=True, null=True, verbose_name="Profil Fotoğrafı")
    
    # --- TIP FAKÜLTESİNE ÖZEL ALANLAR ---
    future_specialization = models.CharField(max_length=150, blank=True, verbose_name="Düşündüğü Uzmanlık") # Örn: "Kardiyoloji", "Beyin Cerrahisi"
    favorite_rotation = models.CharField(max_length=150, blank=True, verbose_name="En Sevdiği Staj") # Örn: "Pediatri", "Dahiliye"
    memorable_moment = models.TextField(blank=True, verbose_name="Fakültedeki Unutulmaz Anısı") # Örn: "İlk hasta muayenem", "Anatomi laboratuvarı"
    white_coat_photo = models.ImageField(upload_to='white_coat_photos/2025/', blank=True, null=True, verbose_name="Beyaz Önlük Töreni Fotoğrafı")
    def __str__(self):
        return f"Dr. Adayı {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "2025 Dönemi Mezunu"
        verbose_name_plural = "2025 Dönemi Mezunları"

    

class Memory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='memories', verbose_name="Hakkında Yazılan Öğrenci")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yazan Kişi")
    text = models.TextField(verbose_name="Anı Metni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yazılma Tarihi")
    is_approved = models.BooleanField(default=False, verbose_name="Onay Durumu") # Yönetici onayı için

    def __str__(self):
        return f"{self.author.username} -> {self.student.first_name}"

    class Meta:
        verbose_name = "Anı"
        verbose_name_plural = "Anılar"