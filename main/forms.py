from django import forms

# class IssueForm(forms.Form):
    # c
class LoggedIssueForm(forms.Form):
    commit_id = forms.CharField(max_length=40,min_length=40, label="Commit ID")
    url = forms.URLField(label='Issue URL')

class ReportForm(forms.Form):
    report = forms.URLField(label='Wiki Page URL')