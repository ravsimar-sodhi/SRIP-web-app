from django import forms

STATUS = [
('PENDING', 'Pending'),
('REJECTED', 'Rejected'),
('APPROVED', 'Approved'),
]

class CommitEvaluationForm(forms.Form):
    user = forms.CharField(max_length=120, label='User', disabled =True, required=False)
    project = forms.CharField(max_length=120, label = 'Project ID', disabled=True, required=False)
    commit_id = forms.CharField(max_length=40,min_length=40, label="Commit ID", disabled=True, required=False)
    url = forms.URLField(label='Issue URL')
    html_fp = forms.FloatField(label='HTML Points')
    css_fp = forms.FloatField(label="CSS Points")
    js_fp = forms.FloatField(label='JS Points')
    py_fp = forms.FloatField(label='Python Points')
    status = forms.ChoiceField(choices=STATUS, label='Status')
    remark = forms.CharField(label = "Remark")