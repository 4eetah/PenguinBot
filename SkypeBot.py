#!/usr/bin/python

import Skype4Py
import time
from datetime import datetime
from cleverbot import Cleverbot

class SkypeBot(object):
    def __init__(self):
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.Attach()
        self.me = self.skype.CurrentUser
        self.stupidBot = Cleverbot()
        self.awayMessage = "\
Hi, seems like Denis isn't in front of \
me right now. I am Gentoo penguin, his pet. \
Would you like to talk for a while ?"

        self.chatsSoFar = []

    def UserStatus(self, Status):
        print 'The status of the user changed'

    def MessageStatus(self, msg, Status):
        time.sleep(1.0)
        chat = msg.Chat
        sender = msg.Sender
        if sender == self.me: return
        if chat in self.chatsSoFar:
            activityTime = chat.ActivityDatetime
            now = datetime.now()
            timeDiff = now - activityTime
            minDiff = timeDiff.seconds / 60
            if minDiff > 20:
                self.chatsSoFar.remove(chat)

        # Prevent intruding to public chats, rethink it later
        if self.me.Handle in chat.Name \
        and self.me.OnlineStatus == 'AWAY':
            if chat not in self.chatsSoFar:
                chat.SendMessage(self.awayMessage)
                self.chatsSoFar.append(chat)
            else:
                answer = self.stupidBot.ask(msg.Body)
                chat.SendMessage(answer)
        else:
            print 'Prolly this is not the right chat'


if __name__ == "__main__":
    bot = SkypeBot()

    while True:
        time.sleep(1.0)

