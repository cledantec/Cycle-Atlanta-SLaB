import json
import unicodecsv as csv

# flatten JSON hierarchy
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


files = ['imu.log']
data = []

# open file, read line-by-line
for file in files:
      for line in open(file):
            # replace single quotes with double quotes to conform with strict JSON
            line = line.replace("\'","\"")
            # convert to CSV-compatible format, append each result to data[]
            data.append(flatten_json(json.loads(line)))

# print(data)

# keys in first row
keys = data[0].keys()

# write to CSV file
with open('imu.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
    output_file.close()
