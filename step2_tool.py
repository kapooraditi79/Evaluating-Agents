from datetime import datetime
def get_time()->str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# describe the function to the model as a tool schema
tools= [ 
    {'type': 'function',
     'function':{
         'name': 'get_time',
         'description': 'Get the current local time',
         'parameters':{
             'type': 'object',
             'properties':{},
             'required':[]
         }
     }
     }
]