# -*- coding: utf-8 -*-
from PsyChat.models import PSYCHAT_MSGTYPE_SYSTEM, PSYCHAT_MSGTYPE_NORMAL, BotSend, PSYCHAT_BOT_SENT, Chat, PSYCHAT_BOT_RESPONSE, PSYCHAT_GROUP_URIIRC, PSYCHAT_BOT_SEND_READY
from irclib import ircbot, irclib
from datetime import datetime
import config
import md5
import re

class SBot(ircbot.SingleServerIRCBot):
    botGroup = PSYCHAT_GROUP_URIIRC
    joinChannels = ["#Algy", ]
    def __init__(self):
        
        ircbot.SingleServerIRCBot.__init__(self,
            [(config.SERVER, config.PORT), ],
            config.BOT_NAME,
            'm',
        )
        
        self.connected = False
        self._fetch()
    ''' 
    event handler part
    '''
    def on_welcome(self,c, e):
        self.connected = True
        for target in self.joinChannels: #extract last channels the user used
            print "target : " + target
            c.join(target) #==self.connect.join(target)
    
    def on_mode(self, c, e):
        nick = irclib.nm_to_n(e.source())
        target = e.target()
        if irclib.is_channel(target):
            self._log(target, config.NOTIFY_NAME, '[%s] by <%s>.' % (' '.join(e.arguments()), nick), PSYCHAT_MSGTYPE_SYSTEM)
        else:
            pass

    def on_nick(self, c, e):
        before = irclib.nm_to_n(e.source())
        after = e.target()
        for target, ch in self.channels.items():
            if ch.has_user(before):
                self._log(target, config.NOTIFY_NAME, '<%s> is now known as <%s>.' % (before, after), PSYCHAT_MSGTYPE_SYSTEM)
    
    def on_join(self, c, e):
        nick = irclib.nm_to_n(e.source())
        self._log(e.target(), config.NOTIFY_NAME, '<%s> has joined.' % nick, PSYCHAT_MSGTYPE_SYSTEM)

    def on_part(self, c, e):
        nick = irclib.nm_to_n(e.source())
        self._log(e.target(), config.NOTIFY_NAME, '<%s> has left.' % nick, PSYCHAT_MSGTYPE_SYSTEM)
    
    def on_quit(self, c, e):
        nick = irclib.nm_to_n(e.source())
        for target, ch in self.channels.items():
            if ch.has_user(nick):
                self._log(target, config.NOTIFY_NAME, '<%s> has quit.' % nick, PSYCHAT_MSGTYPE_SYSTEM)
    
    def on_kick(self, c, e):
        nick_s = irclib.nm_to_n(e.source())
        nick_m = e.arguments()[0]
        because_of = e.arguments()[1]
        self._log(e.target(), config.NOTIFY_NAME, '<%s> was kicked by <%s> because of "%s".' % (nick_m, nick_s, because_of), PSYCHAT_MSGTYPE_SYSTEM)

    def on_pubmsg(self, c, e): 
        nick = irclib.nm_to_n(e.source())
        target = e.target()
        message = e.arguments()[0]
        self._log(target, nick, message,PSYCHAT_MSGTYPE_NORMAL)
        if self.channels[target].is_oper(c.get_nickname()) and \
            nick == config.OPERATOR_NAME and \
            message.startswith(config.OPERATOR_COMMAND):
            self.connection.mode(target, '+o %s' % nick)
    
    '''
    function part
    '''        
            
    def formatMessage(self, source, message):
        return '<%s> %s' % (source, message)
    
    def deformatMessage(self, message):
        m = re.match(r"^<.+> ", message)
        if not m:
            return None
        
        print "deformats : " + message[m.end() : ]
        return message[ m.end() : ]
    
    def sentFilter(self, source, message, msgType):
        if source == config.BOT_NAME:
            splittedMessage = self.deformatMessage( message )
            if not splittedMessage:
                return 
            md5_obj = md5.new()
            md5_obj.update(splittedMessage)
            return md5_obj.hexdigest()
        return 
    # vary by using another db or saving system
    def _log(self, target, source, message, msgType):
        
        print  "@"+target + " "+ "<" + source + ">" + message
        # first, filter if it was sent by bot 
        hexDigest = self.sentFilter(source, message, msgType) # if it is assummed redrawed message
        
        if hexDigest: # it's sent by bot
            print "it has been sent ever..."
            sentArray = BotSend.objects.filter(md5digest = hexDigest).filter(status = PSYCHAT_BOT_SENT).order_by('sent_timestamp') 
            
            if len(sentArray) == 0:
                pass # may be it's fake
            else:
                sentRecord = sentArray[0]; 
                sentRecord.responsed_timestamp = datetime.now()
                sentRecord.status = PSYCHAT_BOT_RESPONSE
                sentRecord.save()
            
        else:
            record = Chat(timestamp = datetime.now(), 
                          source = source, 
                          channel = target, 
                          group = self.botGroup, 
                          msgType = msgType, 
                          content = message);
            record.save()
            
    
    
    def _fetch(self):
        if self.connected:
            try:
                for record in BotSend.objects.filter( status = PSYCHAT_BOT_SEND_READY ):
                    channel = record.ref_chat.channel.lower().encode('utf-8').lower()
                    
                    if channel not in self.channels:
                        self.connection.join(channel)
                    account = record.ref_chat.source.encode('utf-8')
                    
                    message = self.formatMessage(account, record.ref_chat.content ).encode('utf-8')
                    self.connection.privmsg(channel, message) 
                    
                    record.sent_timestamp = datetime.now() # sucess!:)
                    record.save()
                    
            except irclib.ServerNotConnectedError:
                self.connected = False
                self._connect()
                
        print "fetched.."
        self.ircobj.execute_delayed(1, self._fetch) 
        
    
    def queueMsg(self, chatRecord):
        content = chatRecord.content
        md5_obj = md5.new()
        md5_obj.update(content)
        
        sendRecord = BotSend(queued_timestamp = datetime.now(), 
                status = PSYCHAT_BOT_SEND_READY,
                md5digest = md5_obj.hexdigest(),
                bot_group = self.botGroup,
                ref_chat = chatRecord
                );
        sendRecord.save()
        
if __name__ == '__main__':
    bot = SBot()
    bot.start()
