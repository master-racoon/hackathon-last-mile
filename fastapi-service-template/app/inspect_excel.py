import pandas as pd

df = pd.read_excel('/tmp/open_orders.xlsx')
print('Shape:', df.shape)
print('\nColumns:')
for col in df.columns:
    print(f'  - {col}')
print('\n=== First 5 rows ===')
print(df.head(5).to_string(index=False))
print('\n=== Data types ===')
print(df.dtypes.to_string())
print('\n=== Sample values for key fields ===')
for col in df.columns[:10]:
    print(f'\n{col}:')
    print(f'  Sample: {df[col].dropna().head(3).tolist()}')
    print(f'  Unique count: {df[col].nunique()}')
