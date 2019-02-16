from django.db import models
from django.contrib.auth.models import User



class UserDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cfHandle = models.CharField(max_length = 200)

class Problem(models.Model):
	problemId = models.CharField(max_length = 200, primary_key = True)
	contestId = models.CharField(max_length = 100) 
	index = models.CharField(max_length = 100)
	problemName = models.CharField(max_length = 200)
	difficulty = models.IntegerField(default = 0)
	solvedCount = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.problemId)
	
class Tag(models.Model):
	tag = models.CharField(max_length = 200)
	problems = models.ManyToManyField(Problem)

	def __str__(self):
		return str(self.tag)

class Ladder(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	ladderProblems = models.ManyToManyField(Problem)

	def __str__(self):
		return (str(self.user) + ' with ' + str(self.ladderProblems))

