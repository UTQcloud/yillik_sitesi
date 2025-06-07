# yearbook/views.py

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student, Memory
from .forms import CustomUserCreationForm, StudentProfileForm, MemoryForm

# yearbook/views.py

def home(request):
    # İstatistikler için verileri çek
    total_students = Student.objects.count()
    total_memories = Memory.objects.filter(is_approved=True).count()

    # Son eklenen 4 mezunu al
    recent_students = Student.objects.order_by('-user__date_joined')[:4]

    # Son eklenen ve onaylanmış 2 anıyı al
    recent_memories = Memory.objects.filter(is_approved=True).order_by('-created_at')[:2]

    context = {
        'total_students': total_students,
        'total_memories': total_memories,
        'recent_students': recent_students,
        'recent_memories': recent_memories,
    }
    return render(request, 'yearbook/home.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    memories = Memory.objects.filter(student=student, is_approved=True).order_by('-created_at')
    
    has_commented = False
    if request.user.is_authenticated:
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

def student_list(request):
    # 'models.Q' yerine sadece 'Q' kullan
    students = Student.objects.annotate(
        memory_count=Count('memories', filter=Q(memories__is_approved=True))
    ).order_by('first_name', 'last_name')

    context = {
        'students': students
    }
    return render(request, 'yearbook/student_list.html', context)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
    student, created = Student.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = StudentProfileForm(instance=student)
        
    return render(request, 'yearbook/edit_profile.html', {'form': form})

@login_required
def edit_memory_view(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)
    
    if memory.author != request.user:
        messages.error(request, "Bu anıyı düzenleme yetkiniz yok.")
        return redirect('student_detail', student_id=memory.student.id)

    if request.method == 'POST':
        form = MemoryForm(request.POST, instance=memory)
        if form.is_valid():
            edited_memory = form.save(commit=False)
            edited_memory.is_approved = False
            edited_memory.save()
            messages.success(request, 'Anınız güncellendi ve yeniden onay için yöneticiye gönderildi.')
            return redirect('student_detail', student_id=memory.student.id)
    else:
        form = MemoryForm(instance=memory)
        
    context = {
        'form': form,
        'student': memory.student
    }
    return render(request, 'yearbook/edit_memory.html', context)


@login_required
def delete_memory_view(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)
    
    if memory.author != request.user:
        messages.error(request, "Bu anıyı silme yetkiniz yok.")
        return redirect('student_detail', student_id=memory.student.id)

    if request.method == 'POST':
        memory.delete()
        messages.success(request, 'Anınız başarıyla silindi.')
        return redirect('student_detail', student_id=memory.student.id)
    
    return render(request, 'yearbook/confirm_memory.html', {'memory': memory})