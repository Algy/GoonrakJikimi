# -*- coding: utf-8 -*-
# Create your views here.

'''
참고 : https://github.com/sim0629/sirc/blob/master/wsgi.py
'''

from PsyChat.models import PSYCHAT_MSGTYPE_NORMAL
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response, render
from models import Chat
import config
import datetime
import re
import urllib2
import Goonrak
from PsyChat.CrawlerManager import CrawlerManager
from django.http.response import HttpResponse



def auth(request):
    pass

def notGuardian(request):
    pass
'''
Created on 2013. 5. 14.

@author:sim0629

ported by Algy
'''

def error(request, code = '404 Not Found', message = 'error'):
    context = {}
    context['message'] = message.decode('utf-8')
    
    return render_to_response('error.html' , context)


def update(request):
    context = {}
    parameters = request.REQUEST
    
    
    last_update = datetime.datetime.now()
    if 'last_update' in parameters:
        last_update =parameters['last_update'].decode('utf-8')
        
    context['channel'] = 'Goonrak'
    
    context['transition_id'] = 0#transition_id
    critia_datetime = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds = 1)
    
    flooded = False
    for i in xrange(30):
        
        log_records = Chat.objects.filter(timestamp__gte = critia_datetime).order_by('timestamp')
        if len(log_records) == 0:
            pass # gevent.sleep(1) # it means wait 30ms maybe. # how to exchange this?
        else:
            if len(log_records) > config.N_LINES:
                context['status'] = 'flooded'
                flooded = True
            break
        
    logs = log_records.values()
    
    
    if not flooded:
        for log in logs:
            log['source'] = remove_invalid_utf8_char(log['source'])
            log['content'] = remove_invalid_utf8_char(log['content'])
        context['logs'] = logs
    return render_to_response('result.xml', context)

def downdate(request):
    context = {}
    parameters = request.REQUEST

    last_downdate = datetime.datetime.now()
    if 'last_update' in parameters:
        last_downdate =parameters['last_downdate'].decode('utf-8')
        
    context['channel'] = 'Goonrak'
    
    context['transition_id'] = 0#transition_id 

    logs = Chat.objects.filter(timestamp__lte = last_downdate).order_by('-timestamp')[ : config.N_LINES].values()
        
    for log in logs:
        log['source'] = remove_invalid_utf8_char(log['source'])
        log['content'] = remove_invalid_utf8_char(log['content'])
        
    context['logs'] = logs
    
    return render_to_response('result.xml', context)

def send(request):
    context = {}
    parameters = request.REQUEST
    if not Goonrak.settings.PSYCHAT_CRAWLER_MANAGER:
        return error(request, message = 'start bot first')
    
    webCrawler = Goonrak.settings.PSYCHAT_CRAWLER_MANAGER.getWebCrawler()

    if 'message' not in parameters:
        return error(request, message = 'no message')
    
    channel = "Goonrak"
    content = parameters['message'] # .decode('utf-8')
    
    #TODO : change this to real account 
    account = "ALGY"# session['account']
    timestamp = datetime.datetime.now()
    
    record = Chat(timestamp = timestamp, group = webCrawler.botGroup, source = account, channel = channel, msgType = PSYCHAT_MSGTYPE_NORMAL, content = content)
    record.save()
    
    webCrawler.notifyChatMessage(channel = channel, source = account, message = content, msgType = PSYCHAT_MSGTYPE_NORMAL)
    
    log = model_to_dict(record)
    log['source'] = remove_invalid_utf8_char(log['source'])
    log['content'] = remove_invalid_utf8_char(log['content'])
    context['logs'] = [log]
    
    return render_to_response('result.xml', context)


def default(request):
    return render_to_response('psychat.html', {})

def botThread():
    Goonrak.settings.PSYCHAT_CRAWLER_MANAGER = CrawlerManager()
    Goonrak.settings.PSYCHAT_CRAWLER_MANAGER.start()
    
import thread
def startBot(request):
    if Goonrak.settings.PSYCHAT_CRAWLER_MANAGER:
        return HttpResponse("already running")
    thread.start_new_thread(botThread, ())
    return HttpResponse("success!")

pattern = re.compile("[\x00-\x1F]|[\x80-\x9F]", re.UNICODE)
def remove_invalid_utf8_char(s):
    return pattern.sub(u'�', s)