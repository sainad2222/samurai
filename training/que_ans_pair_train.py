import pandas as pd

# Load the CSV file
file_path = "/Users/sainath/Desktop/example_queries.csv"
data = pd.read_csv(file_path)

# Generate vn.train statements
for index, row in data.iterrows():
    question = row["Questions"]
    sql = row["SQL"]
    print(f'vn.train(question="""{question}""", sql="""{sql}""")')
