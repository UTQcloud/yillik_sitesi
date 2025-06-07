from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Student, SchoolClass, Memory

def home(request):
    # Ana sayfada genel bilgiler veya bir karşılama mesajı olabilir
    return render(request, 'yearbook/home.html')

def class_list(request):
    classes = SchoolClass.objects.all().order_by('year', 'name')
    context = {'classes': classes}
    return render(request, 'yearbook/class_list.html', context)

def student_list(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    students = Student.objects.filter(school_class=school_class).order_by('last_name')
    context = {
        'school_class': school_class,
        'students': students
    }
    return render(request, 'yearbook/student_list.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    # Sadece onaylanmış anıları göster
    memories = Memory.objects.filter(student=student, is_approved=True)
    context = {
        'student': student,
        'memories': memories
    }
    return render(request, 'yearbook/student_detail.html', context)