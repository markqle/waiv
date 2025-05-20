"""
URL configuration for cdcwaiv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from waivapp import views, manager
from cdcwaiv import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo', views.showDemoPage),
    path('', views.showLoginPage),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user),
    path('doLogin', views.doLogin),
    path('admin_home', manager.admin_home),
    path('add_staff', manager.add_staff),
    path('add_staff_save', manager.add_staff_save),
    path('add_student', manager.add_student),
    path('add_student_save', manager.add_student_save),
    path('add_counseling', manager.add_counseling),
    path('add_counseling_save', manager.add_counseling_save),
    path('import_monthly_client_listing/',manager.import_monthly_client_listing, name='import_monthly_client_listing'),
    path('monthly_client_listing/', manager.monthly_client_listing, name='monthly_client_listing'),
    path('manage_staff', manager.manage_staff),
    path('edit_staff/<str:staff_id>', manager.edit_staff),
    path('edit_staff_save', manager.edit_staff_save),
    path('manage_student/', manager.manage_student, name='manage_student'),
    path('edit_student/<str:csulb_id>/', manager.edit_student, name='edit_student'),
     path('edit_student/<str:csulb_id>/save/', manager.edit_student_save, name='edit_student_save'),
    path('view_counseling', manager.view_counseling),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
