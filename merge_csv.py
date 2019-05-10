import pandas as pd

import sys
import os

output_csv_filename = 'train_data.csv'
list_of_csv_filenames = []
if len(sys.argv) >= 2:
    list_of_csv_filenames = [str(f) for f in sys.argv[1:-1] if os.path.isfile(f)]
    output_csv_filename = str(sys.argv[-1])

data = pd.read_csv(list_of_csv_filenames[0])

for f in list_of_csv_filenames[1:]:
    if os.path.isfile(f):
        data = data.append(pd.read_csv(f))

data.to_csv(output_csv_filename, index=False)
