from dataclasses import field
from django import forms
from tree.models import Account, User, PlantedTree, Profile
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from crispy_forms.helper import FormHelper
from crispy_forms import bootstrap, helper, layout
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, ButtonHolder, Field, Button, HTML, Div, Hidden
from crispy_forms.bootstrap import InlineField, FormActions, Accordion, AccordionGroup, PrependedText, AppendedText

class UserFormAdd(forms.ModelForm):
    
    account = forms.ModelChoiceField(queryset=Account.objects.all())
    
    class Meta:
        model = User
        fields = ('account', 'username', 'password', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff')
        exclude = ('groups', 'user_permissions')
    
    def clean_account(self):
        if Account.objects.filter(name=self.cleaned_data["account"], user=self.instance).count() > 0:
            raise forms.ValidationError(_('This user already exists in the account.'))
        return self.cleaned_data["account"]
    
    
class PlantedTreeFormCreate(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ('tree', 'planted_at', 'age', 'account', 'latitude', 'longitude')
        widgets = {
            'planted_at': DateTimePickerInput(options={
                            'format': 'DD/MM/YYYY HH:mm',
                            'locale': 'pt-br',
                        })
        }

    def __init__(self, user, *args, **kwargs):
        super(PlantedTreeFormCreate, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column('tree', css_class='form-group col-md-12 mb-0')                
            ),
            Row(
                Column('planted_at', css_class='form-group col-md-12 mb-0')                
            ),
            Row(
                Column('age', css_class='form-group col-md-12 mb-0')                
            ),
            Row(
                Column('account', css_class='form-group col-md-12 mb-0')                
            ),
            Row(
                Column(Field('latitude'), css_class='form-group col-md-12 mb-0')                
            ),
            Row(
                Column(Field('longitude'), css_class='form-group col-md-12 mb-0')                
            ),
            HTML("<br>"),
            FormActions(
                Submit('save_changes', _('save'))                
            )
        )
    

class UserProfileFormUpdate(forms.ModelForm):
    about = forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    joined = forms.DateTimeField()
    
    def __init__(self, *args, **kwargs):
       super(UserProfileFormUpdate, self).__init__(*args, **kwargs)
       self.fields['joined'].widget.attrs['readonly'] = True
    
    class Meta:
        model = Profile
        fields = ('about', 'joined',)