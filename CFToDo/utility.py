import json, requests
import random
from . models import Problem, Tag, Ladder

maxm = 1000000


class CFQuery:

    def __init__(self):
        print ("Welcome to codeforces!")

    def allProblemStat(self):
        urlAllProblems = "http://codeforces.com/api/problemset.problems"
        res = requests.get(urlAllProblems)
        data = json.loads(res.text)
        #print(data)
        N = len(data["result"]["problems"])
        for i in range(50):
            contestId = data["result"]["problems"][i]["contestId"]
            index = data["result"]["problems"][i]["index"]
            problemId = str(contestId) + str(index)
            name = data["result"]["problems"][i]["name"]
            solvedCount = data["result"]["problemStatistics"][i]["solvedCount"]
            tags = data["result"]["problems"][i]["tags"]
            difficulty = self.EvaluateDifficulty(int(solvedCount))
            if(len(Problem.objects.filter(problemId=problemId)) == 0):
                problem = Problem(problemId=problemId,contestId=contestId,index=index,problemName=name,difficulty=difficulty,solvedCount=solvedCount)
                problem.save()
                for tag in tags:
                    if Tag.objects.filter(tag = tag).count() == 0:
                        t = Tag(tag = tag)
                        t.save() 
                        t.problems.add(problem)
                    else:
                        t = Tag.objects.get(tag = tag)
                        t.problems.add(problem)
            else:
                problem = Problem.objects.get(problemId=problemId)
                problem.solvedCount=solvedCount
                problem.difficulty=difficulty
        print(str(N) + " Problem Processed!")
        
    def EvaluateDifficulty(self, solvedCount):             
        coeff = [ 0.00000000e+00 ,-5.57468040e-03 , 3.96749217e-06, -1.43253771e-09,  2.37559930e-13, -1.45370970e-17]
        x = solvedCount
        res = coeff[0] + x*coeff[1] + pow(x,2)*coeff[2] + pow(x,3)*coeff[3] +pow(x,4)*coeff[4] +pow(x,5)*coeff[5] + 6
        
        return res 


    def UserRating(self, cfHandle):
        
        urlUserRating = "http://codeforces.com/api/user.info?handles=" + cfHandle
        query = requests.get(urlUserRating)
        qdata = json.loads(query.text)
        #print(qdata)
        try:
            userRating = int(qdata["result"][0]["rating"])
        except:
            userRating = 1000
        print(userRating)
        if(userRating > 2400):
            rating = 5            
        elif(userRating > 2000):
            rating = 4
        elif(userRating > 1500):
            rating = 3
        elif(userRating > 1000):
            rating = 2
        else:
            rating = 1
        print("user "+ str(cfHandle) +" rating is "+ str(rating))
        print("Rating " + str(rating))
        return rating

    def problemSolvedByUser(self, cfHandle):
        urlUserStat ="http://codeforces.com/api/user.status?handle="+ cfHandle + "&from=1&count=" + str(maxm)
        res = requests.get(urlUserStat)
        data = json.loads(res.text)
        solvedProblemsByUser = []
        Nlength = len(data["result"])
        print (Nlength)
        for submission in data["result"]:
            contestId = str(submission['problem']['contestId'])
            index = str(submission['problem']['index'])
            key = contestId+index
            if(str(submission["verdict"]) == "OK" and key not in solvedProblemsByUser):
                solvedProblemsByUser.append(key)
        print("problemSolvedByUser " + str(len(solvedProblemsByUser)))
        return solvedProblemsByUser

    
    def updateLadder(self, user, cfHandle):
        print('In updateLadder')

        ladder = Ladder.objects.get(user = user)
        problemSolvedByUser = self.problemSolvedByUser(cfHandle = cfHandle)
        for problem in ladder.ladderProblems.all():
            if(problem.problemId in problemSolvedByUser):
                ladder.ladderProblems.remove(problem)

        UserRating = self.UserRating(cfHandle)
        problems = Problem.objects.filter(difficulty = UserRating)
        print(str(len(problems)) + "Problems Fetched")
        print(problems)
        problems = sorted(problems, key=lambda item: random.random())
        print('shuffled')
        if(ladder.ladderProblems.count() < 10):
            for problem in problems:
                if problem not in ladder.ladderProblems.all() and problem not in problemSolvedByUser:
                    ladder.ladderProblems.add(problem)
                    print (problem)
                    print('added')
                if ladder.ladderProblems.count() == 10:
                    break
        print('Ladder Updated')
