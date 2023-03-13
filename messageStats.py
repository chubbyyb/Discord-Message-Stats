# last updated: 03/13/2023

import os
import time
import csv
import json
import re
import graphMessages
import commonWords

# Initilization
path = r"package\messages"
entries = os.listdir(path)
entries.remove("index.json")
dirs = []
length = entries.__len__()
i = 0
n = 0
j = 0
k = 1
found = 0
notFound = 0
row_count = 0
messages = [[],[],[]]
displayGraph = False
displayCommonWords = False


# Loading bar
def loadbar(iteration, total, prefix='',suffix='',decimals=1,length=100,fill='>'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}& {suffix}', end='\r')
    if iteration == total:
        print()


# Convert number to number with commas
def commas(number):
    return ("{:,}".format(number))



#  x[0][1] > x[0][2] should also change x[1][1] > x[1][2] and so on
def sort_3d_array(array):
    # create a list of tuples that contain the corresponding elements from all three subarrays
    tuples_list = list(zip(array[0], array[1], array[2]))
    # sort the list of tuples based on the values from the first subarray
    sorted_tuples = sorted(tuples_list, key=lambda x: x[0])
    # extract the sorted subarrays from the sorted list of tuples
    sorted_array = [
        [t[0] for t in sorted_tuples],
        [t[1] for t in sorted_tuples],
        [t[2] for t in sorted_tuples]
    ]
    return sorted_array


# Incase user wants to change path
if(input("The current path is: "+path+"\nDo you want to change the path? (Y/N): ").lower() == "y"):
    path = input("Enter your path: ")
    print("The new path is: "+path)

if(input("Would you like to graph your overall messages? (Y/N) [EXPERIMENTAL]").lower() == "y"):
    displayGraph = True
    if(input("Would you like to graph your overall messages? (Y/N) [EXPERIMENTAL]").lower() == "y"):
        displayCommonWords = True





# Get all the message file paths
while i != length:
    dirs.append(os.path.join(path,entries[i],"messages.csv"))
    i=i+1
    loadbar(i,length,prefix="Getting paths",suffix="Complete",length=50)
    time.sleep(0.001)


# Prevent fuckshittery
time.sleep(1)

# Read the amount of rows in each messages.csv to count all messages
while n != length:
    with open(dirs[n], 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row if it exists
        header = next(csv_reader, None)

        # Count the remaining rows
        sumRows = sum(1 for row in csv_reader)
        row_count = row_count+sumRows
        messages[0].append(sumRows)

        # Log the user ID in order to pass it to message statistics
        number = re.findall(r'\d+', str(entries[n]))
        messages[1].append(number)
        

    n=n+1
    loadbar(n,length,prefix="Counting messages",suffix="Complete",length=50)



print("You have "+str(commas(row_count))+" messages")


# Get message statistics
with open(os.path.join(path,'index.json'), 'r') as file:
    data = json.load(file)

while j != length:
    search_key = str(messages[1][j]).replace('[','',-1).replace(']','',-1).replace('\'','',-1)
    search_result = data.get(str(search_key))
    j=j+1

    # Print the search result
    if search_result:
        found = found+1
        messages[2].append(search_result)
    else:
        notFound = notFound+1
        messages[2].append('null')

messagesSorted = sort_3d_array(messages)
userDisplay = int(input("\n\nHow many would you like to display? "))
print("Top messages:\n")

while(userDisplay != 0):
    
    print("#"+str(k)+" "
          +str(messagesSorted[2][length-k]).replace("Direct Message with ","")
          +" ["+str(commas(messagesSorted[0][length-k]))+" Messages]")
    
    userDisplay = userDisplay-1
    k = k+1

print("Your total messages are: "+str(commas(row_count)))


if displayGraph == True:
    print("Graphing your messages...")
    graphMessages.graph()

if displayCommonWords == True:
    print("Getting most common words...")
    commonWords.wordStats()
