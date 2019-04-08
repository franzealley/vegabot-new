from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import random
import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             port=8889
                             )

from rasa_core.actions import Action
from rasa_core.events import SlotSet

class GetRecipe(Action):

    def name(self):
        return "get_recipe"

    def run(self,dispatcher,tracker,domain):
        # type: (Dispatcher,DialogueStateTracker,Domain)->List[Event]
        meal_time = tracker.get_slot('mealtime')

        cursor = connection.cursor()

        query = ("SELECT * FROM vegabot.recipe WHERE recipeTime LIKE '%" + meal_time + "%'")

        cursor.execute(query)

        rows = cursor.fetchall()

        return random.choice(rows)

recipe = GetRecipe()

recipe.run(dispatcher,tracker,domain)
