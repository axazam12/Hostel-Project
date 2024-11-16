from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_warden = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='student')
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='profile',null=True)
    approval_status = models.BooleanField(default=0)
    course = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Parent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='parent')
    name=models.CharField(max_length=50)
    address= models.CharField(max_length=100)
    phone_no=models.CharField(max_length=10)
    photo=models.ImageField(upload_to='parent')
    email=models.EmailField()
    student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
    approval_status = models.IntegerField(default=0)

    def __str__(self):
        return self.name
class Hostel(models.Model):
    Hostel_Name=models.CharField(max_length=100)
    total_rooms=models.CharField(max_length=50)
    occupied=models.CharField(max_length=100)
    Rent=models.CharField(max_length=100)
    Location=models.CharField(max_length=100)
    Contact_No=models.CharField(max_length=100)
    room_facilities=models.CharField(max_length=100)
    photo = models.ImageField(upload_to='hostel')

    def __str__(self):
        return self.Hostel_Name

DAYS = (
    ('Sunday','Sunday'),
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
)

class food(models.Model):
    day=models.CharField(max_length=50,choices=DAYS)
    Breakfast=models.CharField(max_length=100)
    Lunch=models.CharField(max_length=100)
    Dinner=models.CharField(max_length=100)

    def __str__(self):
        return self.day

class Notification(models.Model):
    to = models.CharField(max_length=100)
    notification = models.TextField(max_length=100)
    time = models.TimeField()
    timestamp = models.DateField(auto_now_add=True,null=True)

class Warden(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='warden')
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    Email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='warden')
    Date_of_joining = models.DateField(auto_now=True)

    def __str__(self):
        return self.user

class Bookroom(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    booking_date =models.DateField()
    status =models.IntegerField(default=0)
    booked_by = models.ForeignKey(User,on_delete=models.CASCADE)


class Review(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    comments = models.CharField(max_length=30)

class Complaints(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=50,null=True,blank=True)


class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendance')
    date = models.DateField(auto_now=True)
    attendance = models.CharField(max_length=10)
    time = models.TimeField()
