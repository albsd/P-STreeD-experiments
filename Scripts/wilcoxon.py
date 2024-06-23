import pandas as pd
from scipy.stats import wilcoxon

def clean_filename(filename):
    return (filename.replace('.csv', '')
                    .replace('murtree/LinuxRelease', 'Murtree')
                    .replace('pydl8.5/core/build', 'DL8.5')
                    .replace('pystreed/build', 'P-STreeD')
                    .replace('pystreed-master/build', 'STreeD')
                    .replace('../datasets', '')
                    .replace('../../datasets/', '')
                    .replace('../../../datasets/', '')
                    .replace('../../../../datasets/', '')
                    .replace('../data/accuracy/', '')
                    .replace('..//', ''))

def perform_wilcoxon_test(data1, data2, competitor):
    common_files = data1.index.intersection(data2.index)
    
    data1_means = data1.loc[common_files]['elapsed_time']
    data2_means = data2.loc[common_files]['elapsed_time']
    
    differences = data1_means - data2_means
    
    stat, p_value = wilcoxon(data1_means, data2_means)
    
    if differences.median() > 0:
        faster_algorithm = competitor
    else:
        faster_algorithm = 'P-STreeD'
    
    return stat, p_value, differences.median(), faster_algorithm

files = [
    {'label': 'd4n15', 'path': 'average_arithmetic_runtimes_final_final.csv', 'max_depth': 4},
    {'label': 'd5n24', 'path': 'average_arithmetic_runtimes_final_final.csv', 'max_depth': 5},
    {'label': 'd5n31', 'path': 'average_arithmetic_runtimes_d5n31.csv'}
]

results_pstreed_vs_murtree = []
results_pstreed_vs_streed = []

for file_info in files:
    file_label = file_info['label']
    file_path = file_info['path']
    
    df = pd.read_csv(file_path)
    
    df['file'] = df['file'].apply(clean_filename)
    df['path'] = df['path'].apply(clean_filename)
    
    if 'max_depth' in file_info:
        max_depth_value = file_info['max_depth']
        df = df[df['max_depth'] == max_depth_value]
    
    murtree_data = df[df['path'] == 'Murtree'].set_index('file')
    pstreed_data = df[df['path'] == 'P-STreeD'].set_index('file')
    streed_data = df[df['path'] == 'STreeD'].set_index('file')
    
    try:
        stat1, p_value1, median_diff1, faster_algorithm1 = perform_wilcoxon_test(pstreed_data, murtree_data, 'Murtree')
        
        stat2, p_value2, median_diff2, faster_algorithm2 = perform_wilcoxon_test(pstreed_data, streed_data, 'STreeD')
        
        results_pstreed_vs_murtree.append((file_label, stat1, p_value1, median_diff1, faster_algorithm1))
        results_pstreed_vs_streed.append((file_label, stat2, p_value2, median_diff2, faster_algorithm2))
        
        print(f'Results for {file_label} - P-STreeD vs Murtree:')
        print(f'Wilcoxon signed-rank test statistic: {stat1}')
        print(f'p-value: {p_value1}')
        print(f'Median difference: {median_diff1}')
        print(f'Faster Algorithm: {faster_algorithm1}')
        print()
        
        print(f'Results for {file_label} - P-STreeD vs STreeD:')
        print(f'Wilcoxon signed-rank test statistic: {stat2}')
        print(f'p-value: {p_value2}')
        print(f'Median difference: {median_diff2}')
        print(f'Faster Algorithm: {faster_algorithm2}')
        print()
    
    except ValueError as ve:
        print(f"Error processing {file_label}: {ve}")
        print()

output_file = 'wilcoxon_results.txt'

with open(output_file, 'w') as f:
    f.write('Results of Wilcoxon Signed-Rank Test\n\n')
    
    f.write('P-STreeD vs Murtree:\n')
    for result in results_pstreed_vs_murtree:
        f.write(f'{result[0]}: Stat={result[1]}, p-value={result[2]}, Median Difference={result[3]}, Faster Algorithm={result[4]}\n')
    f.write('\n')
    
    f.write('P-STreeD vs STreeD:\n')
    for result in results_pstreed_vs_streed:
        f.write(f'{result[0]}: Stat={result[1]}, p-value={result[2]}, Median Difference={result[3]}, Faster Algorithm={result[4]}\n')
    f.write('\n')

latex_table_file = 'wilcoxon_results_table.tex'

with open(latex_table_file, 'w') as f:
    f.write("""
\\begin{table}[H]
\\centering
\\caption{Wilcoxon Signed-Rank Test results for depths $d = \\{4, 5\\}$. Each entry includes the W-Statistic, the p-value in parentheses, the median difference, and the faster algorithm.}
\\label{wilcoxon}
\\begin{tabular}{|c|c|c|c|c|c|}
\\hline
$depth$ & $n$ & Comparison & W-Statistic & p-value & Median Difference & Faster Algorithm \\\\
\\hline
""")
    
    for result_murtree, result_streed in zip(results_pstreed_vs_murtree, results_pstreed_vs_streed):
        f.write(f"{result_murtree[0]} & {result_murtree[0][3:]} & P-STreeD vs Murtree & {result_murtree[1]} & {result_murtree[2]:.4f} & {result_murtree[3]:.4f} & {result_murtree[4]} \\\\\n")
        f.write(f"{result_streed[0]} & {result_streed[0][3:]} & P-STreeD vs STreeD & {result_streed[1]} & {result_streed[2]:.4f} & {result_streed[3]:.4f} & {result_streed[4]} \\\\\n")
        
    f.write("""
\\hline
\\end{tabular}
\\end{table}
""")

print(f"Results saved to {output_file}")
print(f"LaTeX table saved to {latex_table_file}")
