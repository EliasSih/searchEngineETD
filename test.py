import openai #Need to import this

def chatGPTQuery(context, prompt):

    openai.api_key = "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"

    messages = []
    messages=[
        {"role": "system", "content": "I will first give you a list of document titles and then I will give you a query to a search engine and you will return an expanded search query based on these document titles"},
        {"role": "user", "content": context},
        {"role": "user", "content": prompt}
    ]

    query = {}
    query['role'] = 'user'
    query['content'] = prompt
    #messages.append(query)
    

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    try:
        result = response['choices'][0]['message']['content']
    except:
        result = "Please try another query, if problem persist, try again later."
    return result

context = "The biology and systematics of frogs : contributions submitted to The University of Adelaide, Morphology and systematics of the Solomon Island Ranid frogs, Edible frog harvesting in Indonesia: evaluating its impact and ecological context"

originalQuery = "biology of frogs"
print(chatGPTQuery(context, originalQuery))