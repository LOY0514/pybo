from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)    #charfield의 내용으로 파일이름이 지정
    content = models.TextField()
    create_date = models.DateTimeField()

    elbowCheck = models.IntegerField(default = 0)
    dampCheck = models.IntegerField(default = 0)
    vibCheck = models.IntegerField(default = 0)
    backAngCheck = models.DecimalField(max_digits = 10, decimal_places = 5, default = 0.)
    rlTimeCheck = models.IntegerField(default = 0)
    rlAngCheck = models.DecimalField(max_digits = 10, decimal_places = 5, default = 0.)

    def __str__(self):
        return self.subject
    
    
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    
