from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from ..decorators import student_required, admin_required
from ..forms import StudentSignUpForm,StudentSignUpTwo, StudentEditForm, StudentEditFormTwo
from ..models import Student, User, Homework, Notification, Marks, Attendance, Subject, Test,Timetable,Request


@login_required
def change_password(request):
    notification = Notification.objects.filter(school=request.user.school)[:5]
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('students:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'classroom/students/change_password.html', {
        'form': form, 'notification':notification
    })


@login_required
@admin_required
def StudentSignUpView(request):
    school = request.user.school
    if request.method == 'POST':
        main_form = StudentSignUpForm(request.POST)
        secondary_form = StudentSignUpTwo(request.user,request.POST,request.FILES)
        if main_form.is_valid() and secondary_form.is_valid():
            user = main_form.save(school)
            secondary_form.save(user)
            return redirect('admin:admin_home')
    else:
        main_form = StudentSignUpForm()
        secondary_form = StudentSignUpTwo(request.user)

    return render(request, 'classroom/registration/student_register.html', {
        'main_form': main_form,
        'secondary_form': secondary_form
    })


@login_required
@admin_required
def StudentEditView(request,username):
    if request.method == 'POST':
        edit_form = StudentEditForm(request.POST)
        edit_form_two = StudentEditFormTwo(username, request.POST,request.FILES)
        if edit_form.is_valid() and edit_form_two.is_valid():
            user = edit_form.save(username)
            edit_form_two.save(username)
            return redirect('admin:admin_home')
    else:
        edit_form = StudentEditForm()
        edit_form_two = StudentEditFormTwo(request.user)
    return render(request, 'classroom/registration/student_edit.html', {
        'edit_form': edit_form,
        'edit_form_two': edit_form_two
    })

@method_decorator([login_required], name='dispatch')
class StudentHomeView(ListView):
    model = Homework
    # ordering = ('name', )
    context_object_name = 'homework'
    template_name = 'classroom/students/student_home.html'
    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        homework = Homework.objects.filter(school=self.request.user.school)
        user = self.request.user
        return {'homework':homework, 'user': user, 'notification':notification}
 
class ProfileView(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'classroom/students/student_profile.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        student = Student.objects.filter(user=user)
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'student': student, 'user': user, 'notification':notification}

class NotificationView(ListView):
    model = Notification
    context_object_name = 'notification'
    template_name = 'classroom/students/student_notification.html'
    def get_context_data(self,**kwargs):
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'notification':notification}


class MarksView(ListView):
    model = Marks
    context_object_name = 'marks'
    template_name = 'classroom/students/student_marks.html'

    # def get_context_data(self,**kwargs):
    #     tests = Test.objects.all()
    #     student = Student.objects.filter(user=self.request.user)
    #     # marks = Marks.objects.filter(test=test, student=student)
    #     # for test in tests:
    #     #     marks = Marks.objects.filter(test=test, student=student)
    #     marks = Marks.objects.filter(student=student)
    #     return {'tests': tests, 'marks':marks}

def MarksPlot(request, marks):
    notification = Notification.objects.filter(school=self.request.user.school)[:5]
    return render(request, 'classroom/students/marks_plot.html', {
        'marks': marks, 'notification':notification
    })

    def get_context_data(self,**kwargs):
        marks = Marks.objects.filter(student__user=self.request.user)
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'marks':marks, 'notification':notification}

# >>>>>>> 1f170c1348cb7b23906f81139d1db1de0d4a904c

class TopperMarksView(ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'classroom/students/topper_marks_select_subject.html'


    def get_context_data(self,**kwargs):
        subjects = Subject.objects.filter(school=self.request.user.school)
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'subjects':subjects, 'notification':notification}

# class SelectTestView(ListView):
#     model = Test
#     context_object_name = 'tests'
#     template_name = 'classroom/students/topper_marks_select_test.html'

def SelectTestView(request, subject):
    subject = Subject.objects.get(name=subject,school=request.user.school)
    notification = Notification.objects.filter(school=request.user.school)[:5]
    print(subject.name)
    tests = Test.objects.all()
    print(tests)
    return render(request,'classroom/students/topper_marks_select_test.html',{
        'tests':tests, 'subject': subject, 'notification':notification
        })

def ComparisonView(request, subject, test):
    subject = Subject.objects.filter(name=subject,school=request.user.school)
    test = Test.objects.get(name=test)
    student = Student.objects.get(user=request.user)
    my_marks = Marks.objects.get(student=student)
    notification = Notification.objects.filter(school=self.request.user.school)[:5]
    # print(my_marks.Scored_marks, my_marks.test)
    marks = Marks.objects.all()
    max = 0
    for mark in marks:
        if mark.test == test and mark.Scored_marks > max:
            max = mark.Scored_marks
    print(my_marks.Scored_marks, max)
    return render(request,'classroom/students/topper_comparison.html',{
        'my_marks': my_marks.Scored_marks, 'topper': max, 'notification':notification
        })

