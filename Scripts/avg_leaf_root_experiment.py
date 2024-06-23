import pandas as pd
import numpy as np

file_path = 'example.csv'  
df = pd.read_csv(file_path)

df['elapsed_time'] = pd.to_numeric(df['elapsed_time'], errors='coerce')
#df.loc[df['elapsed_time'] < 1, 'elapsed_time'] = 0
df['terminal_calls'] = pd.to_numeric(df['terminal_calls'], errors='coerce')
#df.loc[df['terminal_calls'] < 1, 'terminal_calls'] = 0
df['cache_hits'] = pd.to_numeric(df['cache_hits'], errors='coerce')
#df.loc[df['cache_hits'] < 1, 'cache_hits'] = 0
df['cache_misses'] = pd.to_numeric(df['cache_misses'], errors='coerce')
#df.loc[df['cache_misses'] < 1, 'cache_misses'] = 0
df['pruned_nodes'] = pd.to_numeric(df['pruned_nodes'], errors='coerce')
#df.loc[df['pruned_nodes'] < 1, 'pruned_nodes'] = 0


df.fillna(-1, inplace=True)

grouped = df.groupby(['file', 'max_depth', 'multithreading']).agg({
    'elapsed_time': 'mean',
    'terminal_calls': 'mean',
    'cache_hits': 'mean',
    'cache_misses': 'mean',
    'pruned_nodes': 'mean'
}).reset_index()

# grouped['elapsed_time'] = np.ceil(grouped['elapsed_time']).astype(int)
# grouped['terminal_calls'] = np.ceil(grouped['terminal_calls']).astype(int)
# grouped['cache_hits'] = np.ceil(grouped['cache_hits']).astype(int)
# grouped['cache_misses'] = np.ceil(grouped['cache_misses']).astype(int)
# grouped['pruned_nodes'] = np.ceil(grouped['pruned_nodes']).astype(int)

output_file_path = 'root_comparison_avg.csv'

grouped.to_csv(output_file_path, index=False)

print(f'Averaged statistics saved to {output_file_path}')
