from django.urls import path
from . import staff_views, views, admin_views, student_views, api_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main_app'

urlpatterns = [
    path("", views.login_user, name='login_user'),
    path("logout/", views.logout_user, name='logout_user'),

    # Api path
    path("recognize_faces/", api_views.recognize_faces, name='recognize_faces'),

    # Admin path
    path("admin/home/", admin_views.admin_home, name="admin_home"),


    path("admin/manage_class/", admin_views.manage_clazz, name='manage_class'),
    path("admin/add_class/", admin_views.add_class, name="add_class"),
    path('admin/delete_class/<int:clazz_id>/', admin_views.delete_class, name='delete_class'),
    path('admin/class/<int:clazz_id>/', admin_views.class_detail, name='admin_class_detail'),
    path('admin/class/<int:clazz_id>/remove-student/<str:student_id>/', admin_views.remove_student_from_clazz, name='remove_student_from_clazz'),
   
    path("admin/manage_staff/", admin_views.manage_staff, name='manage_staff'),
    path("admin/add_staff/", admin_views.add_staff, name="add_staff"),
    path('delete_staff/<str:staff_id>/', admin_views.delete_staff, name='delete_staff'),

    path("admin/manage_student/", admin_views.manage_student, name='manage_student'),
    path("admin/add_student/", admin_views.add_student, name="add_student"),
    path('delete_student/<str:student_id>/', admin_views.delete_student, name='delete_student'),


    # Staff path
    path('staff/home/', staff_views.staff_home, name='staff_home'),


    path("staff/classes/", staff_views.staff_classes, name='staff_classes'),
    path('staff/class-details/<int:clazz_id>/', staff_views.class_details, name='class_details'),
    path('staff/take-attendance/<int:clazz_id>/', staff_views.take_attendance, name='take_attendance'),


    path('staff/feedback/', staff_views.staff_feedback, name='staff_feedback'),
   
    #Student path
    path("student/home/", student_views.student_home, name="student_home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)