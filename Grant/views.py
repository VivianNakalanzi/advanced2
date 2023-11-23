from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Grant.models import UserInfo, Application
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    return render(request, 'index.html')

def status(request):
    applications = Application.objects.all()
    return render(request, 'status.html',{'applications':applications})

@login_required
def apply(request):
    submitted= False
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/apply? submitted= True')
    else:
        form = ApplicationForm
        if submitted in request.GET:
            submitted =True

    return render(request, 'Apply.html', {'form':form, 'submitted':submitted})

def log_in(request):
    context={
            'data':request.POST,
            'has_error':False
        }
    username=request.POST.get('username')
    password=request.POST.get('password')
        
        
    try:
        user_details = User.objects.get(username=username)
        email = user_details.email
        user_email = User.objects.get(email=email)
        if not user_email.is_active:
            messages.add_message(request, messages.ERROR, 'Check your email to verify your account.')
    except Exception as identifier:
            pass

    if username=='':
        messages.add_message(request,messages.ERROR, 'Username is required.')
        context['has_error']=True

    if password=='':
        messages.add_message(request,messages.ERROR, 'Password is required.')
        context['has_error']=True

    user=authenticate(request, username=username, password=password)

    if not user and not context['has_error']:
        messages.add_message(request,messages.ERROR, 'Invalid login.')
        context['has_error']=True

    if context['has_error']:
        return render(request, 'login.html', status=401, context=context)
        
    login(request, user)
    return redirect('index')

def signup(request):
    context = {
        'data':request.POST,
        'has_error':False,
    }
    if request.method == "POST":
        name = request.POST.get('fullName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        organization_name= request.POST.get('organizationName')
        organization_type= request.POST.get('organizationType')

        try:
            if len(password1)<6:
                messages.add_message(request, messages.ERROR, 'Passwords should atleast be 6 characters long.')
                context['has_error']=True
        except Exception as identifier:
            pass

        if password1 != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match.')
            context['has_error']=True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken.')
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.ERROR, 'Username is taken.')
                context['has_error']=True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'signup.html', context, status=400)
        
        user=User.objects.create_user(username=username,email=email)
        user.set_password(password1)
        user.first_name=name
        
        details=UserInfo(user=user,fullname=name,email=email,organizationName=organization_name,organizationType=organization_type)
        details.save()
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Account is created successfully.')
        return render(request, "login.html", context)
    return render(request, "signup.html")


def log_out(request):
    if request.method == "GET":
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logged Out Successfully.')
        return render(request, 'login.html')
    