import json
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt  
from django.http import HttpResponse
import datetime


from .forms import *
from .models import *

def staff_home(request):
    teacher = request.user.staff
    context = {
        'teacher': teacher
    }
    return render(request, "staff_template/staff_home.html", context)

def staff_classes(request):
    # Retrieve the classes taught by the current teacher
    teacher = request.user.staff  # Assuming the current user is a staff member

    # Get all available semesters from the classes taught by the teacher
    semesters = Clazz.objects.filter(teacher=teacher).values_list('semester', flat=True).distinct()

    # Filter classes by semester if provided
    semester = request.GET.get('semester')
    if semester:
        classes = Clazz.objects.filter(teacher=teacher, semester=semester)
    else:
        classes = Clazz.objects.filter(teacher=teacher)

    context = {
        'classes': classes,
        'semesters': semesters,
        'selected_semester': semester
    }
    return render(request, 'staff_template/staff_classes.html', context)

def class_details(request, clazz_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    students = clazz.students.all()

    student_attendance = []
    for student in students:
        attendance_count = AttendanceRecord.objects.filter(student=student, attendance__clazz=clazz, status=False).count()
        student_attendance.append({'student': student, 'attendance_count': attendance_count})

    context = {
        'clazz': clazz,
        'student_attendance': student_attendance
    }
    return render(request, 'staff_template/class_details.html', context)

def take_attendance(request, clazz_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    students = clazz.students.all()

    context = {
        'clazz': clazz,
        'students': students,
        'clazz_id': clazz_id
    }
    return render(request, 'staff_template/take_attendance.html', context)

def staff_feedback(request):
    return render(request, 'staff_template/staff_feedback.html')