import json

with open("postalcodes.json") as read_file:
   data = json.load(read_file)

for i in data:
    if i['POSTAL'] == '603286':
        print(i['ADDRESS'])
        print(i['LATITUDE'])
        print(i['LONGITUDE'])
