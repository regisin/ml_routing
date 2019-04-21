import pandas as pd

list_of_csv_filenames = [
    '1.csv',
    '2.csv',
    '3.csv',
    '4.csv',
    '5.csv',
    '6.csv',
    '7.csv',
    '8.csv',
    # 't9.csv',
    # 't10.csv',
]

output_csv_filename = 'train_data.csv'

data = pd.read_csv(list_of_csv_filenames[0])

for f in list_of_csv_filenames[1:]:
    data = data.append(pd.read_csv(f))

data.to_csv(output_csv_filename, index=False)
