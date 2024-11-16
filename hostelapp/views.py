from django.contrib import auth, messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from hostelapp.forms import UserRegister, Studentform, parentform


# Create your views here.

def homepage(request):
    return render(request,'Modified_files/index.html')

def loginpage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request,user)
            return redirect('base')
        elif user is not None and user.is_warden:
            login(request,user)
            return redirect('wardenpage')
        elif user is not None and user.is_student:
            if user.student.approval_status==1:
                login(request,user)
                return redirect('base1')
            else:
                messages.info(request,"Your Are Not Approved To Login")
        elif user is not None and user.is_parent:
            if user.parent.approval_status==1:
                login(request,user)
                return redirect('parentpage')
            else:
                messages.info(request,"Your Are Not Approved To Login")
        else:
            messages.info(request, "Not Registered User")

    return render(request,'login.html')

def regis(request):
    return render(request,'register.html')

def stureg(request):
    u_form = UserRegister()
    s_form = Studentform()
    if request.method== 'POST':
        u_form=UserRegister(request.POST)
        s_form=Studentform(request.POST,request.FILES)
        if u_form.is_valid() and s_form.is_valid():
            user=u_form.save(commit=False)
            user.is_student = True
            user.save()
            student = s_form.save(commit=False)
            student.user= user
            student.save()
            messages.info(request,"student registered successfully")
            return redirect('loginpage')
    return render(request,'stureg.html',{'u_form':u_form,'s_form':s_form})

def wareg(request):
    return render(request,'wareg.html')
def pareg(request):
    u_form = UserRegister()
    p_form = parentform()
    if request.method=='POST':
        u_form=UserRegister(request.POST)
        p_form=parentform(request.POST,request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user=u_form.save(commit=False)
            user.is_parent=True
            user.save()
            parent=p_form.save(commit=False)
            parent.user=user
            parent.save()
            messages.info(request,"parent registered successfully")
            return redirect('loginpage')
    return render(request,'pareg.html',{'u_form':u_form,'p_form':p_form})

def adminpage(request):
    return render(request,'admin.html')

def parentpage(request):
    return render(request,'parent.html')

def studentpage(request):
    return render(request,'student.html')

def wardenpage(request):
    return render(request,'warden.html')

def log_out(request):
    logout(request)
    return redirect('homepage')