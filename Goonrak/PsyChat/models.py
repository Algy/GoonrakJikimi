from django.db import models

# Create your models here.

class ChatContent(models.Model):
    timestamp = models.DateField()
    name = models.CharField(max_length = 128)
    group = models.IntegerField() # from where? like "kakao"=>1, "jikimi"=>2, "uriirc"=>3
    msgType = models.IntegerField() # normal =>0, invitation =>1 , system => 2 , and so on...
    content = models.TextField()