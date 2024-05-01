from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VolantUserCreationForm
from volunteer_oppertunities.models import VolantProjects, VolantDetails
from .models import VolantUser
from django.utils import timezone



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get the user's projects
        user_project_ids = VolantDetails.objects.filter(user=user).values_list('project_id', flat=True)
        user_projects = VolantProjects.objects.filter(id__in=user_project_ids)
        user_projects_count = VolantProjects.objects.filter(id__in=user_project_ids).count()

        # Count the objects where status is True
        status_true_count = user_projects.filter(status=True).count()
        if 2 > status_true_count:
            volunteer_rank = "Volant X - Silver Volunteer"
        elif 5 > status_true_count:
            volunteer_rank = "Volant X - Gold Volunteer"
        elif 10 > status_true_count:
            volunteer_rank = "Volant X - Rising Star Volunteer"
        elif 20 > status_true_count:
            volunteer_rank = "Volant X - Community Champion" 
        elif 50 > status_true_count:
            volunteer_rank = "Volant X - Inspirational Leader"                

        # Check if the user is currently online based on their last login time
        now = timezone.now()
        last_login = user.last_login
        time_difference = now - last_login
        online_status = time_difference.total_seconds() <= 300  # Considered online if last login within 5 minutes (300 seconds)
        
        print(online_status)
        # Get all users except the current user
        all_users = VolantUser.objects.exclude(pk=user.pk)
        
        context['user'] = user
        context['user_projects'] = user_projects
        context['all_users'] = all_users
        context['status_true_count'] = status_true_count
        context['volunteer_rank'] = volunteer_rank
        context['online_status'] = online_status
        context['user_projects_count'] = user_projects_count

        return context

class HomeView(View):
    """
    View for the dashboard page, accessible only to logged-in users.
    """
    def get(self, request):
        return render(request, 'main/index.html')

class SignupView(View):
    """
    View for user signup.
    """
    def get(self, request):
        form = VolantUserCreationForm()
        return render(request, 'user_management/signup.html', {'form': form})

    def post(self, request):
        form = VolantUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'user_management/signup.html', {'form': form})

class LoginView(View):
    """
    View for user login.
    """
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'user_management/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('volunteer_opportunities:opportunity_list')
            else:
                return redirect('volunteer_opportunities:opportunity_list')
        return render(request, 'user_management/login.html', {'form': form})


class LogoutView(View):
    """
    View for user logout.
    """
    def get(self, request):
        logout(request)
        return redirect('home')
