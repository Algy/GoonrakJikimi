# -*- coding:utf-8 -*-
'''
Created on 2013. 5. 20.

@author: Algy-remote
'''

from PsyChat.IRCCrawler import SBot
from PsyChat.WebCrawler import WebCrawler

class CrawlerManager(object):
    '''
    classdocs
    '''
    
    def start(self):
        # TODO : add custom crawlers
        
        self.webCrawler = WebCrawler()
        self.webCrawler.addObserver(self)
        self.crawlers.append(self.webCrawler)
        
        
        irc = SBot()
        self.crawlers.append(irc)
        irc.addObserver(self)
        irc.start()
        
    def __init__(self):
        '''
        Constructor
        '''
        self.crawlers = []    
        
    def getWebCrawler(self):
        return self.webCrawler
    
    def onEchoMessage(self, sender, botGroup , msgId, source, message):
        pass
    # 실수~ content랑 message랑 같은거에용~ 단지 레코드에서는 content가 source를 대신하고 있어용~
    def onChatMessage(self, sender, botGroup, channel, source, message, msgType):
        record = {}
        record['channel'] = channel
        record['group'] = botGroup
        record['source'] = source
        record['content'] = message
        record['msgType'] = msgType
        
        for otherCrawler in self.crawlers:
            if otherCrawler.botGroup == botGroup:
                continue
            otherCrawler.enqueueMessage(record)
        
    def onSendSuccess(self, sender, botGroup, chatRecord):
        pass