from django.shortcuts import render, redirect
# from django.shortcuts import render, get_object_or_404
from .models import Profile
# from django.http import Http404
# from .forms import BlogPostForm, BlogPostModelForm
from .forms import CreateProfileModelForm
from django.contrib.auth.decorators import login_required
# views always use pascal case
# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse,QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import *
# import urllib2
# from urllib.request import urlopen
from xml.dom import minidom
from .forms import SignupForm, SigninForm
from django.db.models import Count
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import get_object_or_404


fromaddr='yogbulani@gmail.com'
username='yogbulani'
password='gtvrkzeyahnnvqzb'
# Microfb@108
# fromaddr='django.registeractivate@gmail.com'
# username='django.registeractivate'
# password='django_register_activate'


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_instance=form.save()
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            #The user is not active until they activate their account through email
            user.is_active=False
            user.save()
            id=user.id
            email=user.email
            send_email(email,id)
            return render(request,'thankyou.html')
        else:
            return render(request,'sign_up.html',{'form':form})
    else:
        form = SignupForm()
        return render(request,'sign_up.html',{'form':form})


def activate(request):
    id=int(request.GET.get('id'))
    user = User.objects.get(id=id)
    user.is_active=True
    user.save()
    return render(request,'activation.html')


def sign_in(request):
    if request.method=='POST':
        form=SigninForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:                                          #Make sure the account is activated
                    login(request,user)
                    return redirect('/')
        
                else:
                    return render(request,'ErrorPage.html')
            else:
                return render(request,'ErrorPage.html',{'errormessage':'Invalid login'})
        else:
            return render(request,'sign_in.html',{'form':form})
    else:
        form=SigninForm()
        return render(request,'sign_in.html',{'form':form})


@login_required(login_url='/user/signin/')
def mainpage(request):
    if request.method == 'GET':
        message="You are logged in successfully"
        return render(request,'mainpage.html',{'user':request.user,'message':message})
    elif request.method =='POST':
        if request.POST.get("logout"):
            return redirect('user:logout')
        else:
            return redirect('user:thankyou')


def log_out(request):
    logout(request)
    return render(request,'log_out.html')


def send_email(toaddr,id):
    text = "Hare Krishna!\nAll glories to Srila Prabhupada\nAll glories to Lord Gauranga\nHere is the link to activate your account:\nhttp://127.0.0.1:8000/user/activation/?id=%s" %(id)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg.attach(part1)
    subject="Activate your account at IYF Kanpur"
    msg="""\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(fromaddr,toaddr,subject,msg.as_string())
    #Use gmail's smtp server to send email. However, you need to turn on the setting "lesssecureapps" following this link:
    #https://www.google.com/settings/security/lesssecureapps
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr,[toaddr],msg)
    server.quit()

@login_required(redirect_field_name=None)
def profile_create(request):
    form = CreateProfileModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CreateProfileModelForm()
        # obj = Devotee_detail.objects.create(**form.cleaned_data)
        # form = BlogPostForm()
    template_name = "signup.html"
    context = {"title":"Sign Up",
    			"form": form,
    			}
    return render(request, template_name, context)
