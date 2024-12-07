from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Student  # Assuming you have a Student model to fetch student data
from django.contrib.auth import authenticate, login, logout
def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def login_user(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('students')
            else:
                return render(request, 'login.html', {'error': 'Your account is disabled.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home') 

def register(request):
    """Render the registration page and handle user sign-up."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def students(request):
    """Render the students page showing student details, only accessible to logged-in users."""
    students_list = Student.objects.all()  # Fetch all students from the database
    return render(request, 'students.html', {'students': students_list})