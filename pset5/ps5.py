# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# NewsStory
class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        Trigger.__init__(self)
        self.phrase = phrase.lower().split()

    def is_phrase_in(self, text):
        """
        text: a string
        returns: True if the self.phrase appears in its entirity in the given text, False otherwise
        """


        # make a list of the characters of the given text to be searched
        search_text = text.lower().strip(string.punctuation)
        #print(search_text)

        # a string of punctuation characters
        punctuation = string.punctuation + ' '

        # a list will be build of only the alpha numeric characters of the given text, any character in 'punctuation' will be considered a word seperator
        search_text_list = []

        # algorithm for building 'search_text_list' 
        # build the above mentioned list, word by word
        current_word = ''
        # iterate through each character of the 'text'
        for each_char in search_text:

            # if the character is not a punctuation character, it's a part of a word
            if each_char not in punctuation:
                current_word += each_char

            # the current character is a punctuation character, so if a word was being built, its complete, append that word to the list, and start creating a new word
            else:
                if current_word.isalnum():
                    search_text_list.append(current_word)
                    current_word = ''

        # if a word was being built, but it didn't end with a punctuation mark, add that word too to the list
        if current_word.isalnum():
            search_text_list.append(current_word)

        #print('Search list: ' , str(search_text_list))

        # get the index of the first word of the phrase in the 'search_list'
        index_of_first_phrase_in_search_list = -1
        try:
            index_of_first_phrase_in_search_list = search_text_list.index(self.phrase[0])
        except IndexError:
            return False
        except ValueError:
            return False

        #print('index of first word of phrase: ' , str(index_of_first_phrase_in_search_list))

        # the first word of the phrase itself is not present in the search text(list)
        if index_of_first_phrase_in_search_list < 0:
            return False

        #print('Phrase is present')

        # -------------------------------------------------------------------------------------------------------
        # now check if subsequent words of the search text(list) is same aa the subsequentr words in the phrase
        # if not return False
        #--------------------------------------------------------------------------------------------------------

        # the current index of the phrase list
        index_of_phrase_list = 1

        # current index of the search text(list)
        current_index_in_search_text_list = index_of_first_phrase_in_search_list + 1

        # as long as there is more words in search text(list)
        while current_index_in_search_text_list < len(search_text_list):

            # are there more wordds in the phrases list?
            # No? return True because all the phrases are in search_text_list
            # Yes? well continue as normal
            if not (index_of_phrase_list < len(self.phrase)):
                return True

            #print('Word in search list: ', search_text_list[current_index_in_search_text_list])
            #print('Word in phrase list: ', self.phrase[index_of_phrase_list])

            # if current phrase is not in the search_text_list at the expected place
            # check any other word is present in the rest of the search_text_list where the first word in the phrase(list) is present
            if search_text_list[current_index_in_search_text_list] != self.phrase[index_of_phrase_list]:

                # try to find the first word in the phrase list in the rest of the search_text_list, raises ValueError not present
                try:
                    index_of_first_phrase_in_search_list = search_text_list.index(self.phrase[0], current_index_in_search_text_list + 1)
                except ValueError:
                    return False
                # if index_of_first_phrase_in_search_list < 0:
                #     return False

                # the current index of the phrase list
                index_of_phrase_list = 0

                # current index of the search text(list)
                current_index_in_search_text_list = index_of_first_phrase_in_search_list
                


            current_index_in_search_text_list += 1
            index_of_phrase_list += 1

        # the search_text_list ended before the phrase list
        if index_of_phrase_list < len(self.phrase):
            return False

        return True 



# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())
        

# Problem 4
class DescriptionTrigger(PhraseTrigger):

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, date_string):
        Trigger.__init__(self)
        self.date_time = datetime.strptime(date_string, '%d %b %Y %H:%M:%S')
        self.date_time = self.date_time.replace(tzinfo=pytz.timezone("EST"))

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        '''
        Input:  a story object
        Returns True if the publication date of the story is before Trigger's time, False otherwise
        '''
        story_pubdate = story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))
        return story_pubdate < self.date_time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        '''
        Input:  a story object
        Returns True if the publication date of the story is after Trigger's time, False otherwise
        '''
        story_pubdate = story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))
        return story_pubdate > self.date_time


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, T):
        '''
        Input: T is a Trigger class or Subclass Instance
        '''
        Trigger.__init__(self)
        self.trigger = T

    def evaluate(self, story):
        '''
        Input: A Trigger object
        Returns a Complimented Value of the input trigger's evalutate method
        '''
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        '''
        Input: T1 and T2 are Trigger class or Subclass Instance
        '''
        Trigger.__init__(self)
        self.trigger1 = T1
        self.trigger2 = T2

    def evaluate(self, story):
        '''
        Input: Two Trigger objects
        Returns a AND'D value of the input triggers' evalutate method
        '''
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        '''
        Input: T1 and T2 are Trigger class or Subclass Instance
        '''
        Trigger.__init__(self)
        self.trigger1 = T1
        self.trigger2 = T2

    def evaluate(self, story):
        '''
        Input: Two Trigger objects
        Returns a OR'D value of the input triggers' evalutate method
        '''
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []

    # check if a trigger is fired for each story
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                if story not in filtered_stories:
                    # trigger is fired and the story is not already in the list
                    filtered_stories.append(story)

    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    # the list of triggers being built to return 
    trigger_list = []

    # the dictionay of triggers to save reference to the triggers being bulit
    triggers = {}

    for line in lines:
        cmd = line.split(',')

        # the first word is either a ADD command or the name of the trigger
        the_cmd = cmd[0].strip()

        # if it's ADD
        if the_cmd == 'ADD':
            # add all the following triggers to the list of triggers to return
            for atrigger in range(1, len(cmd)):
                trigger_list.append(triggers[cmd[atrigger].strip()])

        # dynamically create trigger as per the file
        else:
            # second word is always the Type of trigger
            trigger_name = cmd[1].strip()
            trigger_obj = None
            if trigger_name == 'TITLE':
                trigger_obj = TitleTrigger(cmd[2].strip())
            elif trigger_name == 'DESCRIPTION':
                trigger_obj = DescriptionTrigger(cmd[2].strip())
            elif trigger_name == 'AFTER':
                trigger_obj = AfterTrigger(cmd[2].strip())
            elif trigger_name == 'BEFORE':
                trigger_obj = BeforeTrigger(cmd[2].strip())
            elif trigger_name == 'NOT':
                trigger_obj = NotTrigger(triggers[cmd[2].strip()])
            elif trigger_name == 'AND':
                trigger_obj = AndTrigger(triggers[cmd[2].strip()], triggers[cmd[3].strip()])
            elif trigger_name == 'OR':
                trigger_obj = OrTrigger(triggers[cmd[2].strip()], triggers[cmd[3].strip()])

            # add the trigger bulit to the dictionary, with the key being the name for that trigger given by user in the trigger.txt file
            triggers[the_cmd] = trigger_obj

    print(lines) # for now, print it so you see what it contains!
    return trigger_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

