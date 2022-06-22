import battle_parser
import json

f = open('logs/533dba1b9ce33e0421c77ea05673656449fa3bb179b5f61ac21b3663fb31bfd8-input.txt',"r")
texts = f.readlines()

result = battle_parser.parse_text(texts, 'local')

print(json.dumps(result, indent=4, sort_keys=True))
