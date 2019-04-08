#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger2.bot import Bot
import re

from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import os
from rasa_core.utils import EndpointConfig

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter

import json

#interpreter = RasaNLUInterpreter("models/nlu/default/vegabot",, lazy_init=False)

MODEL_PATH = "models/dialogue/"
#
# agent = Agent.load(MODEL_PATH,interpreter=interpreter)
#
# print(agent)

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEJrZBTxYqoBABc0lXzaZBqai7M6CpZC9CZCgkSYqX6SmpDivG7T1rIbHn88ft7pe2iguWWl1o71hoU87DqblFZAgKzqzReA66SnbZAhGuhFVMb3gPTzLqmmrkonhtlJlANjJbNbBbZB49uc9ldNGrkApG2NEZBXguyIGOMcQD6GwZDZD'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             port=8889
                             )





def train_bot(data_json,config_file,model_dir):
    training_data = load_data(data_json)
    trainer = Trainer(config.load(config_file))
    trainer.train(training_data)
    model_directory=trainer.persist(model_dir,fixed_model_name='vegabot')



def predict_intent(text):
    interpreter = Interpreter.load('models/nlu/default/vegabot')

    jsontext = interpreter.parse(text)
    json_string = json.dumps(jsontext)
    json_dict = json.loads(json_string)
    json_intent = json_dict["intent"]["name"]

    return json_intent

def get_entities(text):
    interpreter = Interpreter.load('models/nlu/default/vegabot')
    jsontext = interpreter.parse(text)
    json_string = json.dumps(jsontext)
    json_dict = json.loads(json_string)
    json_entities = json_dict["entities"]
    if json_entities:
        return json_entities[0]['entity'], json_entities[0]['value']
    else:
        return False



#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()

       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    user_details = bot.get_user_info(recipient_id)
                    user_message = message['message'].get('text')
                    intent = predict_intent(user_message)
                    entities = get_entities(user_message)
                    response_sent_text = get_message(intent, entities, user_details, user_message)
                    send_message(recipient_id, response_sent_text)

                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def say_hello(user):
    response = 'Hello there '+user['first_name'] + '! Is there anything I can help you with today?'

    return response

def convert_time(entityvalue,entityname):
    entityvalue =  entityvalue.replace(' minutes','')
    entityvalue = entityvalue.replace('under','<').replace('less than','<')
    entityvalue = entityvalue.replace('more than','>').replace('over','>')
    entityvalue = entityvalue.replace('an hour','60').replace('hour','60')

    if '<' in entityvalue or '>' in entityvalue:
        return entityvalue
    else:
        entityvalue = ' > {} and '.format(int(entityvalue)-10) +entityname+ ' < {}'.format(int(entityvalue)+10)
        return entityvalue


def create_query(entities):
    if entities == False:
        entityname = 'recipeType'
        entityvalue = 'lunch'
        query = ("SELECT * FROM vegabot.recipe WHERE " + entityname + " LIKE '%" + entityvalue + "%'")

    elif entities[0] =='mealTime':
        entityname = entities[0]
        entityvalue = entities[1]
        # select recipes where the recipe time matches the entity given
        query = ("SELECT * FROM vegabot.recipe WHERE " + entityname + " LIKE '%" + entityvalue + "%'")

    elif entities[0]=='recipeTime':
        entityname = entities[0]
        entityvalue = convert_time(entities[1],entityname)
        # select recipes where the recipe time matches the entity given
        query = ("SELECT * FROM vegabot.recipe WHERE " + entityname + entityvalue)
    return query

def start_response(entities,user):
    adjectives = ['tasty', 'delicious', 'fabulous', 'scrumptious']
    adjective = random.choice(adjectives)

    if entities == False:
        response = "I wasn't sure what kind of recipe you were after " + user['first_name'] + ", but here is a "

    elif entities[0] == 'mealTime':
        entityvalue = entities[1]
        response = response = str(entities) + ' ' + user['first_name'] + ', here is a ' + adjective + ' ' + entityvalue + 'time'

    elif entities[0] == 'recipeTime':
        response = response = str(entities) + ' ' + user['first_name'] + ', here is a ' + adjective

    return response

def get_recipe(entities,user):

    query = create_query(entities)
    response = start_response(entities,user)

    #connect to db
    cursor = connection.cursor()

    #execute the query
    cursor.execute(query)
    # get all rows from query
    rows = cursor.fetchall()

    tastes = get_tastes(user)
    likes = tastes[0]
    dislikes = tastes[1]


    if rows:
        #pick a random row from the results
        if dislikes:
            filteredRows = apply_tastes(rows,likes,dislikes)
            if filteredRows:
                recipe = random.choice(filteredRows)
            else:
                recipe = random.choice(rows)
        else:
            recipe = random.choice(rows)

        #complete the response with the recipe informatio from the database
        response += ' recipe for a {}\nYou will need:\n{}\nThe method is a follows:\n{}\nThis recipe takes approximately {} minutes'.format(recipe[1] + '!\n',recipe[2].replace(", ", "\n")+ '\n',recipe[3].replace(", ", "\n")+ '\n',str(recipe[6]))

    else:
        response = str(entities) + "Sorry I couldn't find anything like that in my recipe books"
    return response

#find all the user's tastes stored in preference table
def get_tastes(user):

    query = "SELECT * FROM vegabot.preference WHERE userID = '"+user['id']+"'"
    cursor = connection.cursor()

    # execute the query
    cursor.execute(query)
    # get all rows from query
    rows = cursor.fetchall()

    #start two empty lists of likes and dislikes
    likes = []
    dislikes = []

    #if there are preferences stored
    if rows:
        #for every row in the rows
        for row in rows:
            #if preference is a dislike
            if row[3]=='0':
                #add the ingredient name to the dislike list
                dislikes.append(row[2])
            #else if the preference is a like
            elif row[3]=='1':
                #add the ingredient name to like list
                likes.append(row[2])
    #return two lists, one with liked ingredients and dislike ingredients
    #we can then run a check in apply_tastes to ensure these are factored in to the recipe result sent back to the user
    return likes,dislikes

