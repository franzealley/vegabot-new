def get_ingredient_nutrition(entities,user):
    # connect to db
    cursor = connection.cursor()

    # if no entity has been identified, set it to lunch as a default and start response
    if entities == False:
        entityname = 'calories'
        ingredientname = 'Asparagus'
        response = "I wasn't sure what kind of ingredient you needed information for " + user['first_name'] + ", but "
    # if an entity has been found, start the response as follows
    else:
        entityname = entities[0]
        ingredientname = entities[1]
        response = response = user['first_name'] + ' '

    # select recipes where the recipe time matches the entity given
    query = ("SELECT" + entityname +" FROM vegabot.recipe WHERE ingredientName  LIKE '%" + ingredientname + "%'")

    # execute the query
    cursor.execute(query)

    # get all rows from query
    rows = cursor.fetchall()

    # pick a random row from the results
    nutritionInfo = rows[1]
    response += ingredientname + ' contains {}'.format(nutritionInfo[0])

    return response

def get_nutrition(entities,user):
    cursor = connection.cursor()

    # if no entity has been identified, set it to lunch as a default and start response
    if entities == False:
        entityname = 'calcium'
        ingredientname = 'Asparagus'
        response = "I wasn't sure what kind of ingredient you needed information for " + user['first_name'] + ", but "
    # if an entity has been found, start the response as follows
    else:
        entityname = entities[0]
        ingredientname = entities[1]
        response = response = user['first_name'] + ' '

    # select recipes where the recipe time matches the entity given
    query = ("SELECT MAX("+entityname+"), ingredientName FROM vegabot.recipe")

    # execute the query
    cursor.execute(query)

    # get all rows from query
    rows = cursor.fetchall()

    # pick a random row from the results
    nutritionInfo = rows[1]
    response += ingredientname + ' contains {}'.format(nutritionInfo[0])

    return response

,
      {
        "text":"Can you tell me which foods are high in calcium?",
        "intent":"get_nutrition",
        "entities":[
          {
            "start":31,
            "end": 35,
            "value": "high",
            "entity": "level"
          },
          {
            "start":39,
            "end": 46,
            "value": "calcium",
            "entity": "ingredientName"
          }
        ]
      },
      {
        "text":"Which foods are high in calcium?",
        "intent":"get_nutrition",
        "entities":[
          {
            "start":16,
            "end": 20,
            "value": "high",
            "entity": "level"
          },
          {
            "start":24,
            "end": 31,
            "value": "calcium",
            "entity": "ingredientName"
          }
        ]
      },
      {
        "text":"Which foods are high in fat?",
        "intent":"get_nutrition",
        "entities":[
          {
            "start":23,
            "end": 26,
            "value": "fat",
            "entity": "ingredientName"
          },
          {
            "start":16,
            "end": 20,
            "value": "high",
            "entity": "level"
          }

        ]
      },
      {
        "text":"Which foods are low in fat?",
        "intent":"get_nutrition",
        "entities":[
          {
            "start":23,
            "end": 26,
            "value": "fat",
            "entity": "ingredientName"
          },
          {
            "start":16,
            "end": 19,
            "value": "low",
            "entity": "level"
          }
        ]
      },
      {
        "text":"Are there any good ingredients that are high in calcium?",
        "intent":"get_nutrition",
        "entities":[
          {
            "start":48,
            "end": 55,
            "value": "calcium",
            "entity": "ingredientName"
          },
          {
            "start":40,
            "end": 44,
            "value": "high",
            "entity": "level"
          }
        ]
      },
      {
        "text":"Are there any good ingredients that are high in zinc?",
        "intent":"get_nutrition",
        "entities":[
          {
            "start":48,
            "end": 52,
            "value": "zinc",
            "entity": "ingredientName"
          },
          {
            "start":40,
            "end": 44,
            "value": "high",
            "entity": "level"
          }
        ]
      },
      {
        "text":"Can you tell me how many calories are in broccoli?",
        "intent":"get_ingredient_nutrition",
        "entities":[
          {
            "start":40,
            "end": 48,
            "value": "broccoli",
            "entity": "ingredientName"
          },
          {
            "start":25,
            "end": 33,
            "value": "calories",
            "entity": "fieldName"
          }
        ]
      },
      {
        "text":"Can you tell me how many calories are in spinach?",
        "intent":"get_ingredient_nutrition",
        "entities":[
          {
            "start":40,
            "end": 47,
            "value": "spinach",
            "entity": "ingredientName"
          },
          {
            "start":25,
            "end": 33,
            "value": "calories",
            "entity": "fieldName"
          }
        ]
      },
      {
        "text":"Can you tell me how much iron is in broccoli?",
        "intent":"get_ingredient_nutrition",
        "entities":[
          {
            "start":35,
            "end": 43,
            "value": "broccoli",
            "entity": "ingredientName"
          },
          {
            "start":24,
            "end": 27,
            "value": "iron",
            "entity": "fieldName"
          }
        ]
      },
      {
        "text":"Can you tell me how much zinc is in broccoli?",
        "intent":"get_ingredient_nutrition",
        "entities":[
          {
            "start":37,
            "end": 45,
            "value": "broccoli",
            "entity": "ingredientName"
          },
          {
            "start":25,
            "end": 29,
            "value": "zinc",
            "entity": "fieldName"
          }
        ]
      },
      {
        "text":"Can you tell me how much iron is in spinach?",
        "intent":"get_ingredient_nutrition",
        "entities":[
          {
            "start":37,
            "end": 44,
            "value": "spinach",
            "entity": "ingredientName"
          },
          {
            "start":25,
            "end": 29,
            "value": "iron",
            "entity": "fieldName"
          }
        ]
      }





