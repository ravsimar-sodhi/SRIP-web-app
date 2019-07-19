from django import forms

class LoggedCommitForm(forms.Form):
    project_id = forms.CharField(max_length=120, label = 'Project ID')
    commit_id = forms.CharField(max_length=40,min_length=40, label="Commit ID")
    url = forms.URLField(label='Issue URL')

class ReportForm(forms.Form):
    report = forms.URLField(label='Wiki Page URL')