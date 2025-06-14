# Generated by Django 5.2.2 on 2025-06-07 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yearbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '2025 Dönemi Mezunu', 'verbose_name_plural': '2025 Dönemi Mezunları'},
        ),
        migrations.RemoveField(
            model_name='student',
            name='bio',
        ),
        migrations.AddField(
            model_name='student',
            name='favorite_rotation',
            field=models.CharField(blank=True, max_length=150, verbose_name='En Sevdiği Staj'),
        ),
        migrations.AddField(
            model_name='student',
            name='future_specialization',
            field=models.CharField(blank=True, max_length=150, verbose_name='Düşündüğü Uzmanlık'),
        ),
        migrations.AddField(
            model_name='student',
            name='memorable_moment',
            field=models.TextField(blank=True, verbose_name='Fakültedeki Unutulmaz Anısı'),
        ),
        migrations.AddField(
            model_name='student',
            name='white_coat_photo',
            field=models.ImageField(blank=True, null=True, upload_to='white_coat_photos/2025/', verbose_name='Beyaz Önlük Töreni Fotoğrafı'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/2025/', verbose_name='Profil Fotoğrafı'),
        ),
        migrations.AlterField(
            model_name='student',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yearbook.schoolclass', verbose_name='Dönemi'),
        ),
    ]
