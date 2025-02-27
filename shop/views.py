from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from . import views
from .froms import SignUpForm, SignInForm

# Create your views here.

app_name = 'shop'

def index(request):
    return render(request, 'index.html')

def product(request, product_id: int):
    return render(request, 'product.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'signup.html', {'form': form})


    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})



# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('profile')

#     else:
#         form = SignInForm()
#     return render(request, 'signin.html', {'form': form})

# def signin(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)  # ✅ Use `data=request.POST`
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)  # ✅ Authenticate
#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')
#     else:
#         form = SignInForm()
#     return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('index')


def profile(request):
    return render(request, 'profile.html', {'user': request.user})




