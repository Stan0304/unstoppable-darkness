import battle_parser2
import json

f = open('logs/b7b45d8a64ae7f8d2bd549a9f726d5114d3272509f0eb40281e6a01dc581e237-input.txt',"r")
texts = f.readlines()

result = battle_parser2.parse_text(texts, 'local', 'test')

print(json.dumps(result, indent=4, sort_keys=True))
