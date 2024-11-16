import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from hostelapp.models import User, Student, Hostel, food, Notification, Warden, Parent, Bookroom, Review, Complaints, \
    Attendance


class TimeInput(forms.TimeInput):
    input_type = 'time'

class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','password1','password2')

class Studentform(forms.ModelForm):
    class Meta:

        model = Student
        exclude = ('user','approval_status')

class parentform(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ('user','approval_status')
class add_hostel(forms.ModelForm):
    class Meta:
        model = Hostel
        fields='__all__'

class foodform(forms.ModelForm):
    class Meta:
        model = food
        fields= '__all__'


class Notificationform(forms.ModelForm):
    time=forms.TimeField(widget=TimeInput)
    to=forms.DateField(widget=DateInput)

    class Meta:
        model=Notification
        fields='__all__'

class wardenform(forms.ModelForm):
    class Meta:
        model = Warden
        exclude = ('user',)

class bookform(forms.ModelForm):
    booking_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Bookroom
        fields = ('booking_date',)

        def clean_date_joining(self):
            date = self.cleaned_data['booking_date']

            if date < datetime.date.today():
                raise forms.ValidationError("Invalid Date")
            return date


class reviewform(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('student',)


class complaintform(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ('complaint',)

attendnace_choice = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
)

class AddAttendanceForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(approval_status=True))
    attendance = forms.ChoiceField(choices=attendnace_choice, widget=forms.RadioSelect)

    class Meta:
        model = Attendance
        fields = ('student', 'attendance')