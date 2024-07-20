import pandas as pd

# Load the CSV file
file_path = "/Users/kanishkkunal/Downloads/US Stocks Queries - CSV v2 (1).csv"
data = pd.read_csv(file_path)

# Generate vn.train statements
for index, row in data.iterrows():
    question = row["Questions"]
    sql = row["SQL"]
    print(f'vn.train(question="""{question}""", sql="""{sql}""")')
    
