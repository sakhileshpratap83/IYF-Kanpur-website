from .models import Profile, Brother
from .forms import CreateProfileModelForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, BrotherForm, SigninForm, DevotionalForm, EducationForm, ProfessionForm 
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import  transaction
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse,QueryDict
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from xml.dom import minidom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import *
# import urllib2
# from django.contrib.auth.decorators import login_required
# from urllib.request import urlopen
# from django.shortcuts import render,redirect
# views always use pascal case


fromaddr='yogbulani@gmail.com'
username='yogbulani'
password='gtvrkzeyahnnvqzb'
# Microfb@108
# fromaddr='django.registeractivate@gmail.com'
# username='django.registeractivate'
# password='django_register_activate'



# class ProfileBrotherCreate(CreateView):
# 	model = Brother
# 	fields = ['user']
# 	success_url = reverse_lazy('profile')

# 	def get_context_data(self, **kwargs):
# 		data = super(ProfileBrotherCreate, self).get_context_data(**kwargs)
# 		if self.request.POST:
# 			data['brothers'] = BrotherFormSet(self.request.POST)
# 		else:
# 			data['brothers'] = BrotherFormSet()
# 		return data

# 	def form_valid(self, form):
# 		context = self.get_context_data()
# 		brothers = context['brothers']
# 		with transaction.atomic():
# 			self.object = form.save()

# 			if brothers.is_valid():
# 				brothers.instance = self.object
# 				brotherforms = brothers.save(commit = False)
# 				brothers.user = request.user
# 				brotherforms.save()
# 		return super(ProfileBrotherCreate, self).form_valid(form)


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
			# email = request.POST['email']
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




@login_required(login_url='/user/signin/')
def profile(request):
	# BroFormSet = inlineformset_factory(User, Brother, form = BrotherForm, fields=('brother_name','year_of_birth'), can_delete = True, extra =1, max_num = 5)
	if request.method == 'POST':
		# b_formset = BrotherFormset(request.POST, instance=request.user.profile.brother)
		u_form = UserUpdateForm(request.POST, instance=request.user)
		e_form = EducationForm(request.POST, instance=request.user)
		prof_form = ProfessionForm(request.POST, instance=request.user)
		d_form = DevotionalForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
								   request.FILES,
								   instance=request.user.profile)
		# b_formset = BroFormSet(request.POST, instance = request.user)
		if u_form.is_valid() and p_form.is_valid() and e_form.is_valid() and prof_form.is_valid() and d_form.is_valid():# and b_formset.is_valid():# and b_form.is_valid():
			u_form.save()
			p_form.save()
			e_form.save()
			prof_form.save()
			d_form.save()
			# b_formset.save()
			# for b_form in b_formset:
			# 	b_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('/user/brother')

	else:
		# b_formset = BrotherFormset(request.GET or None)
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		e_form = EducationForm(instance=request.user.education)
		prof_form = ProfessionForm(instance=request.user.profession)
		d_form = DevotionalForm(instance=request.user.devotional)
		# b_formset = BroFormSet(instance = request.user)
	context = {
		'u_form': u_form,
		'p_form': p_form,
		'e_form': e_form,
		'prof_form': prof_form,
		'd_form': d_form,
		# 'b_formset' : b_formset,
	}

	return render(request, 'user/profile copy.html', context)
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

@login_required
def brother(request):
	BroFormSet = inlineformset_factory(User, Brother, form = BrotherForm, fields=('brother_name','year_of_birth'), can_delete = True, extra =1, max_num = 5)
	if request.method == 'POST':
		b_formset = BroFormSet(request.POST, instance = request.user)
		if b_formset.is_valid():
			b_formset.save()
			# for b_form in b_formset:
			# 	b_form.save()
			messages.success(request, f'Your brother details has been updated!')
			return redirect('/user/brother')
	else:
		# b_formset = BrotherFormset(request.GET or None)
		b_formset = BroFormSet(instance = request.user)
	context = {
		'b_formset' : b_formset,
	}
	return render(request, 'user/brother.html', context)
	
# def brother(request):
# 	user = request.user
# 	broformset = inlineformset_factory(User, Brother, fields=('brother_name','year_of_birth'), can_delete = False, extra =1, max_num = 5)
# 	# print(user.username)
# 	if request.method == "POST":
# 		formset = broformset(request.POST, instance = user)# queryset = Brother.objects.filter(user = user))
# 		if formset.is_valid():
# 			formset.save()
# 			# instances = formset.save(commit=False) #if not commit, then it gives integrity error since it updated brother_name didn't got the user_id and it cannot be null
# 			# for instance in instances:
# 			# 	instance.user = user
# 			# 	instance.save()

# 			redirect('/user/brother')
# 	formset = broformset(instance = user)#queryset = Brother.objects.filter(user = user))

# 	return render(request, 'brother.html', {'formset':formset})


@staff_member_required
def counselees(request):# [for retrieve]
	# obj = get_object_or_404(Devotee_detail, slug = dev_slug)
	# list out the objects
	# could be search
	qs = User.objects.all() #queryset -> list all python objects[]
	# qs = Devotee_detail.objects.filter(conselor__icontains = "request.user.profile.full_name") #quesryset -> list filter python objects[]
	template_name = "user/counselees.html"
	context = {"counselees": qs}
	return render(request, template_name, context)