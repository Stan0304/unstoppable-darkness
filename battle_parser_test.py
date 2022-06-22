import battle_parser
import json


f = open('tests/text-to-result/result-training.txt',"r")
texts = f.readlines()

result = battle_parser.parse_text(texts, 'local')

print(json.dumps(result, indent=4, sort_keys=True))

f = open('tests/text-to-result/gold-war.txt',"r")
texts = f.readlines()

result = battle_parser.parse_text(texts, 'local')

print(json.dumps(result, indent=4, sort_keys=True))

