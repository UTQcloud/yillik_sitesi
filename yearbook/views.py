# yearbook/views.py

from django.shortcuts import render, get_object_or_404

from .models import Student, Memory

def home(request):
   
    students = Student.objects.all().order_by('last_name', 'first_name')
    context = {'students': students}
    return render(request, 'yearbook/home.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    memories = Memory.objects.filter(student=student, is_approved=True).order_by('-created_at')
    context = {
        'student': student,
        'memories': memories
    }
    return render(request, 'yearbook/student_detail.html', context)