#filter results from recipe table to factor in the user's dislikes
def apply_tastes(rows,likes,dislikes):

    #convert row tuple to list so it is mutable
    rows = list(rows)
    #for every row in the rows of results
    for row in rows:
        #for every dislike in the dislikes list
        for dislike in dislikes:
            #if this dislike is found in the ingredients field of the recipe row
            if dislike in row[2]:
                #remove this row from the rows of results (the user won't want to cook a recipe that contains a disliked ingredient)
                rows.remove(row)
            else:
                #continue as we want to keep other rows
                continue
    #returned the new filtered list of rows
    return rows

#convert text e.g. 'I like spinach' to a numeric value, either 0 or 1
def like_or_dislike(message):

    #if message contains dislike or dont like then set likeValue to 0 (to be stored in db)
    if 'dislike' in message or "don't like" in message:
        likeValue = '0'
    #else change to 1 to store ingredient as a LIKE in db
    else:
        likeValue = '1'

    #return value for use in check_memory func
    return likeValue

#first we must check whether the vegabot already knows the user likes/dislikes this food ingredient
def check_memory(entities,user,message):

    #if the bot has trouble recognising a food entity from the message it will just reply with a standard response and do nothing
    if entities == False:
        response = "Sorry, I'm not sure I know that ingredient."
        return response
    else:
        #set ingredient to equal the 2nd item from the entities list returned
        ingredient = entities[1]
        #userID comes from facebook's data
        userID = user['id']
        #get whether the user likes or dislikes this ingredient from func that converts text to '0' or '1'
        likeValue = like_or_dislike(message)

        #run a query to see if this preference is already stored in the db
        query = "SELECT * FROM vegabot.preference WHERE userID='"+userID+"' AND ingredientName='"+ingredient+"'"

        #connect to db
        cursor = connection.cursor()

        # execute the query
        cursor.execute(query)

        rows = cursor.fetchall()
        #if preference is already stored
        if rows:
            row = rows[0]
            # if the user has repeated info e.g. i like spinach and spinach is stored as a LIKE in the db then do nothing but return a response
            if row[3]== likeValue:
                response = 'I already know this but thank you for reminding me'
                return response
            #else if the preference of spinach is stored as a like but the user now says they dislike the ingredient then update the preference to dislike (or like depending on what its currently stored as)
            elif row[3] != likeValue:
                #update query
                query = "UPDATE vegabot.preference SET userLike='"+likeValue+"' WHERE userID='"+userID+"' AND ingredientName='"+ingredient+"'"
                #response to represent the change
                response = "Oh! So you have changed your mind about {}. I will remember this in future.".format(ingredient)
                #run query
                store_preference(query)
                return response
        #if the preference isnt currently stored then run an insert query to store it
        else:
            query = "INSERT INTO vegabot.preference (userID,ingredientName,userLike) VALUES ('" + userID + "','" + ingredient + "'," + likeValue + ")"
            response = 'Thank you for letting me know. I will try to remember this in future.'
            #runs query
            store_preference(query)
            return response

#runs query to store food like/dislike in preference table
def store_preference(query):

    # connect to db
    cursor = connection.cursor()

    # execute the query
    cursor.execute(query)
    cursor.close()
    #commit is required to commit all changes to db
    connection.commit()

#function to recite privacy policy to user when requested
def recite_privacy_policy(user):
    #fixed standard response
    response = "I was developed by a university student for their final year project and was not built for commercial use.\n\nThrough Facebook I can access only your full name and profile picture, however, lovely as it is, I make no use of your profile picture. I may use your first name from time to time as I find this makes my responses more personal.\n\nI only store your food ingredient likes and dislikes. You can give me this information by stating 'I like ingredientname' or 'I dislike ingredientname'. This data is stored in a safe and secure database. You can ask me to remove this data at any time.\n\nThe data stored about you is not accessible to anyone other than the developer of this chatbot and is not used anywhere other than this application.\n\nI hope this makes you feel more reassured when talking to me, {}.".format(user['first_name'])
    return response

#function to recite vegabot introduction when asked
def introduction(user):
    #fixed response
    response = "Well {}, I am a simple recipe chatbot built by a final year Computing student. You can ask me for a range of recipes: dinner time, breakfast, recipes under 15 minutes, etc. and I will do my best to find a recipe that's right for you.\n\nYou can tell me a bit about what you like and don't like so I can pick recipes that I know you'll enjoy. Just tell me 'I like ingredientname' or 'I dislike ingredientname' and I'll bear that in mind when finding you a recipe.\n\nIf you want to know anything about the privacy and safety of your data when talking to me then just ask!".format(user['first_name'])
    return response

#chooses a random message to send to the user
def get_message(intent,entities,user,message):

    if intent == 'greeting':
        response = say_hello(user)
    elif intent == 'get_recipe':
        response = get_recipe(entities, user)
    elif intent == 'store_preference':
        response = check_memory(entities, user,message)
    elif intent == 'recite_privacy_policy':
        response = recite_privacy_policy(user)
    elif intent == 'introduce_yourself':
        response = introduction(user)
    else:
        response = "Sorry I'm not sure I understand you. As I am only a prototype, I can only tell you about recipes."
    return response


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response, 'REGULAR')
    return "success"

if __name__ == "__main__":
    app.run()