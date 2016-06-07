'''
Created on May 31, 2016

@author: qwaider
'''
from main import MLR_train
if __name__ == '__main__':
    
   # MLR_train.main(["-t" ,"train" ,"-f" ,"fff" ,"-m","mmk"])
    import json

config = {'key1': 'value1', 'key2': 'value2'}

with open('config.json', 'w') as f:
    json.dump(config, f)
    pass