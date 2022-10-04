from urllib.request import Request
from django.shortcuts import render
from django.contrib.auth import logout
# Create your views here.
from curses.ascii import US
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import  UserRegisterForm , UserChangeForm
from django.contrib.auth.decorators import  login_required
# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from .models import  CustomUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required



@staff_member_required(login_url='login')
def register(request):
    if request.method == 'POST':
        # print(request.POST)
        form = UserRegisterForm(request.POST)
        # print(form.errorlist)
        if form.is_valid():
            # print(form.email)
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return render(request, 'users/create_accounts.html', {'done': f'{email}'})
#  redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/create_accounts.html', {'form': form})

def login_method(request):
    if request.user.is_authenticated:
        return redirect('ad-home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):    
                return redirect(request.GET.get('next'))
            else:
                return redirect('ad-home')
        else:
            try:
                my_user = CustomUser.objects.get(email=email)
                if my_user.is_active == False:
                    return render(request, 'users/login.html',{'messege':"account is deavtivated "})
                else:
                    return render(request, 'users/login.html',{'messege':"Password is incorrect"})
            except:
                return render(request, 'users/login.html',{'messege':"Email not found"})
            
    return render(request, 'users/login.html')

def logout_method(request):
    logout(request)
    return redirect('login')

@staff_member_required(login_url='login')
def all_users(request):
     if request.method == 'POST':
         
        if request.POST.get('switch' , '') != '':
            state = CustomUser.objects.get(id=request.POST.get('switch')).is_active
            CustomUser.objects.filter(id=request.POST.get('switch')).update(is_active = not(state))
        elif request.POST.get('delete' , '') != '':
            CustomUser.objects.get(id=request.POST.get('delete')).delete()
            

     users = CustomUser.objects.all()
     return render(request, 'users/accounts.html',{'users':users})
    
        # Return an 'invalid login' error message.
@staff_member_required(login_url='login')
def change_profile(request,email):
    error = None
    print(request.POST)
    
    try:
        my_user = CustomUser.objects.get(email=email)
        
        print(email)
    except:
        return redirect('users_page')
    if request.method == "POST":
        # name CustomUser.objects.filter(email=email).update(name = request.POST.get('name'))
        
        my_user = CustomUser.objects.get(email=email)
        print('here')
        if request.POST.get('switch' , '') != '':
            my_user = CustomUser.objects.get(email=email)
            state = CustomUser.objects.get(email=email).is_active
            CustomUser.objects.filter(email=email).update(is_active = not(state))
            return redirect('users_page')
        if request.POST.get('delete' , '') != '':
            CustomUser.objects.get(email=email).delete()
            return redirect('users_page')
        if request.POST.get('admin' , '') != '':
            my_user = CustomUser.objects.get(email=email)
            state = CustomUser.objects.get(email=email).is_staff
            CustomUser.objects.filter(email=email).update(is_staff = not(state))
            return redirect('users_page')
        if request.POST.get('name' , '') != '':
            my_user.name = request.POST.get('name')
        if request.POST.get('email' , '') != '':
            new_email = request.POST.get('email')
            qs = CustomUser.objects.filter(email=new_email)  
            if qs.exists():  
                error = "Email is taken"
                # my_user.email = new_email
                render(request, 'users/edit_accounts.html',{'my_user':my_user,'error':error})
            else:
                my_user.email = new_email
        
        if request.POST.get('password' ,'') != '':
            try:
                password = request.POST.get('password')
                validate_password(password,my_user)
                my_user.set_password(password)
                my_user.save()
            except Exception as e:
                error = e
        my_user.save()
        

    return render(request, 'users/edit_accounts.html',{'my_user':my_user,'error':error})