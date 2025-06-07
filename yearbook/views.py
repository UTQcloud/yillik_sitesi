# yearbook/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student, Memory
from .forms import CustomUserCreationForm, StudentProfileForm, MemoryForm

def home(request):
    students = Student.objects.all().order_by('last_name', 'first_name')
    context = {'students': students}
    return render(request, 'yearbook/home.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    memories = Memory.objects.filter(student=student, is_approved=True).order_by('-created_at')
    
    # has_commented varsayılan olarak False
    has_commented = False
    if request.user.is_authenticated:
        # Silinen kayıt veritabanında olmayacağı için .exists() False döndürecektir.
        # Bu mantık, anı silindiğinde formun tekrar görünmesini sağlar.
        if Memory.objects.filter(student=student, author=request.user).exists():
            has_commented = True

    if request.method == 'POST' and request.user.is_authenticated:
        if not has_commented:
            memory_form = MemoryForm(request.POST)
            if memory_form.is_valid():
                new_memory = memory_form.save(commit=False)
                new_memory.student = student
                new_memory.author = request.user
                new_memory.is_approved = False
                new_memory.save()
                messages.success(request, 'Anınız başarıyla gönderildi ve onay bekliyor.')
                return redirect('student_detail', student_id=student.id)
        else:
            messages.warning(request, 'Bu kişi için zaten bir anı bıraktınız.')
            return redirect('student_detail', student_id=student.id)
    else:
        memory_form = MemoryForm()

    context = {
        'student': student,
        'memories': memories,
        'memory_form': memory_form,
        'has_commented': has_commented,
    }
    return render(request, 'yearbook/student_detail.html', context)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Yeni kullanıcıya boş bir Student profili oluştur
            Student.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
            return redirect('edit_profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'yearbook/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'yearbook/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile_view(request):
    # Kullanıcının Student profilini getir veya yoksa oluştur
    student, created = Student.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = StudentProfileForm(instance=student)
        
    return render(request, 'yearbook/edit_profile.html', {'form': form})