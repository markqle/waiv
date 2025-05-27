# waivapp/LoginCheckMiddleWare.py

from django.urls           import reverse
from django.http           import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleWare(MiddlewareMixin):
    PUBLIC = {
        'show_login','do_login','logout',
        'admin:login','static','media',
    }
    MANAGER = {
        'admin_home','add_staff','add_staff_save',
        'add_student','add_student_save','manage_staff',
        'edit_staff','edit_staff_save',
        'manage_student','edit_student','edit_student_save',
        'import_monthly_client_listing','monthly_client_listing',
        'add_counseling','add_counseling_save','view_counseling',
        'create_monthly_report','monthly_report_detail',
    }
    COUNSELOR = {
        'staff_home',            # Home dashboard
        'staff_add_counseling',  # GET  /staff/add_counseling/
        'staff_add_counseling_save',  # POST /staff/add_counseling_save/
        'staff_view_counseling', # View counseling logs
        'staff_manage_student',  # Manage students list
        'staff_view_student',    # View a single student’s detail
        'staff_edit_student',
    }

    def process_view(self, request, view_func, view_args, view_kwargs):
        resolver = request.resolver_match
        name = resolver.url_name if resolver else None

        # 1) public pages never protected
        if name in self.PUBLIC:
            return None

        user = request.user
        # 2) anonymous → login
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse('show_login'))

        # 3) superusers and staff → full access
        if user.is_superuser or user.is_staff:
            return None

        # 4) case managers
        if user.position == 'case_manager':
            if name in self.MANAGER or name in self.PUBLIC:
                return None
            return HttpResponseRedirect(reverse('admin_home'))

        # 5) counselors
        if user.position == 'counselor':
            if name in self.COUNSELOR or name in self.PUBLIC:
                return None
            return HttpResponseRedirect(reverse('staff_home'))

        # 6) everything else → login
        return HttpResponseRedirect(reverse('show_login'))
