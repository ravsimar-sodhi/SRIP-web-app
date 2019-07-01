from django import forms
CHOICES=[
    ("user", "User"),
    ("org", "Organization"),
]
class ProjectBulkAddForm(forms.Form):
    owner = forms.CharField(max_length=120, label = 'Owner')
    o_type = forms.ChoiceField(choices=CHOICES, label = 'Owner Type')