import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import math

from .forms import *
from .models import *

def student_home(request):
    student = get_object_or_404(Student, admin=request.user)
    total_classes = student.classes.count()
    total_attendance = AttendanceRecord.objects.filter(student=student).count()
    total_present = AttendanceRecord.objects.filter(student=student, status=True).count()
    
    if total_attendance == 0:
        percent_present = percent_absent = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    
    subjects = Clazz.objects.filter(students=student)
    subject_names = []
    data_present = []
    data_absent = []
    
    for subject in subjects:
        attendance = Attendance.objects.filter(clazz=subject)
        present_count = AttendanceRecord.objects.filter(attendance__in=attendance, status=True, student=student).count()
        absent_count = AttendanceRecord.objects.filter(attendance__in=attendance, status=False, student=student).count()
        subject_names.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    
    subject_data = zip(subjects, data_present, data_absent)

    context = {
    'total_attendance': total_attendance,
    'percent_present': percent_present,
    'percent_absent': percent_absent,
    'total_subject': total_classes,
    'subject_data': subject_data,
    'page_title': 'Student Homepage'
}

    
    return render(request, 'student_template/student_home.html', context)


# @ csrf_exempt
# def student_view_attendance(request):
#     student = get_object_or_404(Student, admin=request.user)
#     if request.method != 'POST':
#         course = get_object_or_404(Course, id=student.course.id)
#         context = {
#             'subjects': Subject.objects.filter(course=course),
#             'page_title': 'View Attendance'
#         }
#         return render(request, 'student_template/student_view_attendance.html', context)
#     else:
#         subject_id = request.POST.get('subject')
#         start = request.POST.get('start_date')
#         end = request.POST.get('end_date')
#         try:
#             subject = get_object_or_404(Subject, id=subject_id)
#             start_date = datetime.strptime(start, "%Y-%m-%d")
#             end_date = datetime.strptime(end, "%Y-%m-%d")
#             attendance = Attendance.objects.filter(
#                 date__range=(start_date, end_date), subject=subject)
#             attendance_reports = AttendanceReport.objects.filter(
#                 attendance__in=attendance, student=student)
#             json_data = []
#             for report in attendance_reports:
#                 data = {
#                     "date":  str(report.attendance.date),
#                     "status": report.status
#                 }
#                 json_data.append(data)
#             return JsonResponse(json.dumps(json_data), safe=False)
#         except Exception as e:
#             return None

# def student_view_profile(request):
#     student = get_object_or_404(Student, admin=request.user)
#     form = StudentEditForm(request.POST or None, request.FILES or None,
#                            instance=student)
#     context = {'form': form,
#                'page_title': 'View/Edit Profile'
#                }
#     if request.method == 'POST':
#         try:
#             if form.is_valid():
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 password = form.cleaned_data.get('password') or None
#                 address = form.cleaned_data.get('address')
#                 gender = form.cleaned_data.get('gender')
#                 passport = request.FILES.get('profile_pic') or None
#                 admin = student.admin
#                 if password != None:
#                     admin.set_password(password)
#                 if passport != None:
#                     fs = FileSystemStorage()
#                     filename = fs.save(passport.name, passport)
#                     passport_url = fs.url(filename)
#                     admin.profile_pic = passport_url
#                 admin.first_name = first_name
#                 admin.last_name = last_name
#                 admin.address = address
#                 admin.gender = gender
#                 admin.save()
#                 student.save()
#                 messages.success(request, "Profile Updated!")
#                 return redirect(reverse('student_view_profile'))
#             else:
#                 messages.error(request, "Invalid Data Provided")
#         except Exception as e:
#             messages.error(request, "Error Occured While Updating Profile " + str(e))

#     return render(request, "student_template/student_view_profile.html", context)
