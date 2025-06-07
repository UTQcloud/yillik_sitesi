# yearbook/admin.py

from django.contrib import admin
from .models import Student, Memory 
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  
    list_display = ('first_name', 'last_name', 'user')
    search_fields = ('first_name', 'last_name')

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
   
    list_display = ('student', 'author', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_memories']

    def approve_memories(self, request, queryset):
        queryset.update(is_approved=True)
    approve_memories.short_description = "Seçili anıları onayla"
