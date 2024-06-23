import pandas as pd

file_path = 'average_arithmetic_runtimes_d5n31.csv'  
df = pd.read_csv(file_path)

def rank_programs(group):
    group['rank'] = group['elapsed_time'].rank(method='min')
    return group

df = df.groupby('file').apply(rank_programs)

avg_ranks = df.groupby('path')['rank'].mean().sort_values()

print("Average ranks:")
print(avg_ranks)