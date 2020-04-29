from django.shortcuts import render, get_object_or_404
from .models import Devotee_detail
from django.http import Http404
from .forms import BlogPostForm, BlogPostModelForm

def dev_detail_list_view(request):
    # list out the objects
    # could be search
    # qs = Devotee_detail.objects.all() #quesryset -> list all python objects[]
    qs = Devotee_detail.objects.filter(content__icontains = "ho") #quesryset -> list filter python objects[]
    template_name = "blog/list.html"
    context = {"object_list": qs}
    return render(request, template_name, context)

def dev_detail_create_view(request):
    form = BlogPostModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BlogPostModelForm()
        # obj = Devotee_detail.objects.create(**form.cleaned_data)
        # form = BlogPostForm()
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)

def dev_detail_view(request, dev_slug):# [for retrieve]
    obj = get_object_or_404(Devotee_detail, slug = dev_slug)
    template_name = "blog/detail.html"
    context = {"object" : obj}
    return render(request, template_name, context)


def dev_update_view(request, dev_slug):
    obj = get_object_or_404(Devotee_detail, slug = dev_slug)
    template_name = "blog/update.html"
    context = {"object": obj, "form":None}
    return render(request, template_name, context)

def dev_delete_view(request, dev_slug):
    obj = get_object_or_404(Devotee_detail, slug = dev_slug)
    template_name = "blog/delete.html"
    context = {"object": obj}
    return render(request, template_name, context)