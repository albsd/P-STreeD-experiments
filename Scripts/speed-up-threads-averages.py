import pandas as pd
import numpy as np
from scipy.stats import gmean
import os

def calculate_means(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    df['file'] = df['file'].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
    
    grouped = df.groupby(['file', 'multithreading', 'num_threads', 'max_depth', 'max_num_nodes'])

    def custom_agg(x):
        elapsed_time_arith_mean = np.mean(x['elapsed_time'])
        elapsed_time_geom_mean = gmean(x['elapsed_time'])
        
        # elapsed_time_arith_mean = "<1" if elapsed_time_arith_mean < 1 else round(elapsed_time_arith_mean)
        # elapsed_time_geom_mean = "<1" if elapsed_time_geom_mean < 1 else round(elapsed_time_geom_mean)
        
        return pd.Series({
            'elapsed_time_arith_mean': elapsed_time_arith_mean,
            'elapsed_time_geom_mean': elapsed_time_geom_mean,
            'terminal_calls_arith_mean': round(np.mean(x['terminal_calls'])),
            'terminal_calls_geom_mean': round(gmean(x['terminal_calls'])),
            'cache_hits_arith_mean': round(np.mean(x['cache_hits'])),
            'cache_hits_geom_mean': round(gmean(x['cache_hits'])),
            'cache_misses_arith_mean': round(np.mean(x['cache_misses'])),
            'cache_misses_geom_mean': round(gmean(x['cache_misses']))
        })

    results = grouped.apply(custom_agg).reset_index()

    results.to_csv(output_csv, index=False)

input_csv = 'run_times_pstreed_comparisons_numthreads.csv'
output_csv = 'speed-up_threads_averages.csv'
calculate_means(input_csv, output_csv)
