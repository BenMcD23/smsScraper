import ast

with open('data.txt', 'r') as file:
    data = file.read()

data = ast.literal_eval(data)

firstname = "Kelsey"
lastname = "Evans"

# loop each event
for i in data:
    # each event without the name of the event
    temp = i[1:]
    for j in temp:
        # print(j)
        for k in j:
            if len(k) > 3:
                if k[1] == firstname and k[2] == lastname and (k[3]=="Selected" or k[3]=="Bidding" or k[3]=="Reserve"):
                    print(i[0])