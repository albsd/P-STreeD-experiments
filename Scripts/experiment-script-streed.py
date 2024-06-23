import subprocess
import time
import csv
import os
import sys

def get_next_available_filename(base_name, extension):
    counter = 0
    while True:
        filename = f"{base_name}{('-' + str(counter)) if counter > 0 else ''}.{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

program_infos = [
    {
        "path": "pystreed-master/build",
        "program": "./STreeD"
    },
]

max_depth_num_nodes_combinations = [
    # {"max_depth": "4", "max_num_nodes": "15"},
    # {"max_depth": "5", "max_num_nodes": "24"},
    {"max_depth": "5", "max_num_nodes": "31"},
]

# Define files
data_files = [
    "../data/accuracy/anneal.csv",
    "../data/accuracy/audiology.csv",
    "../data/accuracy/breast-wisconsin.csv",
    "../data/accuracy/diabetes.csv",
    "../data/accuracy/fico-binary.csv",
    "../data/accuracy/german-credit.csv",
    "../data/accuracy/heart-cleveland.csv",
    "../data/accuracy/hepatitis.csv",
    "../data/accuracy/ionosphere.csv",
    "../data/accuracy/kr-vs-kp.csv",
    "../data/accuracy/letter.csv",
    "../data/accuracy/lymph.csv",
    "../data/accuracy/mushroom.csv",
    "../data/accuracy/pendigits.csv",
    "../data/accuracy/splice-1.csv",
    "../data/accuracy/tic-tac-toe.csv",
    "../data/accuracy/vehicle.csv",
    "../data/accuracy/yeast.csv"
]

timeout = 600

n = 10

base_csv_filename = "run_times_streed_d5n31"
csv_extension = "csv"

csv_file = get_next_available_filename(base_csv_filename, csv_extension)

with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "run", "path", "program", "task", "file", "max_depth", "max_num_nodes", "status", "elapsed_time", "output"
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
                "-use-dataset-caching", "1",
                "-use-branch-caching", "0",
                "-time", str(timeout)
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
                
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        "run", "path", "program", "task", "file", "max_depth", "max_num_nodes", "status", "elapsed_time", "output"
                    ])
                    writer.writerow({
                        "run": i + 1,
                        "path": prog_info["path"],
                        "program": prog_info["program"],
                        "task": "accuracy",
                        "file": data_file,
                        "max_depth": combo["max_depth"],
                        "max_num_nodes": combo["max_num_nodes"],
                        "status": status,
                        "elapsed_time": elapsed_time,
                        "output": output
                    })
                
                if result.returncode != 0:
                    print(f"Error encountered!\n{output}")
                    sys.exit(1)

                if status == "Failed":
                    break

                if elapsed_time > 598.0:
                    break

                print(f"Completed run {i + 1} for program {prog_info['program']} with file {data_file}, max_depth {combo['max_depth']}, max_num_nodes {combo['max_num_nodes']}")

print(f"Results saved to {csv_file}")
