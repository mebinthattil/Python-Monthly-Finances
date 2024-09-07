'''
NOTE
This is just dummy data.
Output data should like the table given below.
All "Modes" to be indexed have been given the table below.

|----------|-----------------|---------------|------|--------|-------|
| Txn Date | Mode (Card,UPI) |Vendor Name    |Debit | Credit |Balance|
|----------|-----------------|---------------|------|--------|-------|
|01-06-2024|debit card       |KANTI SWEETS   |632   |        |100000 |
|03-06-2024|UPI              |Truffles       |1210  |        |100000 |
|05-06-2024|UPI              |SomeDude       |      |320     |100000 |
|06-06-2024|Internet Banking |BITS           |1000  |        |100000 |
|08-06-2024|NEFT             |Maxi           |      |500     |100000 |
|----------|-----------------|---------------|------|--------|-------|

'''
#imports
import csv
import platform, subprocess
import os, sys


dev_mode = False #set dev mode to True, for acess to logs

if dev_mode:
    file_path = "Enter path to csv file here so you dont have to type it again and again".strip("\"\"")
else:
    file_path = input("Enter the path of csv file: ").strip("\"\"")

print("\n\n\nStarted extracting useful data from file...\n")

#reading data from dump csv
if sys.platform == "win32":
    file_object = open(r'{}'.format(file_path), 'r')
    data = list(csv.reader(file_object))
else:
    file_object = open(r'{}'.format(file_path), 'r', newline = '')
    data = list(csv.reader(file_object, delimiter='\t'))

#cleaning up and adding only relavant transaction data to 'processed_data_list'
processed_data_list = []
target_row_number = 0
for i in range(len(data)):
    if "Txn Date" in data[i][0]:
        target_row_number = i
        break

    
             
            
        


for row in data[target_row_number:]:
    processed_data_list.append(row)
#modifying header in list
#processed_data_list[0][0],processed_data_list[0][1],processed_data_list[0][2],processed_data_list[0][3] = "Date", "Payment Mode", "Vendor", "Debit"
processed_data_list[0] = ['Date','Payment Mode','Vendor','Debit','Credit','Balance']

# Header now looks like ['Date','Payment Mode','Vendor','Debit','Credit','Balance']    

#converting processed_data_list to proper format
formated_list = []
for i in processed_data_list[1:-2]:
    text = i[0].replace(",,", ',Ref No. Not Found,')
    text = text.replace(", ,",',0,')
    l = text.split('"')
    nl = l[0].split(',') + l[1:]
    while '' in nl:
        nl.remove('')
    nl = [nl[0]] + [nl[2].strip()] +[nl[4]] +[nl[5]] +[nl[-1]]
    if dev_mode:
        print("String to list:",nl)
    formated_list.append(nl)

#creating the final list which we will return at the end
export_list = []
export_list.append(processed_data_list[0]) #adding header

#cleaning up each transaction details by extracting mode of payment, vendor, etc.
for rows in formated_list:
    sublist = [] #sublist should be in format ['Date','Payment Mode','Vendor','Debit','Credit','Balance',]
    rows_copy = rows.copy()
#########################################################################
    '''Adding date to sublist'''
    sublist.append(rows[0]) 
##########################################################################
    '''adding Payment Mode to sublist'''

    if "upi" in rows[1].lower():
        sublist.append("UPI")
    elif "debit card" in rows[1].lower():
        sublist.append("Debit Card")
    elif "inb" in rows[1].lower():
        sublist.append("Internet Banking")
    elif "neft" in rows[1].lower():
        sublist.append("NEFT")
    else:
        sublist.append("Un-identifiable")

    '''Done with Payment Mode to sublist'''
############################################################################
    '''#adding Vendor info to sublist'''
    
    #finding lowest index of a numeric character
    for i in range(len(rows[1])):
        if rows[1][i].isnumeric():
            first_number_index = i
            break  
    
    #slicing the string
    rows[1] = rows[1][(first_number_index+1):]

    #finding first instance of alphabet
    for i in range(len(rows[1])):
        if rows[1][i].isalpha():
            first_alpha_index = i
            break
    
    #slicing string again
    rows[1] = rows[1][(first_alpha_index):]
    
    #finding next instance of '/'
    for i in range(len(rows[1])):
        if rows[1][i] == '/':
            first_slash_index = i
            break
        else:
            first_slash_index = len(rows[1])

    #final string slicing
    rows[1] = rows[1][:first_slash_index]
        
    #removing '--' if in the end of the string
    if rows[1][:-3:-1] == "--":
        rows[1] = rows[1][:-2]
    
    #handling exception for NEFT and INB
    if 'inb' in rows_copy[1].lower():
        rows[1] = "INB NEFT TXN unsupported"
    elif 'neft' in rows_copy[1].lower():
        rows[1] = "INB NEFT TXN unsupported"

    
    #now rows[1] will be string with vendor name. Adding that to sublist
    sublist.append(rows[1][:24].strip())

    '''Done with adding Vendor name to sublist'''
##########################################################################################
    '''Adding Debit Info to sublist'''
    sublist.append(rows[2])
#########################################################################################
    '''Adding Credit Info to sublist'''
    sublist.append(rows[3])
#########################################################################################
    '''Adding Balance Info to sublist'''
    sublist.append(rows[4])
#########################################################################################
    '''  Sublist complete :) '''

    export_list.append(sublist)



'''Writing to a csv file'''

new_file_object = open("CleanCSV.csv", 'w', newline='')
writer_object = csv.writer(new_file_object)
writer_object.writerows(export_list)
new_file_object.close()

'''Done writing to a  new CSV'''

file_object.close()

print("\nData successfully extracted, Going to start categorizing Data...\n")

if __name__ == '__main__':
    if platform.system() == "Windows":
        os.startfile("CleanCSV.csv")
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "CleanCSV.csv"])