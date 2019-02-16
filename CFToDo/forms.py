from django import forms
import json, requests
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
	firstname = forms.CharField(label = 'First Name')
	lastname = forms.CharField(label = 'Last Name')
	username = forms.CharField(label = 'Username')
	handle = forms.CharField(label = 'Codeforces Handle')
	email = forms.EmailField(label = 'E-mail')
	password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput())
	
	def clean(self):
		cleaned_data = super().clean()
		p1 = cleaned_data.get("password1")
		p2 = cleaned_data.get("password2")
		username = cleaned_data.get("username")
		cfhandle = cleaned_data.get("handle")
		if len(User.objects.filter(username=username)) > 0:
			raise forms.ValidationError('Username already Exists')
		if len(p1) < 8:
			raise forms.ValidationError('Password should be minimum 8 characters long.')
		if p1 != p2:
			raise forms.ValidationError('Both Password fields should be same.')
		urlUserStat ="http://codeforces.com/api/user.status?handle="+cfhandle
		res = requests.get(urlUserStat)
		data = json.loads(res.text)
		if data['status'] == 'FAILED':
			raise forms.ValidationError(data['comment'])

