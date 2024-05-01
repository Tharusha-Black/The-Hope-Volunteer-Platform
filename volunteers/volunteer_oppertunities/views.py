from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import VolunteerOpportunityForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import VolantProjects, VolantDetails
from django.utils import timezone



def is_superuser(user):
    return user.is_superuser

class CreateOpportunityView(View):
    @method_decorator(user_passes_test(is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = VolunteerOpportunityForm()
        return render(request, 'volunteer_oppertunities/volunt_oppertunity_form.html', {'form': form})

    def post(self, request):
        form = VolunteerOpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer opportunity created successfully!')
            return redirect('volunteer_opportunities:opportunity_list') 
        return render(request, 'volunteer_oppertunities/volunt_oppertunity_form.html', {'form': form})

class UpdateOpportunityView(View):
    @method_decorator(user_passes_test(is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk):
        opportunity = get_object_or_404(VolantProjects, pk=pk)
        form = VolunteerOpportunityForm(instance=opportunity)
        return render(request, 'volunteer_oppertunities/volunt_oppertunity_form.html', {'form': form, 'opportunity': opportunity})

    def post(self, request, pk):
        opportunity = get_object_or_404(VolantProjects, pk=pk)
        form = VolunteerOpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer opportunity updated successfully!')
            return redirect('volunteer_opportunities:opportunity_list') 
        return render(request, 'volunteer_oppertunities/volunt_oppertunity_form.html', {'form': form, 'opportunity': opportunity})


class DeleteOpportunityView(View):
    def get(self, request, pk):
       pass

    def post(self, request, pk):
        # Retrieve the project object or return 404 if not found
        opportunity = get_object_or_404(VolantProjects, pk=pk)
        # Delete the project
        opportunity.delete()
        # Optionally, add a success message
        messages.success(request, 'Volunteer opportunity deleted successfully!')
        # Redirect to the opportunity list page or any other desired page
        return redirect('volunteer_opportunities:opportunity_list')


class OpportunityListView(View):
    def get(self, request):
        # Get distinct project types
        distinct_project_types = dict(VolantProjects.PROJECT_TYPES)
        distinct_cities = dict(VolantProjects.CITY_CHOICES)
        distinct_regions = dict(VolantProjects.REGION_CHOICES)
        opportunities = VolantProjects.objects.all()

        # Get sorting criteria from request parameters
        sort_type = request.GET.get('sort_type')
        sort_city = request.GET.get('sort_city')
        sort_region = request.GET.get('sort_region')
        
        filters = {}
        if sort_type:
            filters['project_type'] = sort_type
        if sort_city:
            filters['city'] = sort_city
        if sort_region:
            filters['region'] = sort_region
        
        if filters:
            opportunities = opportunities.filter(**filters)

        opportunity_data = []
        for opportunity in opportunities:
            joined_members_count = VolantDetails.objects.filter(project=opportunity).count()
            user_has_joined = VolantDetails.objects.filter(project=opportunity, user=request.user).exists()
            opportunity_data.append({
                'opportunity': opportunity,
                'joined_members_count': joined_members_count,
                'user_has_joined': user_has_joined
            })
        return render(request, 'volunteer_oppertunities/oppertunity_list.html', {
            'opportunity_data': opportunity_data, 
            'distinct_project_types': distinct_project_types, 
            'distinct_cities': distinct_cities, 
            'distinct_regions': distinct_regions,
            })
    
class JoinOpportunityConfirmView(View):
    template_name = 'volunteer_oppertunities/join_confirm.html'

    def get(self, request, pk):
        opportunity = get_object_or_404(VolantProjects, pk=pk)
        return render(request, self.template_name, {'opportunity': opportunity})

    def post(self, request, pk):
        opportunity = get_object_or_404(VolantProjects, pk=pk)
        
        # Check if the user is already registered for the project
        if VolantDetails.objects.filter(project=opportunity, user=request.user).exists():
            messages.error(request, 'You have already joined this opportunity!')
            return redirect('volunteer_opportunities:opportunity_list')
        
        # Create a new VolantDetails object
        VolantDetails.objects.create(project=opportunity, user=request.user, joined_date=timezone.now())
        messages.success(request, 'You have joined the opportunity successfully!')
        return redirect('volunteer_opportunities:opportunity_list')






