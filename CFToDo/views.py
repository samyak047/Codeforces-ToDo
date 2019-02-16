from django.shortcuts import render, redirect
from .utility import CFQuery
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserDetails, Ladder, Problem


# Create your views here.
def register(request):
	if(request.method == 'POST'):
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			handle = form.cleaned_data['handle']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			user = User.objects.create_user(username = username, email = email, password = password)
			user.first_name = firstname
			user.last_name = lastname
			print('saving in db')
			UserDetails(user = user, cfHandle = handle).save()
			l = Ladder(user = user)
			l.save()
			print('Registration Complete')
			return redirect('http://127.0.0.1:8000/accounts/login/')
		else:
			return render(request, 'register.html', {'form' : form})
	else:	
		form = RegisterForm()
		args = {'form': form}
		return render(request, 'register.html', args)

@login_required
def index(request):
	user = request.user
	cf = CFQuery()
	cf.allProblemStat()
	print('ok')
	cf.updateLadder(user = user, cfHandle = UserDetails.objects.get(user = user).cfHandle)
	print(request.user.get_username() + " Done")
	problemList = Ladder.objects.get(user = user).ladderProblems.all()
	return render(request, 'index.html', {'problemList' : problemList, 'user' : user})

def home(request):
	return render(request, 'home.html')