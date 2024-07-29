# Python-Monthly-Finances

## Things to be done on own:
1. Run main.py script
2. Move sheet from categorized csv to budget tracker csv (For detailed excel formulas and graphs)
3. Note bank statement csv file must be 'csv -utf8' format.
4. For acessing AI categorization Llama3 must be installed locally.


## Adding Category Keywords
Default: AI automatically categorizes into specified topics.
Manual: If you want to add for example "Myntra" as part of shopping, just add it in "Category Keywords.txt".



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
                     --> These groups are sorted based on keywords updated automatically in the "Category Keywords.txt"
                     --> Finally puts the categorized data into "Categorized.csv" and deleted the intermediate "CleanCSV.csv" file.

### 4. Categorizer_LLM + Ollama Tuning Files
                    --> CategorizerLLM: Takes any vendor name and categorises them into one of the user predefined topics (Eg: Travel, Shopping, etc).
                    --> Ollama Tuning: System prompt for Llama 3 (7B)
                    

