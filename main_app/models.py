import os
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Staff"), (3, "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name
    
    
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Staff(models.Model):
    staff_id = models.CharField(unique=True, max_length=20)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name
    
class Clazz(models.Model):
    name = models.CharField(max_length=100)
    clazz_id = models.CharField(unique=True ,max_length=50)
    semester = models.CharField(max_length=10)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    place = models.CharField(max_length=100)
    schedule = models.CharField(max_length=500)

    def __str__(self):  
        return self.name + ' ' + self.clazz_id

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(unique=True, max_length=20)
    classes = models.ManyToManyField(Clazz, related_name='students')

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name + ' ' + self.student_id

    def get_image_path(self, filename):
        return os.path.join('student_images', self.student.student_id, filename)

class StudentImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=Student.get_image_path)


class Attendance(models.Model):
    clazz = models.ForeignKey(Clazz, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()