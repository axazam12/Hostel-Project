import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from hostelapp.forms import add_hostel, foodform, Notificationform, wardenform, UserRegister
from hostelapp.models import Hostel, food, Notification, Warden, User, Student, Parent, Review, Complaints, Bookroom, \
    Attendance


def base(request):
    return render(request,'admin/ui.html')

def addhostel(request):
    h_form=add_hostel()
    if request.method=='POST':
        h_form=add_hostel(request.POST,request.FILES)
        if h_form.is_valid():
            h_form.save()
            return redirect('view_hostel')
    return render(request,'admin/addhostel.html',{'h_form':h_form})

def view_hostel(request):
    data=Hostel.objects.all()
    return render(request,'admin/viewhostel.html',{'data':data})

def update_hostel(request,id):
    data = Hostel.objects.get(id=id)
    h_form=add_hostel(instance=data)
    if request.method == 'POST':
        h_form = add_hostel(request.POST,request.FILES, instance=data)
        if h_form.is_valid():
            h_form.save()
            return redirect('view_hostel')
    return render(request,'admin/updatehostel.html',{'h_form':h_form})

def deletehostel(request,id):
    data=Hostel.objects.get(id=id)
    data.delete()
    return redirect('view_hostel')


def addfood(request):
    f_form=foodform()
    if request.method=='POST':
        f_form=foodform(request.POST)
        if f_form.is_valid():
            f_form.save()
            return redirect('viewfood')
    return render(request,'admin/addfood.html',{'f_form':f_form})

def viewfood(request):
    data=food.objects.all()
    return render(request,'admin/viewfood.html',{'data':data})

def updatefood(request,id):
    data=food.objects.get(id=id)
    f_form=foodform(instance=data)
    if request.method=='POST':
        f_form=foodform(request.POST,instance=data)
        if f_form.is_valid():
            f_form.save()
            return redirect('viewfood')
    return render(request,'admin/updatefood.html',{'f_form':f_form})

def deletefood(request,id):
    data=food.objects.get(id=id)
    data.delete()
    return redirect('viewfood')

def notiadd(request):
    n_form=Notificationform()
    if request.method=='POST':
        n_form=Notificationform(request.POST)
        n_form.save()
        return redirect('notiview')
    return render(request,'admin/notiadd.html',{'n_form':n_form})

def notiview(request):
    data=Notification.objects.all()
    return render(request,'admin/notiview.html',{'data':data})

def notiupdate(request,id):
    data=Notification.objects.get(id=id)
    n_form=Notificationform(instance=data)
    if request.method=='POST':
        n_form=Notificationform(request.POST,instance=data)
        if n_form.is_valid():
            n_form.save()
            return redirect('notiview')
    return render(request,'admin/notiupdate.html',{'n_form':n_form})

def deletenoti(request,id):
    data=Notification.objects.get(id=id)
    data.delete()
    return redirect('viewnoti')

def wardenreg(request):
    u_form = UserRegister()
    w_form = wardenform()
    if request.method=='POST':
        u_form=UserRegister(request.POST)
        w_form=wardenform(request.POST,request.FILES)
        if u_form.is_valid() and w_form.is_valid():
            user = u_form.save(commit=False)
            user.is_warden=True
            user.save()
            warden = w_form.save(commit=False)
            warden.user=user
            warden.save()
            messages.info(request,'warden registered successfully')
            return redirect('wardenview')
    return render(request,'admin/wardenadd.html',{'u_form':u_form,'w_form':w_form})

def wardenview(request):
    data=Warden.objects.all()
    return render(request,'admin/wardenview.html',{'data':data})

def wardenupdate(request,id):
    data = Warden.objects.get(id=id)
    w_form =wardenform(request.POST or None,request.FILES or None,instance=data)
    if w_form.is_valid():
        w_form.save()
        return redirect('wardenview')
    return render(request,'admin/wardenupdate.html',{'w_form':w_form})

def wardendel(request,id):
    data1=Warden.objects.get(id=id)
    data = User.objects.get(warden=data1)
    if request.method=='POST':
        data.delete()
        return redirect('wardenview')
    else:
        return redirect('wardenview')

