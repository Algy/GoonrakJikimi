from django.db import models

# Create your models here.

# base model of problem
# replace Account to real model correspond to account model in real
# plz use only somoonja and underline  to name field  please :)

class ProblemSet(models.Model):
    score = models.PositiveIntegerField()
    kind =  models.CharField(max_length=20) # binary, system, forensic, crypto, network, real_world; python, c_language;
    name = models.CharField(max_length=60) # problem name
    
    description = models.TextField() # seol myeong
    auth_method = models.CharField(max_length=15) # key, 5answer, manual_check .... let's think about it 
    
    is_open = models.BooleanField()
    # open_by = models.ForeignKey(Account)
    
    open_timestamp = models.DateTimeField()
    recent_modified_timestamp = models.DateTimeField()

  
class ProblemSolveInfo(models.Model):
    timestamp = models.DateTimeField()
    problem = models.ForeignKey(ProblemSet) # one to many(1:) relation
    
    #solver = models.ForeignKey(Account)
    is_breakthrough = models.BooleanField()
    
    
'''
Relation
ProblemSet(1:) <-----> ProblemSolveInfo <-------> ( : 1 ) Account

e.g

bin100 ----- 1 a.m solved by Algy(break-trhough)        ------- Algy    
            |- 2 p.m solved by Dandelin                    ----+-- Dandelin
            |- 5 p.m solved by PhoBiA                       ---+-- PhoBiA
            |- 10 p.m solved by Algy again                 ----|
            
system200 ----- .....
forensic300 ---   .....
'''
# corrspond to auth_method field!
class ProblemAuthWithKey(models.Model): 
    problem = models.OneToOneField(ProblemSet)
    answer_key = models.TextField()

# corrspond to auth_method field!
class ProblemAuthManually(models.Model):
    problem = models.OneToOneField(ProblemSet)
    # verified_by = models.ForeignKey(Account) # it must be problem opener

# uhuhuhuh him dul da
#here's good music for hard working :) : http://www.youtube.com/watch?v=o1eHKf-dMwo