"""IYF_K URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from user.views import(
	profile_create	
	)

from django.conf.urls import url, include 


from blog.views import (
	dev_detail_create_view,

)
# from django.conf.urls import url
# import IYF_K.views as core_views


from .views import (
	home_page,
	about_page,
	contact_page,
	diff_render_page,
	)

urlpatterns = [

	path('', home_page),
	# path('login/', login)
	path('blog-new/', dev_detail_create_view),
	path('blog/', include('blog.urls')),
	path('user/profile/', profile_create),
	path('user/', include('user.urls')),
    # re_path(r'^blog/(?P<post_id>\w+)/$', indDevoteeDetailPage),
	re_path(r'^pages?',about_page),
	path('about/', about_page),
	path('contact/', contact_page),
	path('diff_render_page/', diff_render_page),
    path('admin/', admin.site.urls),
    # url(r'^signup/$', core_views.signup, name='signup'),
   	#re_path(r'^register_activate/',include('register_activate.urls')),
    # re_path(r'^admin/', admin.site.urls),
]
