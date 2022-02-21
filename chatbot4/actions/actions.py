# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient




client = MongoClient("mongodb+srv://sahilDB:ZcBARYyUaAbkCjlx@cluster0.aysyi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

#databasename
db = client["professors_database"]
 
# Collection Name
professor = db["professor"]



#extracting all professors from database and storing it in data list
x = professor.find()

#storing all professors data from database
data = [i for i in x]

# print(data)


class ActionGetProfessor(Action):

    def name(self) -> Text:
        # used to give name to your custom action

        return "action_get_professor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #LOGIC:
        # custom code for implementing logic
        # here I apply very simple logic to get professor
        # from list of professors i am checking user entered topic is any professor in area_of_expertise
        # if it is appending it to result
        # if not program will check professors about as about contain lot of information about the professor
        # so i applied a condition that if topic's count in about is greater than or eual to 2
        # if yes append 
        # if professor record have value about and area_of_expertise is None program will check topic in designatio
        # 

        #get slot value extracted from user
        topic = tracker.get_slot("topic_name")
        # flag = 0
        if topic != None:
            list_of_prof = []
            for prof in data:
                if prof['area_of_expertise']!= None:
                    if topic in prof['area_of_expertise']: 
                        list_of_prof.append(prof)
                elif prof['area_of_expertise'] == None and prof['about'] != None:
                    count = prof['about'].count(topic)
                    if count >= 2:
                        list_of_prof.append(prof)
                elif prof['area_of_expertise'] == None and prof['about'] == None and prof['designation'] != None:
                    if topic in prof['designation']:
                        list_of_prof.append(prof)
            if len(list_of_prof)>=1:
                # flag = 1
                # if len(list_of_prof)>3:
                msg1 = "you can contact professors followed by link you can get more information about professor by clicking on links:- "
                # Giving only 3 professor at a time
                if len(list_of_prof)>3:
                    for p in list_of_prof[:3]:
                        msg = '\n'+msg1+' Name: '+p['Name']+' link:'+p['href']
                else:
                    for p in list_of_prof:
                        msg = '\n'+msg1+' Name: '+p['Name']+' link:'+p['href']

                dispatcher.utter_message(text=msg)

            else:
                msg = "Sorry No record found"
                dispatcher.utter_message(text=msg)

        return []
