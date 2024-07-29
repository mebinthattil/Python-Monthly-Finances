'''
NOTE
This is just dummy data.
Output data should like the table given below.
Vendor Names categorized into categories
Vendor Names categories to be inserted with a blank line above and below for better visibility
Category names must be in the format : "--<category name>--"

|----------|-----------------|-----------------------------|------|--------|-------|
| Txn Date | Mode (Card,UPI) |Vendor Name                  |Debit | Credit |Balance|
|----------|-----------------|-----------------------------|------|--------|-------|
|          |                 |                             |      |        |       |
|          |                 |--Food & Transportation--    |      |        |       |
|          |                 |                             |      |        |       |
|01-06-2024|debit card       |Zomato                       |632   |        |803360 |
|03-06-2024|UPI              |Ola                          |1210  |        |803560 |
|          |                 |                             |      |        |       |
|          |                 |--Shopping--                 |      |        |       |
|          |                 |                             |      |        |       |
|05-06-2024|UPI              |Amazon                       |      |320     |803860 |
|06-06-2024|Internet Banking |Flipkart                     |1000  |        |802360 |
|----------|-----------------|-----------------------------|------|--------|-------|


'''
#imports
import csv
import os, sys, subprocess
from categorizer_llm import categorize


#Getting file path info from user
file_path = "CleanCSV.csv"

#Creating Category Keywords Dictionary
keywords_file_object = open("Category Keywords.txt", 'r')
keyword_dictionary = eval(keywords_file_object.read())
keywords_file_object.close()
print("\nStarted Categorizing Data...\n")

#reading data from dump csv
file_object = open(r'{}'.format(file_path), 'r')
data = list(csv.reader(file_object))
#data in format ['Date','Payment Mode','Vendor','Debit','Credit','Balance']
number_of_entries = len(data)
number_of_entries_categorized, number_of_entries_categorized_llm = 0, 0
'''
Trying to create 8 lists
1. Header List
2. Tuition & Hostel Fees List
3. Reccuring Payment & Subscriptions List
4. Books & Supplies List
5. Food & Transportation List
6. Shopping List
7. Un-Indexed Expenditures List
8. Credit Sources List
At the end merge them and dump to new csv file
'''


'''Creating 7 Lists'''
header = [data[0]]
Tuition_and_Hostel_Fees = [['','','','','',''],['------','------','Tuition & Hostel Fees','------','------','------'],['','','','','',''],]
Reccuring_Payment_and_Subscriptions_List = [['','','','','',''],['------','------','Reccuring Payment & Subscriptions','------','------','------'],['','','','','',''],]
Books_and_Supplies_List = [['','','','','',''],['------','------','Books & Supplies','------','------','------'],['','','','','',''],]
Food_and_Transportation_List = [['','','','','',''],['------','------','Food & Transportation','------','------','------'],['','','','','',''],]
Shopping_List = [['','','','','',''],['------','------','Shopping','------','------','------'],['','','','','',''],]
Un_Indexed_Expenditures_List = [['','','','','',''],['------','------','Un-Indexed Expenditures','------','------','------'],['','','','','',''],]
Credit_Sources = [['','','','','',''],['------','------','Credited Txn','------','------','------'],['','','','','',''],]
#Checking which list each entry falls into 

