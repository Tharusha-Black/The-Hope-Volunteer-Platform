from django.db import models
from django.utils import timezone
from django.conf import settings

class VolantProjects(models.Model):
    PROJECT_TYPES = [
        ('one_time', 'One Time'),
        ('long_term', 'Long Term'),
        ('ongoin', 'Ongoing')
    ]
    PROJECT_OBJECTIVES_TYPES = [
        ('community_service', 'Community Service'),
        ('education_and_tutoring', 'Education and Tutoring'),
        ('healthcare_and_wellness', 'Healthcare and Wellness'),
        ('environmental_conservation', 'Environmental Conservation'),
        ('animal_welfare', 'Animal Welfare'),
        ('advocacy_and_human_rights', 'Advocacy and Human Rights'),
        ('arts_and_culture', 'Arts and Culture'),
        ('disaster_relief_and_emergency_response', 'Disaster Relief and Emergency Response'),
        ('technology_and_digital_skills', 'Technology and Digital Skills'),
        ('mentoring_and_youth_development', 'Mentoring and Youth Development'),
        ('international_volunteerism', 'International Volunteerism'),
        ('virtual_volunteering', 'Virtual Volunteering'),
    ]
    CITY_CHOICES = [
        ('colombo', 'Colombo'),
        ('gampaha', 'Gampaha'),
        ('kalutara', 'Kalutara'),
        ('kandy', 'Kandy'),
        ('matale', 'Matale'),
        ('nuwara_eliya', 'Nuwara Eliya'),
        ('galle', 'Galle'),
        ('matara', 'Matara'),
        ('hambantota', 'Hambantota'),
        ('jaffna', 'Jaffna'),
        ('mannar', 'Mannar'),
        ('vavuniya', 'Vavuniya'),
        ('mullaitivu', 'Mullaitivu'),
        ('kilinochchi', 'Kilinochchi'),
        ('batticaloa', 'Batticaloa'),
        ('ampara', 'Ampara'),
        ('trincomalee', 'Trincomalee'),
        ('kurunegala', 'Kurunegala'),
        ('puttalam', 'Puttalam'),
        ('anuradhapura', 'Anuradhapura'),
        ('polonnaruwa', 'Polonnaruwa'),
        ('badulla', 'Badulla'),
        ('moneragala', 'Moneragala'),
        ('ratnapura', 'Ratnapura'),
        ('kegalle', 'Kegalle'),
    ]

    REGION_CHOICES = [
        ('sabaragamuwa_province', 'Sabaragamuwa Province'),
        ('uva_province', 'Uva Province'),
        ('central_province', 'Central Province'),
        ('eastern_province', 'Eastern Province'),
        ('northern_province', 'Northern Province'),
        ('southern_province', 'Southern Province'),
        ('western_province', 'Western Province'),
        ('north_western_province', 'North Western Province'),
        ('north_central_province', 'North Central Province'),
    ]
    STATUS_CHOICES = [
        (True, 'Completed'),
        (False, 'Incompleted'),
    ]
    project_name = models.CharField(max_length=100)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    project_objective = models.CharField(max_length=50, choices=PROJECT_OBJECTIVES_TYPES)
    project_description = models.TextField()
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default="colombo")
    region = models.CharField(max_length=50, choices=REGION_CHOICES, default="westren_province")
    open_date = models.DateField(default=timezone.now)  # Change to DateField
    end_date = models.DateField()  # Change to DateField
    members_required = models.IntegerField()
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)  # Added status field


    class Meta:
        app_label = 'volunteer_oppertunities'

    def __str__(self):
        return self.project_name
    
class VolantDetails(models.Model):
    project = models.ForeignKey(VolantProjects, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_date = models.DateField(default=timezone.now)  # Change to DateField

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name}"
