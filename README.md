# Python-Monthly-Finances

## Things to be done on own:
1. Run main.py script
2. Move sheet from categorized csv to budget tracker csv
3. Copy Paste from categorized sheet to main sheet to get acess to all the formulas and charts present in the main sheet



## Adding Category Keywords
If you want to add for example "Myntra" as part of shopping, just add it in "Category Keywords.txt" and everything else will take care of itself.



## Files Used:

### 1. Category Indexing 
                     --> Key value pair dictionary in the format : {category name : [vendor1, vendor2, etc]}
                     --> Eg: {Travel: ['Uber', 'Ola']}



### 2. Clean CSV generator
                     --> Extracts useful data from the dumped csv file.
                     --> Extracted data in the format ['Date','Payment Mode','Vendor','Debit','Credit','Balance']
                     --> Puts extracted data into the csv file 'CleanCSV.csv'



### 3. CSV Categorizer 
                     --> Takes data from 'CleanCSV.csv' as input to organise into groups
                     --> These groups are sorted based on keywords updated manually in the "Category Keywords.txt"
                     --> Finally puts the categorized data into "Categorized.csv" and deleted the intermediate "CleanCSV.csv" file.


### NOTE: Currently only tested for SBI Statements