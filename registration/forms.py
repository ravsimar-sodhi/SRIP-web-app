from django import forms
from .models import Student


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'registrations/{0}'.format(filename)

class StudentForm(forms.Form):
	name = forms.CharField(label='Name of Student', max_length=100)
	email = forms.EmailField(label='Email ID', max_length=100)
	clg_name = forms.CharField(label='College Name', max_length=100)
	branch_year = forms.CharField(label='Branch and Year', max_length=100)
	rollno = forms.CharField(label='Roll Number', max_length=100)
	area_interest = forms.CharField(label='Area of Interest', max_length=100)
	handle = forms.CharField(label='Github Handle', max_length=100)
	resume = forms.FileField(label='Resume')
	st_id = forms.FileField(label='Student ID Card')

class ProfileForm(forms.Form):
	# ref = forms.ModelChoiceField()
	# def __init__(self, *args, **kwargs):
	# 	super(MyForm, self).__init__(*args, **kwargs)
	# 	self.fields['ref'].queryset = Student.objects.filter(handle=self.request.user)

	name = forms.CharField(label='Name of Student', max_length=100)
	email = forms.EmailField(label='Email ID', max_length=100)
	clg_name = forms.CharField(label='College Name', max_length=100)
	branch_year = forms.CharField(label='Branch and Year', max_length=100)
	rollno = forms.CharField(label='Roll Number', max_length=100)
	area_interest = forms.CharField(label='Area of Interest', max_length=100)
	handle = forms.CharField(label='Github Handle', max_length=100)
	resume = forms.FileField(label='Resume')
	st_id = forms.FileField(label='Student ID Card')

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Student
#         exclude = ['status', 'function_points', 'user','effort', 'report', 'mentor', 'batch', 'handle']
#         labels = {
#             'name': _('Name of Student'),
#             'st_id': _("Student ID"),
#             'email':_("Email ID"),
#             'rollno':_("Roll No."),
#             'clg_name':_("College Name"),
#             'branch_year':_("Branch & Year"),
#             'area_interest':_("Area of Interest"),
#             'handle':_("Github Handle"),
#             'resume':_("Resume"),
#         }