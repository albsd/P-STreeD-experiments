import pandas as pd

input_files = [
    # enter files with runtimes here
    
    # 'run_times_murtree.csv',
    # 'run_times_streed.csv',
    # 'run_times_pstreed.csv',
    # 'run_times_dl85.csv'
]

dfs = []

for file in input_files:
    df = pd.read_csv(file)
    df['max_num_nodes'].fillna(0, inplace=True)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

average_runtimes = combined_df.groupby(['path', 'max_depth', 'max_num_nodes', 'file'])['elapsed_time'].mean().reset_index()

average_runtimes['elapsed_time'].fillna(-1, inplace=True)


output_file = 'example_output.csv'
average_runtimes.to_csv(output_file, index=False)

print("Average arithmetic runtimes computed!")