def viewreg(request):
    student = Student.objects.all()
    parent = Parent.objects.all()
    context = {
        'student':student,
        'parent':parent
    }
    student = Student.objects.all()
    parent = Parent.objects.all()
    context = {
        'student':student,
        'parent':parent
    }
    return render(request,'admin/viewreg.html',context)

def approve_student(request,id):
    student=Student.objects.get(user_id=id)
    student.approval_status=1
    student.save()
    messages.info(request,'student approved successfully')
    return redirect('viewreg')

def reject_student(request,id):
    data1 = Student.objects.get(user_id=id)
    data = User.objects.get(student=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('viewreg')
    else:
        return redirect('viewreg')

def approve_parent(request,id):
    parent=Parent.objects.get(user_id=id)
    parent.approval_status=1
    parent.save()
    messages.info(request,'parent approved successfully')
    return redirect('viewreg')

def reject_parent(request,id):
    data1 = Parent.objects.get(user_id=id)
    data = User.objects.get(parent=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('viewreg')
    else:
        return redirect('viewreg')

def viewreview_admin(request):
    data=Review.objects.all()
    return render(request,'admin/viewreview.html',{'data':data})

def complaint_view(request):
    data = Complaints.objects.all()
    return render(request,'admin/complaintview.html',{'data':data})

def reply_complaint(request, id):
    f = Complaints.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('complaint_view')
    return render(request, 'admin/reply_complaint.html', {'f': f})

def view_booking(request):
    data = Bookroom.objects.all()
    return render(request,'admin/viewbooking.html',{'data':data})

def confirm_booking(request, id):
    details_qs = Hostel.objects.all()
    if details_qs.exists():

        book = Bookroom.objects.get(id=id)
        book.status = 1
        book.save()

        hstl = Hostel.objects.all().last()
        occupied = hstl.occupied
        hstl.occupied = int(occupied) + 1
        hstl.save()
        messages.info(request, 'Room Booking Confirmed')
        return redirect('view_booking')
    else:
        messages.info(request, 'Please Update Hostel Details')
        return HttpResponseRedirect(reverse('view_booking'))


def reject_booking(request, id):
    book = Bookroom.objects.get(id=id)
    if request.method == 'POST':
        book.status = 2
        book.save()
        messages.info(request, 'Room Booking rejected')
        return redirect('view_booking')
    return render(request, 'admin/reject_booking.html')

def add_attendance(request):
    student = Student.objects.filter(approval_status=True)
    return render(request, 'admin/student_list.html', {'student': student})

now = datetime.datetime.now()

def mark(request, id):
    user = Student.objects.get(user_id=id)
    att = Attendance.objects.filter(student=user, date=datetime.date.today())
    if att.exists():
        messages.info(request, "Today's Attendance Already marked for this Student ")
        return redirect('add_attendance')
    else:
        if request.method == 'POST':
            attndc = request.POST.get('attendance')
            Attendance(student=user, date=datetime.date.today(), attendance=attndc,time=now.time()).save()
            messages.info(request, "Attendance Added successfully ")
            return redirect('add_attendance')
    return render(request, 'admin/mark_attendance.html')

def view_attendance(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for i in value_list:
        attendance[i] = Attendance.objects.filter(date=i)
    return render(request, 'admin/view_attendance.html', {'attendances': attendance})


# In Python, using the Django framework, the line of code Attendance.objects.values_list('date', flat=True).distinct() retrieves a distinct list of dates from the Attendance model.
#
# Here's what this line of code does step by step:
#
# Attendance: This is the model class representing the data you have defined in your Django application. It's assumed that you have a model named Attendance.
#
# .objects: This is the manager provided by Django to interact with the database records associated with the Attendance model.
#
# .values_list('date', flat=True): This method retrieves specific fields from the database records. In this case, it retrieves the 'date' field from the Attendance model. The flat=True argument indicates that you want to receive a flat list of values instead of a list of tuples.
#
# .distinct(): This method is used to retrieve only distinct values from the list of dates. It ensures that each date appears only once in the final list.
#
# So, when you execute Attendance.objects.values_list('date', flat=True).distinct(), you will get a list of distinct date values from the 'date' field of the Attendance model's database records. This is useful for obtaining a list of unique dates when recording attendance, for example.

def day_attendance(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendances': attendance,
        'date': date
    }
    return render(request, 'admin/day_attendance.html', context)