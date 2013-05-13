__author__ = 'Dandelin'
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from forms import MyRegisterationForm

def home(request):
    return render_to_response('home.html',  {'user': request.user})

def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return render_to_response('home.html',  {'user': request.user})
    else:
        return HttpResponseRedirect('/accounts/login')

def logout(request):
    auth.logout(request)
    return render_to_response('home.html')

def register_user(request):
    if request.method=='POST':
        form=MyRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    args={}
    args.update(csrf(request))
    args['form']=MyRegisterationForm()
    return render_to_response('register.html', args)