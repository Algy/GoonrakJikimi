'''
Created on 2013. 5. 20.

@author: Algy-remote
'''

import re
class Crawler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.observers = set()
        
    def addObserver(self, observer):
        self.observers.add(observer)
    def removeObserver(self, observer):
        self.observers.remove(observer)
    
    def notifyEchoMessage(self, source, message):
        '''
            onEchoMessage(sender, botGroup , msgId, source, message)
        '''
        
        for ob in self.observers:
            ob.onEchoMessage(self, self.botGroup, source, message)
        
    def notifyChatMessage(self, channel, source, message, msgType):
        '''
            onChatMessage(sender,. botGroup, channel, source, message, msgType)
        '''
        for ob in self.observers:
            ob.onChatMessage(self, self.botGroup, channel, source, message, msgType)
            
    def notifySendSuccess(self, chatRecord):
        '''
            onSendSuccess(sender,. botGroup, chatRecord)
        '''
        for ob in self.observers:
            ob.onSendSuccess(self, self.botGroup, chatRecord)
        
    def enqueueMesssage(self, chatRecord):
        raise NotImplementedError()
    
    def formatMessage(self, source, message, msgType):
        return '<%s> %s' % (source, message)
    
    def extractMessage(self, fmtMessage):
        m = re.match(r"^<.+?> ", fmtMessage)
        if not m:
            return None
        
        return fmtMessage[ m.end():]
