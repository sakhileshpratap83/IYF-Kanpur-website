from django.shortcuts import render, redirect
from .models import Profile, Brother
from .forms import CreateProfileModelForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, BrotherFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import  transaction
# views always use pascal case
from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse,QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import *
from django.views.generic.edit import CreateView
# import urllib2
# from urllib.request import urlopen
from xml.dom import minidom
from django.urls import reverse_lazy
from .forms import SigninForm
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


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user_instance=form.save()
			username=request.POST['username']
			password=request.POST['password1']
			user=authenticate(username=username,password=password)
			#The user is not active until they activate their account through email
			user.is_active=False
			user.save()
			id=user.id
			email=user.email
			send_email(email,id)
			messages.success(request, f'Email has been sent on {email} for confirmation.!')
			return render(request,'home.html')
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html', {'form': form})

# def sign_up(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user_instance=form.save()
#             username=request.POST['username']
#             password=request.POST['password']
#             user=authenticate(username=username,password=password)
#             #The user is not active until they activate their account through email
#             user.is_active=False
#             user.save()
#             id=user.id
#             email=user.email
#             send_email(email,id)
#             return render(request,'thankyou.html')
#         else:
#             return render(request,'sign_up.html',{'form':form})
#     else:
#         form = SignupForm()
#         return render(request,'sign_up.html',{'form':form})


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
					messages.success(request, f'Hare Krishna {username} prabhu!!! Welcome to Radha Madhav\'s abord!')
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
	msg="""From: %s\nTo: %s\nSubject: %s\n\n%s""" %(fromaddr,toaddr,subject,msg.as_string())
	#Use gmail's smtp server to send email. However, you need to turn on the setting "lesssecureapps" following this link:
	#https://www.google.com/settings/security/lesssecureapps
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr,[toaddr],msg)
	server.quit()


class ProfileBrotherCreate(CreateView):
    model = Brother
    fields = ['profile']
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        data = super(ProfileBrotherCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['brothers'] = BrotherFormSet(self.request.POST)
        else:
            data['brothers'] = BrotherFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        brothers = context['brothers']
        with transaction.atomic():
            self.object = form.save()

            if brothers.is_valid():
                brothers.instance = self.object
                brothers.save()
        return super(ProfileBrotherCreate, self).form_valid(form)


@login_required(login_url='/user/signin/')
def profile(request):
	if request.method == 'POST':
		# b_formset = BrotherFormset(request.POST, instance=request.user.profile.brother)
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
								   request.FILES,
								   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():# and b_form.is_valid():
			u_form.save()
			p_form.save()
			# for b_form in b_formset:
			# 	b_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		# b_formset = BrotherFormset(request.GET or None)
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form,
	}

	return render(request, 'user/profile.html', context)
	# form = CreateProfileModelForm(request.POST or None)
	# if form.is_valid():
	#     form.save()
	#     form = CreateProfileModelForm()
	#     # obj = Devotee_detail.objects.create(**form.cleaned_data)
	#     # form = BlogPostForm()
	# template_name = "user/profile.html"
	# context = {"title":"Sign Up",
	# 			"form": form,
	# 			}

	# return render(request, template_name, context)

# def create_brother(request):
#     template_name = 'user/brother.html'
#     heading_message = 'Brother Details'
#     if request.method == 'GET':
#         formset = BrotherFormset(request.GET or None)
#     elif request.method == 'POST':
#         formset = BrotherFormset(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 # extract name from each form and save
#                 brother_name = form.cleaned_data.get('brother_name')
#                 # save book instance
#                 if brother_name:
#                     Brother(brother_name=brother_name).save()
#             # once all books are saved, redirect to book list view
#             return redirect('user/profile')
#     return render(request, template_name, {
#         'formset': formset,
#         'heading': heading_message,
#     })



@staff_member_required
def counselees(request):# [for retrieve]
	# obj = get_object_or_404(Devotee_detail, slug = dev_slug)
	# list out the objects
	# could be search
	qs = User.objects.all() #quesryset -> list all python objects[]
	# qs = Devotee_detail.objects.filter(conselor__icontains = "request.user.profile.full_name") #quesryset -> list filter python objects[]
	template_name = "user/counselees.html"
	context = {"counselees": qs}
	return render(request, template_name, context)