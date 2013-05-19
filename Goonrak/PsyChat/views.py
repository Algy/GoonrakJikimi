# Create your views here.

'''
bot을 실행시키는 view
참고 : https://github.com/sim0629/sirc/blob/master/wsgi.py
'''
from django.shortcuts import render_to_response, render
from django.utils.dateparse import parse_datetime
import datetime
import urllib2
import re

from botDBProvider import BotDBProvider

'''
가디언 회원인지 인증 작업
'''
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
    
    return render_to_response('PsyChat/error.html' , context)

# update (sirc 서버의 입장에서 일정 날짜 이후의 메시지 업데이트) . SIRC => client (AJAX)
def update(request):
    context = {}
    parameters = request.REQUEST
    
    if 'channel' not in parameters:
        return error(request, message = 'no channel')
    last_update = datetime.datetime.now()
    if 'last_update' in parameters:
        last_update = parse_datetime(parameters['last_update'].decode('utf-8'))
    if 'transition_id' not in parameters:
        return error(request, message = 'no transition_id') 
    channel = parameters['channel'].lower()#.decode('utf-8').lower()
    #channel is percent-encoded now
    channel_encoded = urllib2.quote(channel)

    transition_id = parameters['transition_id'].decode('utf-8')
    account_name = request.session['account'] 
    
    
    if db[account_name].find({'channel': channel}).count() == 0:
        db[account_name].insert({'channel': channel})
        
        
    context['channel'] = channel
    context['transition_id'] = transition_id
    logs = []
    for i in xrange(30):
        logs = list(db[channel_encoded].find({
            'datetime': {"$gt": last_update},
        }, sort = [
            ('datetime', pymongo.ASCENDING)
        ]))
        
        if len(logs) == 0:
            gevent.sleep(1) # how to exchange this?
        else:
            if len(logs) > config.N_LINES:
                logs = []
                context['status'] = 'flooded'
            break
    for log in logs:
        log['source'] = remove_invalid_utf8_char(log['source'])
        log['message'] = remove_invalid_utf8_char(log['message'])
    context['logs'] = logs
    return render('result.xml', context)

# downdate (sirc 서버의 입장에서 일정 날짜 이전 메시지들 내려주기) 
def downdate(request):
    context = {}
    if 'channel' not in parameters:
        return error(start_response, message = 'no channel')
    last_downdate = datetime.datetime.now()
    if 'last_downdate' in parameters:
        last_downdate = parse_datetime(parameters['last_downdate'].decode('utf-8'))
    if 'transition_id' not in parameters:
        return error(start_response, message = 'no transition_id')
    channel = parameters['channel'].lower()#.decode('utf-8').lower()
    channel_encoded = urllib2.quote(channel) #channel name is percent-encoded

    transition_id = parameters['transition_id'].decode('utf-8')
    context['channel'] = channel
    context['transition_id'] = transition_id
    logs = db[channel_encoded].find({
        'datetime': {"$lt": last_downdate},
    }, limit = config.N_LINES, sort = [
        ('datetime', pymongo.DESCENDING)
    ])
    logs = list(logs)
    for log in logs:
        log['source'] = remove_invalid_utf8_char(log['source'])
        log['message'] = remove_invalid_utf8_char(log['message'])
    context['logs'] = logs
    start_response('200 OK', [('Content-Type', 'text/xml; charset=utf-8')])
    return [render('result.xml', context)]

# 메시지를 보냄
def send(request):
    context = {}
    if 'channel' not in parameters:
        return error(start_response, message = 'no channel')
    if 'message' not in parameters:
        return error(start_response, message = 'no message')
    #send db에 넣을 때는 percent-encode할 필요가 없다
    channel = parameters['channel'].decode('utf-8').lower()
    message = parameters['message'].decode('utf-8')
    
    dict = {
        'account': session['account'],
        'channel': channel,
        'message': message
    }
    
    db.send.insert({
        'account': session['account'],
        'channel': channel,
        'message': message
    })
    context['logs'] = [{
        'source': config.BOT_NAME,
        'message': '<%s> %s' % (remove_invalid_utf8_char(session['account']), remove_invalid_utf8_char(message)),
        'datetime': datetime.datetime.now()
    }]
    start_response('200 OK', [('Content-Type', 'text/xml; charset=utf-8')])
    return [render('result.xml', context)]

# 특정 세션의 채널 목록을 지움
def delete(request):
    if 'channel' not in parameters:
        return error(start_response, message = 'no channel')
    channel = parameters['channel'].decode('utf-8').lower()
    db[session['account']].remove({'channel': channel})
    start_response('200 OK', [])
    return []


def default(request):
    context = {}
    context['account'] = session['account']
    context['channels'] = list(db[session['account']].find(fields = ['channel']))
    db.session.remove({'datetime': {'$lt': datetime.datetime.now() - datetime.timedelta(1)}})
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [render('channel.html', context)]


pattern = re.compile("[\x00-\x1F]|[\x80-\x9F]", re.UNICODE)
def remove_invalid_utf8_char(s):
    return pattern.sub(u'�', s)