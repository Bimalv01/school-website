from multiprocessing import AuthenticationError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views import View
from .models import * 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView,CreateView,ListView
from .models import Student
from .forms import StudentForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import MaterialSearchForm
from .models import school_file
from django.shortcuts import render, redirect







# Create your views here.
def index(request):
    return render(request, 'index.html')

def download(request):
    data=school_file.objects.all()
    print(data)
    return render(request, 'download.html', {'data':data})

def userview(request):
    data=school_file.objects.all()
    print(data)
    return render(request, 'userview.html', {'data':data})




def upload(request):
    if request.method== 'POST':
        subject1=request.POST['subject']
        year1=request.POST['year']
        course1=request.POST['course']
        upload1=request.FILES['upload']
        new_school_file = school_file(subject_name=subject1, year=year1, course=course1,upload=upload1)
        new_school_file.save()
        
    return render(request, 'uploadfile.html')

 
def about(request):
    return render(request, 'about.html')

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('upload')
            else:
                return render(request, 'Login.html', {'form': form, 'error_message': 'Invalid credentials'})

    else:
        form = AuthenticationError()

    return render(request, 'Login.html', {'form': form})

#update
class Update_detail(UpdateView):
    model=school_file
    fields='__all__'
    template_name='update.html'
    success_url=reverse_lazy('download')
    
#delete
def delete(request,pk):
    de=school_file.objects.get(id=pk)
    de.delete()

    return redirect('download')

#studentreigister
def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/student-login/')
    else:
        form = StudentForm()

    return render(request, 'studentregister.html', {'form': form})




def approval(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        action = request.POST['action']
        student = Student.objects.get(id=student_id)

        if action == 'approve':
            student.is_approved = True
            student.save()

            # Send an email to the student
            send_mail(
               
                'Congratulations! Your registration has been approved',
                'Your User Roll Number is {} and your password is {}.'.format(student.roll_number, student.password),
                settings.EMAIL_HOST_USER,
                [student.email],
                fail_silently=False,
            )
        elif action == 'reject':
            student.delete()

    students = Student.objects.filter(is_approved=False)
    return render(request, 'approval.html', {'students': students})

#list of students in admin view
def studentview(request):
    data=Student.objects.all()
    print(data)
    return render(request, 'student_details.html', {'data':data})

#list of student
def registrationlist(request):
    data=Student.objects.all()
    print(data)
    return render(request, 'registrationlist.html', {'data':data})

#studlogin
def studentlogin(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(roll_number=roll_number, password=password)
            # Redirect to a profile page or any other page after successful login
            # For now, redirecting to a success message
            request.session['roll_number'] = student.id
            
            messages.success(request, f"Welcome, {student.name}!")
            return redirect('student_dashboard',student_id = student.id )  # Replace 'success_page' with your desired URL name
        except Student.DoesNotExist:
            messages.error(request, "Invalid roll number or password. Please try again.")

    return render(request, 'studentlogin.html')

#search materials 


def material_search(request):
    if request.method == 'POST':
        form = MaterialSearchForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data.get('subject_name')
            year = form.cleaned_data.get('year')
            course = form.cleaned_data.get('course')

            # Filter the files based on the provided criteria
            materials = school_file.objects.all()

            if subject_name:
                materials = materials.filter(subject_name__icontains=subject_name)
            if year:
                materials = materials.filter(year__icontains=year)
            if course:
                materials = materials.filter(course__icontains=course)

            return render(request, 'listmaterials.html', {'materials': materials, 'form': form})
    else:
        form = MaterialSearchForm()

    return render(request, 'material_search.html', {'form': form})

#edit profile
class edit_student(UpdateView):
    model = Student
    fields = ['name', 'email', 'parent_name', 'parent_contact']
    template_name = 'edit_student.html'
    
    def get_success_url(self):
        return reverse_lazy('student_dashboard', kwargs={'student_id': self.object.id})

#student dashboard
def student_dashboard(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_dashboard.html', {'student': student})
#
def listmaterials(request):
    student = request.user.student  # Assuming the student is logged in
    study_materials = student.study_materials.all()

    context = {'study_materials': study_materials}
    return render(request, 'userview.html', {'student': student, 'study_materials': study_materials})


def admin_logout(request):
    logout(request)
    # Redirect to a specific page after logout (you can change this to your desired URL)
    return redirect('Login') 

def feedback_view(request):
    return render(request, 'feedback.html')

def Contact(request):
    return render(request, 'Contact.html')

def staff(request):
    return render(request, 'staff.html')

def coures(request):
    return render(request, 'course.html')


#feedback
def FeedbackListView(request):
    
    data=Feedback.objects.all()
    return render(request,'feedback_list.html',{'feedbacks':data})




   
from datetime import datetime
def send_feedback(request):
    pk=request.session.get('roll_number')
    print(pk)
    if request.method =="POST":
        print('ok')
        data=Student.objects.filter(id=pk).first()
        feedback=request.POST.get("id_feedback")
        Feedback.objects.create(
            roll_number=pk,
            name=data.name,
            date=datetime.now(),
            feedback=feedback
            
        )
        
        print(data.name)
        
        return redirect(f'/student_dashboard/{pk}/')
    return render(request,'feedback_create.html')


class replay_feedback(UpdateView):
    model=Feedback
    fields=['admin_reply']
    template_name='admin_feedback_create .html'
    success_url=reverse_lazy('FeedbackListView')
    

def userFeedbackListView(request):
    
    pk=request.session.get('roll_number')
    data=Feedback.objects.filter(roll_number=pk)
    return render(request,'user_feedback_list .html',{'feedbacks':data})
