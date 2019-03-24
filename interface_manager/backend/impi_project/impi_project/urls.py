"""impi_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from interface_app.views import user_views
from interface_app.views.service.service_detail_views import ServiceDetailViews
from interface_app.views.service.service_list_views import ServiceListViews
from interface_app.views.interface.interface_list_views import InterfaceListViews
from interface_app.views.interface.interface_detail_views import InterfaceDetailViews
from interface_app.views.service.service_interface_detail_views import ServiceInterfaceDetailViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/user/', user_views.UserViews.as_view()),

    path('backend/services/', ServiceListViews.as_view()),
    path('backend/services/<int:pk>', ServiceDetailViews.as_view()),
    path('backend/services/<int:pk>/interfaces', ServiceInterfaceDetailViews.as_view()),

    path('backend/interfaces/', InterfaceListViews.as_view()),
    path('backend/interfaces/<int:pk>', InterfaceDetailViews.as_view()),
]
