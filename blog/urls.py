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
from django.urls import path
from .views import (
	dev_detail_list_view,
	dev_detail_view,
	dev_update_view,
	dev_delete_view,
)

urlpatterns = [

	path('', dev_detail_list_view),
	path('<str:dev_slug>/', dev_detail_view),
	path('<str:dev_slug>/edit', dev_update_view),
	path('<str:dev_slug>/delete', dev_delete_view),

]
