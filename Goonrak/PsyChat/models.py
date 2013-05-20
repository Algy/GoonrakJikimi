from django.db import models
from django.db.models.fields import AutoField

# Create your models here.
    
PSYCHAT_GROUP_KAKAO = 0
PSYCHAT_GROUP_JIKIMI = 1
PSYCHAT_GROUP_URIIRC = 2

PSYCHAT_MSGTYPE_NORMAL = 0
PSYCHAT_MSGTYPE_SYSTEM =1


class Chat(models.Model):
    timestamp = models.DateTimeField()
    source = models.CharField(max_length = 60)
    group = models.IntegerField() # from where? like "kakao"=>1, "jikimi"=>2, "uriirc"=>3
    channel = models.CharField(max_length = 60)
    msgType = models.IntegerField() # normal =>0, invitation =>1 , system => 2 , and so on...
    content = models.TextField()
    
    
PSYCHAT_BOT_SEND_READY = 0
PSYCHAT_BOT_SENT = 1
PSYCHAT_BOT_RESPONSE = 2
class BotSend(models.Model):
    queued_timestamp = models.DateTimeField();
    sent_timestamp = models.DateTimeField();
    responsed_timestamp = models.DateTimeField();
    
    status =  models.IntegerField() #PSYCHAT_BOT_XXX
    md5digest = models.CharField(max_length = 32)
    bot_group = models.IntegerField();
    ref_chat = models.ForeignKey(Chat);
