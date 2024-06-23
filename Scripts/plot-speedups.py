import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_speedups(input_csv, output_plot_base):
    try:
        df = pd.read_csv(input_csv, delimiter=',')
        
        df.columns = df.columns.str.strip()
        
        print("Columns loaded from CSV:", df.columns)
        
        required_columns = {'file', 'num_threads', 'max_depth', 'max_num_nodes', 'speedup_arith_mean'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Input CSV must contain the columns: {required_columns}")

        df_max_depth_4 = df[df['max_depth'] == 4]
        
        df_max_depth_5 = df[df['max_depth'] == 5]

        sns.set(style="whitegrid")

        fig, axes = plt.subplots(1, 2, figsize=(36, 18), sharey=True)

        sns.lineplot(ax=axes[0], data=df_max_depth_4, x='num_threads', y='speedup_arith_mean', hue='file', marker='o')
        axes[0].set_title('d = 4, n = 15', fontsize=34)
        axes[0].set_xlabel('Number of Threads', fontsize=34)
        axes[0].set_ylabel('Speed-up', fontsize=34)
        axes[0].tick_params(axis='both', which='major', labelsize=30)
        axes[0].set_xticks(df_max_depth_4['num_threads'].unique()) 
        axes[1].set_xticks(df_max_depth_5['num_threads'].unique())


        sns.lineplot(ax=axes[1], data=df_max_depth_5, x='num_threads', y='speedup_arith_mean', hue='file', marker='o')
        axes[1].set_title('d = 5, n = 24', fontsize=34)
        axes[1].set_xlabel('Number of Threads', fontsize=34)
        axes[1].tick_params(axis='both', which='major', labelsize=30)

        handles, labels = axes[1].get_legend_handles_labels()
        fig.legend(handles, labels, title='Dataset', loc='upper right', fontsize=28, title_fontsize=30)
        axes[0].get_legend().remove()
        axes[1].get_legend().remove()

        plt.tight_layout(rect=[0, 0, 0.875, 1])

        plt.savefig(f"{output_plot_base}_combined.png", bbox_inches='tight')

        plt.show()
    
    except Exception as e:
        print(f"Error processing {input_csv}: {e}")


input_csv = 'speedup_results_threads.csv'
output_plot = 'speed-up_plot'
plot_speedups(input_csv, output_plot)
