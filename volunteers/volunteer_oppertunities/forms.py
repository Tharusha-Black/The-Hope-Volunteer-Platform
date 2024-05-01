from django import forms
from .models import VolantProjects

class VolunteerOpportunityForm(forms.ModelForm):
    class Meta:
        model = VolantProjects
        fields = ['project_name', 'project_type', 'project_objective', 'project_description', 'city', 'region', 'end_date', 'members_required', 'status']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=VolantProjects.STATUS_CHOICES),  # Add widget for status field
        }

    def clean(self):
        cleaned_data = super().clean()
        project_objective = cleaned_data.get('project_objective')
        descriptions = {
            'community_service': 'Opportunities that involve directly assisting local communities through activities such as food distribution, clothing drives, community clean-ups, and neighborhood revitalization projects.',
            'education_and_tutoring': 'Volunteering to support educational initiatives, such as tutoring students, assisting teachers in classrooms, leading workshops, or participating in literacy programs.',
            'healthcare_and_wellness': 'Volunteering in healthcare settings such as hospitals, clinics, or nursing homes to provide support to patients, assist medical staff, or promote wellness initiatives.',
            'environmental_conservation': 'Opportunities focused on protecting and preserving the environment through activities such as tree planting, wildlife habitat restoration, beach clean-ups, or promoting sustainability initiatives.',
            'animal_welfare': 'Volunteering with animal shelters, rescue organizations, or wildlife sanctuaries to care for animals, assist with adoption events, or participate in animal rehabilitation efforts.',
            'advocacy_and_human_rights': 'Volunteering with advocacy groups, nonprofits, or NGOs to promote social justice, human rights, and equality through activities such as lobbying, fundraising, awareness campaigns, or community organizing.',
            'arts_and_culture': 'Volunteering in museums, galleries, theaters, or cultural centers to support artistic and cultural programs, assist with events, provide guided tours, or contribute to creative projects.',
            'disaster_relief_and_emergency_response': 'Volunteering with organizations involved in disaster preparedness, response, and recovery efforts, including providing aid to affected communities, distributing supplies, or assisting with rescue and recovery operations.',
            'technology_and_digital_skills': 'Volunteering to help organizations with technology-related tasks such as website development, social media management, digital marketing, IT support, or teaching digital literacy skills.',
            'mentoring_and_youth_development': 'Volunteering to mentor young people, provide guidance and support in academic or personal development, lead youth programs, or serve as a positive role model.',
            'international_volunteerism': 'Opportunities to volunteer abroad or participate in international development projects, including humanitarian aid, healthcare missions, education programs, or sustainable development initiatives.',
            'virtual_volunteering': 'Opportunities that can be done remotely or online, such as virtual tutoring, remote administrative support, graphic design, translation, or social media management.'
        }
        description = descriptions.get(project_objective, '')
        cleaned_data['project_description'] = description
        return cleaned_data
