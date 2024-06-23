import subprocess
import time
import csv
import os
import sys
import re

def get_next_available_filename(base_name, extension):
    counter = 0
    while True:
        filename = f"{base_name}{('-' + str(counter)) if counter > 0 else ''}.{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

def extract_statistics(output):
    stats = {
        "terminal_calls": None,
        "cache_hits": None,
        "cache_misses": None,
        "pruned_nodes": None
    }

    terminal_calls_match = re.search(r'Terminal calls:\s+(\d+)', output)
    if terminal_calls_match:
        stats["terminal_calls"] = int(terminal_calls_match.group(1))
    
    cache_hits_match = re.search(r'Cache optimal solution hits:\s+(\d+)', output)
    if cache_hits_match:
        stats["cache_hits"] = int(cache_hits_match.group(1))

    cache_misses_match = re.search(r'Cache optimal solution misses:\s+(\d+)', output)
    if cache_misses_match:
        stats["cache_misses"] = int(cache_misses_match.group(1))
    
    pruned_nodes_match = re.search(r'Pruned nodes:\s+(\d+)', output)
    if pruned_nodes_match:
        stats["pruned_nodes"] = int(pruned_nodes_match.group(1))
    
    return stats

program_infos = [
    {
        "path": "pystreed/build",
        "program": "./STreeD"
    },
]

max_depth_num_nodes_combinations = [
    # #{"max_depth": "4", "max_num_nodes": "15", "multithreading":"root"},
    {"max_depth": "5", "max_num_nodes": "31", "multithreading":"root", "num_threads": "4"},
    {"max_depth": "5", "max_num_nodes": "31", "multithreading":"none", "num_threads": "1"},
    # #{"max_depth": "4", "max_num_nodes": "15", "multithreading":"leaf"},
    # {"max_depth": "5", "max_num_nodes": "31", "multithreading":"leaf"},
    # {"max_depth": "5", "max_num_nodes": "31", "multithreading":"none"}

    # {"max_depth": "4", "max_num_nodes": "15", "multithreading":"none", "num_threads": "1"},
    # {"max_depth": "4", "max_num_nodes": "15", "multithreading":"root", "num_threads": "2"},
    # {"max_depth": "4", "max_num_nodes": "15", "multithreading":"root", "num_threads": "3"},
    # {"max_depth": "4", "max_num_nodes": "15", "multithreading":"root", "num_threads": "4"},

    # {"max_depth": "5", "max_num_nodes": "24", "multithreading":"none", "num_threads": "1"},
    # {"max_depth": "5", "max_num_nodes": "24", "multithreading":"root", "num_threads": "2"},
    # {"max_depth": "5", "max_num_nodes": "24", "multithreading":"root", "num_threads": "3"},
    # {"max_depth": "5", "max_num_nodes": "24", "multithreading":"root", "num_threads": "4"},
]

data_files = [

    #"../data/accuracy/anneal.csv",
    #"../data/accuracy/audiology.csv",
    #"../data/accuracy/breast-wisconsin.csv",
    # "../data/accuracy/diabetes.csv",
    # "../data/accuracy/fico-binary.csv",
    # "../data/accuracy/german-credit.csv",
    #"../data/accuracy/heart-cleveland.csv",
    #"../data/accuracy/hepatitis.csv",
    # "../data/accuracy/ionosphere.csv",
    #"../data/accuracy/kr-vs-kp.csv",
    # "../data/accuracy/letter.csv",
    #"../data/accuracy/lymph.csv",
    #"../data/accuracy/mushroom.csv",
    "../data/accuracy/pendigits.csv",
    #"../data/accuracy/splice-1.csv",
    #"../data/accuracy/tic-tac-toe.csv",
    #"../data/accuracy/vehicle.csv",
    #"../data/accuracy/yeast.csv"
]
timeout = 600

n = 10

base_csv_filename = "toy_script_test"
csv_extension = "csv"

csv_file = get_next_available_filename(base_csv_filename, csv_extension)

with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "run", "path", "program", "multithreading", "num_threads", "file", "max_depth", "max_num_nodes", 
        "status", "elapsed_time", "output", "terminal_calls", 
        "cache_hits", "cache_misses", "pruned_nodes"
    ])
    writer.writeheader()

for prog_info in program_infos:
    for data_file in data_files:
        for combo in max_depth_num_nodes_combinations:
            command = [
                prog_info['program'],
                "-task", "accuracy",
                "-file", data_file,
                "-max-depth", combo["max_depth"],
                "-max-num-nodes", combo["max_num_nodes"],
                "-use-branch-caching", "0",
                "-use-dataset-caching", "1",
                "-time", str(timeout),
                "-multithreading", combo["multithreading"],
                "-num-threads", combo["num_threads"],
            ]
            
            for i in range(n):
                start_time = time.time()
                
                result = subprocess.run(command, capture_output=True, text=True, cwd=prog_info["path"])
                
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                
                if result.returncode == 0:
                    status = "Success"
                    output = result.stdout.strip()
                else:
                    status = "Failed"
                    output = result.stderr.strip()
                
                if elapsed_time > 598.0:
                    status = "Timed out"
                    output = result.stdout.strip()

                stats = extract_statistics(output)

                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        "run", "path", "program", "multithreading", "num_threads", "file", "max_depth", "max_num_nodes", 
                        "status", "elapsed_time", "output", "terminal_calls", 
                        "cache_hits", "cache_misses", "pruned_nodes"
                    ])
                    writer.writerow({
                        "run": i + 1,
                        "path": prog_info["path"],
                        "program": prog_info["program"],
                        "multithreading": combo["multithreading"],
                        "num_threads": combo["num_threads"],
                        "file": data_file,
                        "max_depth": combo["max_depth"],
                        "max_num_nodes": combo["max_num_nodes"],
                        "status": status,
                        "elapsed_time": elapsed_time,
                        "output": output,
                        "terminal_calls": stats["terminal_calls"],
                        "cache_hits": stats["cache_hits"],
                        "cache_misses": stats["cache_misses"],
                        "pruned_nodes": stats["pruned_nodes"]
                    })
                
                if result.returncode != 0:
                    print(f"Error encountered!\n{output}")

                if status == "Failed":
                    break

                if elapsed_time > 598.0:
                    break

                print(f"Finished run {i + 1} for {combo['multithreading']} with {combo['num_threads']} - file {data_file}, max_depth {combo['max_depth']}, max_num_nodes {combo['max_num_nodes']}, elapsed_time {elapsed_time}")

print(f"Results saved to {csv_file}")