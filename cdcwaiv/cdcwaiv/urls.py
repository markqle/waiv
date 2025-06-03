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
from waivapp import views, manager, StaffViews
from cdcwaiv import settings

urlpatterns = [
#   Manager URL path
    path('admin/', admin.site.urls),
    path('demo', views.showDemoPage),
    path('', views.showLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', manager.admin_home, name = "admin_home"),
    path('add_staff', manager.add_staff, name="add_staff"),
    path('add_staff_save', manager.add_staff_save, name="add_staff_save"),
    path('add_student', manager.add_student, name="add_student"),
    path('add_student_save', manager.add_student_save, name="add_student_save"),
    path('add_counseling', manager.add_counseling, name="add_counseling"),
    path('add_counseling_save', manager.add_counseling_save, name="add_counseling_save"),
    path('import_monthly_client_listing/',manager.import_monthly_client_listing, name='import_monthly_client_listing'),
    path('import_checkin_simplicity/',manager.import_checkin_simplicity,name='import_checkin_simplicity'),
    path('monthly_client_listing/', manager.monthly_client_listing, name='monthly_client_listing'),
    path('checkin_simplicity/', manager.checkin_simplicity, name='checkin_simplicity'),
    path('manage_staff', manager.manage_staff, name="manage_staff"),
    path('edit_staff/<str:staff_id>', manager.edit_staff, name="edit_staff"),
    path('edit_staff_save', manager.edit_staff_save, name="edit_staff_save"),
    path('manage_student/', manager.manage_student, name='manage_student'),
    path('edit_student/<str:csulb_id>/', manager.edit_student, name='edit_student'),
    path('edit_student/<str:csulb_id>/save/', manager.edit_student_save, name='edit_student_save'),
    path('view_counseling', manager.view_counseling, name="view_counseling"),
    path('create_monthly_report/', manager.create_monthly_report,name='create_monthly_report'),
    path('monthly_report_detail/',manager.monthly_report_detail,name='monthly_report_detail'),

#   Staff URL path
    # STAFF HOME
    path('staff/home/',          StaffViews.staff_home,           name='staff_home'),

    # COUNSELING
    path('staff/add_counseling/',       StaffViews.add_counseling,      name='staff_add_counseling'),
    path('staff/add_counseling_save/',  StaffViews.add_counseling_save, name='staff_add_counseling_save'),
    path('staff/view_counseling/',      StaffViews.view_counseling,     name='staff_view_counseling'),

    # STUDENTS
    path('staff/manage_student/',          StaffViews.manage_student,      name='staff_manage_student'),
    path('staff/edit_student/<str:csulb_id>/',       StaffViews.edit_student,      name='staff_edit_student'),
    path('staff/edit_student/<str:csulb_id>/save/',  StaffViews.edit_student_save, name='staff_edit_student_save'),


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