def selectAttendanceSubject(request):
    Subjects = Subject.objects.filter(school=request.user.school);
    print(Subjects)
    notification = Notification.objects.filter(school=request.user.school)[:5]
    return render(request,'classroom/students/select-subject.html',{
        'subjects':Subjects, 'notification':notification
        })

def PieChartView(request, subject):
    student = Student.objects.get(user=request.user)
    subject = Subject.objects.get(name=subject,school=request.user.school)
    notification = Notification.objects.filter(school=self.request.user.school)[:5]
    print(subject)
    attendance = Attendance.objects.filter(student=student, Subject=subject)
    total = attendance.count()
    present = Attendance.objects.filter(student=student, Subject=subject, present=True).count()
    absent = Attendance.objects.filter(student=student, Subject=subject, present=False).count()
    print(attendance.count(), present, absent)
    return render(request,'classroom/students/pie.html',
        {'attendance' : attendance, 'total': total, 'present': present, 'absent': absent, 'notification':notification})

def ScatterPlotView(request, subject):
    student = Student.objects.get(user=request.user)
    subject = Subject.objects.get(name=subject,school=request.user.school)
    attendance = Attendance.objects.filter(student=student, Subject=subject)
    notification = Notification.objects.filter(school=self.request.user.school)[:5]
    # jan = 0, feb = 0, mar = 0, apr = 0, may = 0, june = 0, july = 0, aug = 0, sep = 0, oct = 0, nov = 0, dec = 0
    jan = 0
    feb = 0
    mar = 0
    apr = 0
    may = 0
    june = 0
    july = 0
    aug = 0
    sep = 0
    oct = 0
    nov = 0
    dec = 0
    for a in attendance:
        print(a.class_date.strftime("%d-%m"))
        month = a.class_date.strftime("%m")
        month = int(month[-1])
        print(month, a.present)
        if month == 1 and a.present:
            jan = jan + 1
        elif month == 2 and a.present:
            feb = feb + 1
        elif month == 3 and a.present:
            mar = mar + 1
        elif month == 4 and a.present:
            apr = apr + 1
        elif month == 5 and a.present:
            may = may + 1
        elif month == 6 and a.present:
            june = june + 1;
        elif month == 7 and a.present:
            july = july + 1
        elif month == 8 and a.present:
            aug = aug + 1
        elif month == 9 and a.present:
            sep = sep + 1
        elif month == 10 and a.present:
            oct = oct + 1
        elif month == 11 and a.present:
            nov = nov + 1
        elif month == 12 and a.present:
            dec = dec + 1
    print(mar)
    return render(request,'classroom/students/scatter.html',
        {'jan': jan, 'feb': feb, 'mar': mar, 'apr': apr, 'may': may, 'june': june, 'july': july, 'aug': aug, 'sep': sep, 'oct': oct, 'nov': nov, 'dec': dec, 'notification':notification})

def AttendanceView(request, subject):
    student = Student.objects.get(user=request.user)
    subject = Subject.objects.get(name=subject,school=user.school)
    # print(subject)
    attendance = Attendance.objects.filter(student=student, Subject=subject)
    notification = Notification.objects.filter(school=self.request.user.school)[:5]
    # total = attendance.count()
    # present = Attendance.objects.filter(student=student, Subject=subject, present=True).count()
    # absent = Attendance.objects.filter(student=student, Subject=subject, present=False).count()
    # print(attendance.count(), present, absent)
    return render(request,'classroom/students/student_attendance.html',
        {'attendance' : attendance, 'subject': subject, 'notification':notification})

@method_decorator([login_required], name='dispatch')
class TimetableListView(ListView):
    model = Timetable
    template_name = 'classroom/students/timetable.html'


    def get_context_data(self,**kwargs):
        student = Student.objects.get(user=self.request.user)
        timetable = Timetable.objects.filter(batch=student.batch)
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'timetable':timetable,'user':self.request.user, 'notification':notification}

      
@method_decorator([login_required], name='dispatch')
class RequestView(ListView):
    model = Request
    context_object_name = 'requests'
    template_name = 'classroom/students/requests_list.html'

    def get_context_data(self,**kwargs):
        requests = Request.objects.filter(owner=self.request.user)
        notification = Notification.objects.filter(school=self.request.user.school)[:5]
        return {'requests':requests, 'notification':notification}