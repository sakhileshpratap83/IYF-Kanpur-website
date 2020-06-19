from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# don't repeat yourself = DRY
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from IYF_K.forms import SignUpForm

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})


# @login_required
# @staff_member_required
def home_page(request):
    var = "hello there..."#acting as second element of dictionary
    # doc = "<h1>{title}</h1>".format(title=title)
    context = {"title": var}
    if request.user.is_authenticated:
        context = {"title": var, "mylist": [1,2,3,4]}
    return render(request, "home.html", context)#title here will act as variable passed as dictionary to html page

def about_page(request):
    var = "About"  # acting as second element of dictionary
    return render(request, "about.html", {"title": var})

def aboutSP_page(request):
    var = "Srila Prabhupada"
    return render(request, "aboutSP.html", {"title" : var})

def contact_page(request):
    var = "Contact Us"  # acting as second element of dictionary[called context]
    form = ContactForm(request.POST or None) #making a data in the form of dictionary which can be passed as context
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    # doc = "<h1>{title}</h1>".format(title=title)
    context = {"title": var,
        "form": form,
    }
    return render(request, "form.html", context)


def diff_render_page(request):
    context 		= {"title":"this is a string from txt file"}
    template_name 	= "hello_world.html"
    template_obj 	= get_template(template_name)
    rendered_item 	= template_obj.render(context)
    # doc = "<h1>{title}</h1>".format(title=title)
    return HttpResponse(rendered_item)