import pandas as pd

# Load the CSV file
file_path = "/Users/kanishkkunal/Downloads/Untitled spreadsheet.csv"
data = pd.read_csv(file_path)

# Generate vn.train statements
for index, row in data.iterrows():
    question = row["Documentation"]
    print(f'vn.train(documentation="""{question}""")')
