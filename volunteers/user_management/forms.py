# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import VolantUser  

class VolantUserCreationForm(UserCreationForm):
    INTEREST_CHOICES = [
        ('environmental_conservation', 'Environmental conservation'),
        ('animal_welfare', 'Animal welfare'),
        ('social_justice', 'Social justice and human rights'),
        ('education', 'Education and mentoring'),
        ('arts', 'Arts and culture'),
        ('health', 'Health and wellness'),
        ('community_development', 'Community development'),
        ('technology', 'Technology and innovation'),
        ('sports', 'Sports and recreation'),
        ('elderly_care', 'Elderly care and support'),
    ]

    ABILITY_CHOICES = [
        ('communication_skills', 'Communication skills (verbal and written)'),
        ('leadership', 'Leadership and teamwork'),
        ('problem_solving', 'Problem-solving and critical thinking'),
        ('organization', 'Organization and time management'),
        ('teaching', 'Teaching and training'),
        ('creativity', 'Creativity and innovation'),
        ('adaptability', 'Adaptability and flexibility'),
        ('technical_skills', 'Technical skills (e.g., IT, programming)'),
        ('research', 'Research skills'),
        ('counseling', 'Counseling and empathy'),
    ]

    TALENT_CHOICES = [
        ('artistic', 'Artistic abilities (painting, drawing, sculpting)'),
        ('musical', 'Musical talents (playing instruments, singing)'),
        ('performing_arts', 'Performing arts (acting, dancing)'),
        ('crafting', 'Crafting and DIY skills'),
        ('cooking', 'Cooking and culinary skills'),
        ('photography', 'Photography and videography'),
        ('gardening', 'Gardening and landscaping'),
        ('sports', 'Sports and athletic abilities'),
        ('public_speaking', 'Public speaking and storytelling'),
        ('writing', 'Writing and storytelling'),
    ]

    interests = forms.MultipleChoiceField(choices=INTEREST_CHOICES, widget=forms.CheckboxSelectMultiple)
    abilities = forms.MultipleChoiceField(choices=ABILITY_CHOICES, widget=forms.CheckboxSelectMultiple)
    talents = forms.MultipleChoiceField(choices=TALENT_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = VolantUser  
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'mobile_number', 'nic', 'interests', 'abilities', 'talents')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if VolantUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if VolantUser.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("This mobile number is already in use.")
        return mobile_number

    def clean_nic(self):
        nic = self.cleaned_data.get('nic')
        if VolantUser.objects.filter(nic=nic).exists():
            raise forms.ValidationError("This NIC is already in use.")
        return nic
