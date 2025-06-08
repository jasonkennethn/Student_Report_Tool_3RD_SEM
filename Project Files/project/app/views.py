from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def no_cache(view_func):
    @never_cache
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@never_cache
@login_required
def dashboard_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        cgpa = request.POST.get('cgpa')
        if not (student_id and name and cgpa):
            messages.error(request, 'All fields are required.')
        elif Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID must be unique.')
        else:
            try:
                cgpa_val = float(cgpa)
                student = Student(student_id=student_id, name=name, cgpa=cgpa_val)
                student.save()
                messages.success(request, f"{name} record is successfully created")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'Details upload fail')
    return render(request, 'dashboard.html')

@never_cache
@login_required
def list_students_view(request):
    students = Student.objects.all()
    return render(request, 'list_students.html', {'students': students})

@never_cache
@login_required
def edit_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student_id_new = request.POST.get('student_id')
        name = request.POST.get('name')
        cgpa = request.POST.get('cgpa')
        if not (student_id_new and name and cgpa):
            messages.error(request, 'All fields are required.')
        elif Student.objects.filter(student_id=student_id_new).exclude(id=student.id).exists():
            messages.error(request, 'Student ID must be unique.')
        else:
            try:
                cgpa_val = float(cgpa)
                student.student_id = student_id_new
                student.name = name
                student.cgpa = cgpa_val
                student.save()
                messages.success(request, f"{student.name} record is successfully updated")
                return redirect('list_students')
            except Exception as e:
                messages.error(request, 'Update failed')
    return render(request, 'edit_student.html', {'student': student})

@never_cache
@login_required
def delete_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully')
        return redirect('list_students')
    return render(request, 'delete_student.html', {'student': student})

