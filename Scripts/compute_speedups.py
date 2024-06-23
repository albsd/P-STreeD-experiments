import pandas as pd
import numpy as np

def compute_speedups(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    baseline_df = df[df['num_threads'] == 1][['file', 'max_depth', 'max_num_nodes', 'elapsed_time_arith_mean']]
    baseline_df = baseline_df.rename(columns={'elapsed_time_arith_mean': 'baseline_arith_mean'})
    
    merged_df = pd.merge(df, baseline_df, on=['file', 'max_depth', 'max_num_nodes'])
    
    merged_df['speedup_arith_mean'] = merged_df['baseline_arith_mean'] / merged_df['elapsed_time_arith_mean']
    
    speedup_df = merged_df[merged_df['num_threads'].isin([2, 3, 4])]
    
    speedup_df = speedup_df[['file', 'num_threads', 'max_depth', 'max_num_nodes', 'speedup_arith_mean']]
    
    speedup_df.to_csv(output_csv, index=False)

input_csv = 'speed_up_threads_averages.csv'
output_csv = 'speedup_results_threads.csv'
compute_speedups(input_csv, output_csv)
