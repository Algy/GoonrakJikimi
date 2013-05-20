'''
Created on 2013. 5. 20.

@author: Algy-remote
'''
from PsyChat.crawler import Crawler
from PsyChat.models import PSYCHAT_GROUP_JIKIMI, Chat
import datetime

class WebCrawler(Crawler):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.botGroup = PSYCHAT_GROUP_JIKIMI
        Crawler.__init__(self)
    
    def enqueueMessage(self, chatRecord):
        record = Chat(timestamp = datetime.datetime.now(), 
                      source = chatRecord['source'], 
                      channel = chatRecord['channel'], 
                      group = chatRecord['group'], 
                      msgType = chatRecord['msgType'], 
                      content = chatRecord['content']);
        record.save()
        