from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, TravelProfile, REASON_LIST
from services.models import POI_TYPES, POE_TYPES, POG_TYPES, POA_TYPES
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
     
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 
            'first_name', 'last_name', 'birth', 'number',
        ]
        
    def clean_email(self): 
        email = self.cleaned_data['email']
        if len(User.objects.filter(email=email)) > 0:
            raise ValidationError(_("Email already registered"))
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        msg = ""
        
        if len(password1) < 8:
            msg += _("<li>Length less than 8 characters</li>")
        
        if not any (c.islower() for c in password1):
            msg += _("<li>At least one lowercase letter is required</li>")
        
        if not any (c.isupper() for c in password1):
            msg += _("<li>At least one capital letter is required</li>")
        
        if not any (c.isdigit() for c in password1):
            msg += _("<li>At least one number is required</li>")
            
        if msg != "":
            raise ValidationError(msg)
        
        return password1
    
    
class TravelProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TravelProfileForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['poi_selection'].required = False
        self.fields['poe_selection'].required = False
        self.fields['pog_selection'].required = False
        self.fields['poa_selection'].required = False
        self.fields['food_restrictions'].required = False
        self.fields['observations'].required = False
        
    reason_selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=REASON_LIST)
    poi_selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=POI_TYPES)
    poe_selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=POE_TYPES)
    pog_selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=POG_TYPES)
    poa_selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=POA_TYPES)
    
    class Meta:
        model = TravelProfile
        fields = ['title', 'description','n_adults','n_teenagers', 'n_children', 'n_babies','n_elderly',
                  'reduced_mobility','food_restrictions','animals', 'reason_selection',
                  'poi_selection', 'poe_selection', 'pog_selection', 'poa_selection', 'budget',
                  'adventure_level', 'observations']
    
    def clean_reason_selection(self):
        reason_selection = self.cleaned_data['reason_selection']
        return str(reason_selection)
    
    def clean_poi_selection(self):
        poi_selection = self.cleaned_data['poi_selection']
        return str(poi_selection)
    
    def clean_poe_selection(self):
        poe_selection = self.cleaned_data['poe_selection']
        return str(poe_selection)
    
    def clean_pog_selection(self):
        pog_selection = self.cleaned_data['pog_selection']
        return str(pog_selection)
    
    def clean_poa_selection(self):
        poa_selection = self.cleaned_data['poa_selection']
        return str(poa_selection)
    
