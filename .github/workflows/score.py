import os
import json
import sys
import re
import openai
from radon.visitors import ComplexityVisitor
from radon.complexity import cc_visit
from dotenv import load_dotenv
load_dotenv()
N = 10
openai.api_key = os.getenv("OPENAI_API_KEY")

print(sys.version)

env_file = os.getenv("updatedFiles")
print(env_file)
old_and_new_code = json.dumps(env_file)
print(json.loads(env_file))
print("ENV:", old_and_new_code)

def call_Chat_gpt_for_time_and_space_complexity(content):
  chat_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": "You will be provided with Python code, give only Time complexity and Space Complexity all functions in json fomat with no explation"
      },
      {
        "role": "user",
        "content": content
      }
    ],
    temperature=0,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  # print(chat_response)
  return chat_response['choices'][0]['message']['content']

def get_cyclomitic_complexity(fun):
#   v = ComplexityVisitor.from_code(fun)
#   result = v.functions
#   print(result)
  return cc_visit(fun)


def convert_complexity_to_number(complexity):
  final_comp = 1
  complexity = complexity[2:-1]
  log_indexes = [i.start() for i in re.finditer('log', complexity)]
  complexity = complexity.replace('log', '')
#   complexity = complexity.replace(r'[A-Za-z]', r'n')
  complexity = re.sub(r'[a-zA-Z]', r'n', complexity)
  for id in log_indexes:
    complexity = complexity[:id+1]+"log"+complexity[id+1:]
  complexity = complexity.replace('  ', '')
#   print(complexity)
  complexity = list(complexity)
#   print(complexity)
  i=0
  while i< len(complexity):
    if complexity[i]=="n":
       final_comp*=N
    elif complexity[i]=="l":
      final_comp*=1.2
      i+=3
    elif complexity[i]=="^":
      last=complexity[i-1]
      if last.isnumeric():
        last=int(last)
      else:
        last=N
      next = int(complexity[i+1]) if complexity[i+1].isnumeric() else N
      # print(final_comp,next,last)
      if final_comp>1:
        final_comp/=last
      if next>last:
        final_comp=final_comp * 100#math.pow(last,next)
      elif next==last:
        final_comp=final_comp * 150
      else:
        final_comp=final_comp * 70
      i+=1
    i+=1
  return final_comp
#   if 
def give_start_rating(old_score,new_score):
  delta = ((old_score-new_score)/old_score)*100
  if delta<=0:
    print("No Optimisation Required")
    return {'old_code': 4.5,
            'new_code': 4.5}
  
  else:
    if 0<delta<=20:
      return {'old_code': 4 ,
            'new_code': 4.5 }
    elif 20<delta<=50:
      return {'old_code': 3 ,
            'new_code': 4.5 }
    elif 50<delta<=75:
      return {'old_code': 2.5 ,
            'new_code': 4.5 }
    else:
      return {'old_code': 1.5 ,
            'new_code': 4.5 }


def get_score_for_code(file_path):
    file = open(file_path, "r")
    fun = file.read()
    file.close()
    print("Calling ChatGPT API to Get Complexities")
    resp = call_Chat_gpt_for_time_and_space_complexity(fun)
    resp = json.loads(resp)
    # print(resp)


    # resp = {'cal_n': {'time_complexity': 'O(n)', 'space_complexity': 'O(1)'}, 'cal_nlogn': {'time_complexity': 'O(n log n)', 'space_complexity': 'O(1)'}, 'cal_n_n': {'time_complexity': 'O(n^2)', 'space_complexity': 'O(1)'}, 'bubbleSort': {'time_complexity': 'O(n^2)', 'space_complexity': 'O(1)'}}
    print("Getting Cyclomatic Complexity")
    cyclo_comp = get_cyclomitic_complexity(fun=fun)
    # print(cyclo_comp)

    for c in cyclo_comp:
        name, comp = c.name, c.complexity
        resp[name]["cyclo_complexity"] = comp
    

    for res in resp:
        code = resp[res]
        score = convert_complexity_to_number(code["time_complexity"])+convert_complexity_to_number(code["space_complexity"])+code["cyclo_complexity"]
        resp[res]["score"] = score
        # print(score)
    
    return resp