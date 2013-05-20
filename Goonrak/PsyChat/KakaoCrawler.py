'''
Created on 2013. 5. 21.

@author: Algy-remote
'''
from PsyChat.crawler import Crawler
from models import PSYCHAT_GROUP_KAKAO

class KakaoCrawler(Crawler):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Crawler.__init__(self)
        self.botGroup = PSYCHAT_GROUP_KAKAO
    
    def enqueueMesssage(self, chatRecord):
        pass