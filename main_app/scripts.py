import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse  
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *


def admin_home(request):
    admin = request.user.admin
    context = {
        'admin': admin
    }

    return render(request, 'admin_template/admin_home.html', context)


# Manage Class 
def manage_clazz(request):

    semesters = Clazz.objects.values_list('semester', flat=True).distinct()

    # Filter classes by semester if provided
    semester = request.GET.get('semester')

    if semester:
        all_clazz = Clazz.objects.filter(semester=semester)
    else:
        all_clazz = Clazz.objects.all()


    context = {
        'semesters': semesters,
        'all_clazz': all_clazz,
    }

    return render(request, "admin_template/manage_clazz.html", context)


# Add class button inside manage class page
def add_class(request):
    form = ClazzForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            class_id = form.cleaned_data.get('clazz_id')
            semester = form.cleaned_data.get('semester')
            teacher = form.cleaned_data.get('teacher')
            # place = form.cleaned_data.get('place')
            # schedule = form.cleaned_data.get('schedule')
            try:
                clazz = Clazz()
                clazz.name = name
                clazz.clazz_id = class_id
                clazz.teacher = teacher
                clazz.semester = semester
                # clazz.place = place
                # clazz.schedule = schedule
                clazz.save()
                messages.success(request, 'Successfully Added')
                return redirect(reverse('main_app:add_class'))
            
            except Exception as e:
                messages.error(request, "Could not add " + str(e))

        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'admin_template/add_class.html', context)

def clazz_details(request, clazz_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    students = clazz.students.all()

    context = {
        'clazz': clazz,
        'students': students
    }

    return render(request, 'admin_template/class_details.html', context)

# When click in class => Student list and add student, remove student button
def add_student_to_class(request, clazz_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, student_id=student_id)
        clazz.students.add(student)
        return redirect('class_details', clazz_id=clazz_id)

    context = {
        'clazz': clazz,
        'students': students
    }
    return render(request, 'admin_template/add_student_to_class.html', context)

def remove_student_from_clazz(request):
    pass

# Edit button inside manage class page
def edit_clazz(request):
    pass

# Delete button inside manage class page
def delete_clazz(request):
    pass



# Manage Teacher
def manage_teacher(request):
    pass

def add_teacher(request):
    pass

def edit_teacher(request):
    pass

def delete_teacher(request):
    pass

# Manage Student
def manage_student(request):
    pass

def add_student(request):
    pass

def edit_student(request):
    pass

def delete_student(request):
    pass