for rows in data[1:]:
    status = False #status = False --> did not categorise into any of the lists.    status = True --> Categorised into one of the 8 lists
    for items in [element.lower() for element in keyword_dictionary["Tuition & Hostel Fees"]]:
        if items in rows[2].lower():
            Tuition_and_Hostel_Fees.append(rows)
            status, number_of_entries_categorized = True, number_of_entries_categorized + 1
            break
    
    for items in [element.lower() for element in keyword_dictionary["Reccuring Payment & Subscriptions"]]:
        if items in rows[2].lower():
            Reccuring_Payment_and_Subscriptions_List.append(rows)
            status, number_of_entries_categorized = True, number_of_entries_categorized + 1
            break
    
    for items in [element.lower() for element in keyword_dictionary["Books & Supplies"]]:
        if items in rows[2].lower():
            Books_and_Supplies_List.append(rows)
            status, number_of_entries_categorized = True, number_of_entries_categorized + 1
            break
    
    for items in [element.lower() for element in keyword_dictionary["Food & Transportation"]]:
        if items in rows[2].lower():
            Food_and_Transportation_List.append(rows)
            status, number_of_entries_categorized = True, number_of_entries_categorized + 1
            break
    
    for items in [element.lower() for element in keyword_dictionary["Shopping"]]:
        if items in rows[2].lower():
            Shopping_List.append(rows)
            status, number_of_entries_categorized = True, number_of_entries_categorized + 1
            break
    else: # anything that is a credit txn or unindexed txn goes here
        if rows[3] == ' ': # anything that is a credit txn goes here
            Credit_Sources.append(rows)
            status, number_of_entries_categorized = True, number_of_entries_categorized + 1 # keeping credit txns seperate 

        else: 
######################################################################################################################
            if not status: # anything that is unindexed goes here
                '''Once we reach a txn that is unindexed, we do two things
                1. Run categorizer llm to check if it can identify
                2. Once it identifies, update to 'Keyword_Dictionary.py' so that we dont need to run the llm again for same vendor'''
                print("\nCategorizing new vendor ", number_of_entries_categorized_llm,'done...\n')
                llm_categorized_topic = categorize(rows[2])
                if llm_categorized_topic == "Tuition & Hostel Fees":
                    Tuition_and_Hostel_Fees.append(rows)
                    keyword_dictionary["Tuition & Hostel Fees"].append(rows[2])
                    number_of_entries_categorized_llm += 1

                elif llm_categorized_topic == "Reccuring Payment & Subscriptions":
                    Reccuring_Payment_and_Subscriptions_List.append(rows)
                    keyword_dictionary["Reccuring Payment & Subscriptions"].append(rows[2])
                    number_of_entries_categorized_llm += 1

                elif llm_categorized_topic == "Books & Supplies":
                    Reccuring_Payment_and_Subscriptions_List.append(rows)
                    keyword_dictionary["Books & Supplies"].append(rows[2])
                    number_of_entries_categorized_llm += 1

                elif llm_categorized_topic == "Food & Transportation":
                    Reccuring_Payment_and_Subscriptions_List.append(rows)
                    keyword_dictionary["Food & Transportation"].append(rows[2])
                    number_of_entries_categorized_llm += 1

                elif llm_categorized_topic == "Shopping":
                    Reccuring_Payment_and_Subscriptions_List.append(rows)
                    keyword_dictionary["Shopping"].append(rows[2])
                    number_of_entries_categorized_llm += 1
                
                else:
                    Un_Indexed_Expenditures_List.append(rows)
                    keyword_dictionary["Un-Indexed Expenditures"].append(rows[2])
                    number_of_entries_categorized_llm += 1

                #Now updating changes to keyword_dictionary.txt
                keywords_file_object = open("Category Keywords.txt", 'w')
                keywords_file_object.write(str(keyword_dictionary))
                keywords_file_object.close()
        
final_list = header + Tuition_and_Hostel_Fees + Reccuring_Payment_and_Subscriptions_List + Books_and_Supplies_List + Food_and_Transportation_List + Shopping_List + Un_Indexed_Expenditures_List + Credit_Sources

'''Writing to a csv file'''

new_file_object = open("Categorized.csv", 'w', newline='')
writer_object = csv.writer(new_file_object)
writer_object.writerows(final_list)
new_file_object.close()

'''Done writing to a  new CSV'''

file_object.close()

print("\n\n\nDone with data categorization, Opening the file...")

os.remove("CleanCSV.csv")

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

open_file("Categorized.csv")