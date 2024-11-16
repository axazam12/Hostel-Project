from django.contrib import messages
from django.shortcuts import render, redirect

from hostelapp.forms import bookform, reviewform, complaintform
from hostelapp.models import Hostel, Student, Bookroom, Review, Complaints


def base1(request):
    return render(request,'student/base.html')

def viewhostel(request):
    data=Hostel.objects.all()
    return render(request,'student/viewhostel.html',{'data':data})

def book_room(request):
    form = bookform()
    if request.method == 'POST':
        form = bookform(request.POST)
        if form.is_valid():
            book = form.save(commit=False)

            book.student = Student.objects.get(user=request.user)
            book.booking_date = form.cleaned_data.get('booking_date')
            book.booked_by = request.user
            student_qs = Bookroom.objects.filter(student=Student.objects.get(user=request.user))
            if student_qs.exists():
                messages.info(request, 'You have Already Booked room  ')
            else:
                book.save()
                messages.info(request, 'Successfully Booked Room ')
                return redirect('base1')
    return render(request, 'student/book_room.html', {'form': form})

def booking_status(request):
    student =Student.objects.get(user=request.user)
    status = Bookroom.objects.filter(student=student)
    return render(request,'student/booking_status.html',{'status':status})

def add_review(request):
    s=Student.objects.get(user=request.user)
    form = reviewform()
    if request.method== 'POST':
        form = reviewform(request.POST)
        f=form.save(commit=False)
        f.student =s
        f.save()
        messages.info(request, 'Your Review Send Successfully')
        return redirect('base1')
    return render(request,'student/addreview.html',{'form':form})

def viewreview(request):
    data=Review.objects.all()
    return render(request,'student/viewreview.html',{'data':data})

def add_complaint(request):
    form = complaintform()
    u = request.user
    if request.method=='POST':
        form = complaintform(request.POST)
        if form.is_valid():
            obj =form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request,'complaint added successfully')
            return redirect('base1')
    return render(request,'student/addcomplaint.html',{'form':form})

def view_complaint(request):
    data = Complaints.objects.filter(user=request.user)
    return render(request,'student/viewcomplaint.html',{'data':data})

