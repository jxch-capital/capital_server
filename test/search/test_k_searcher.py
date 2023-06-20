import pandas as pd

data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

arr = df.values
print(arr)

arr = df.to_numpy()
print(arr)