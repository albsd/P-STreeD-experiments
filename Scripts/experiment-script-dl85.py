import subprocess
import time
import csv
import os
import sys

def get_next_available_filename(base_name, extension):
    counter = 1
    filename = f"{base_name}.{extension}"
    while os.path.isfile(filename):
        filename = f"{base_name}_{counter}.{extension}"
        counter += 1
    return filename

program_infos = [
    {
        "path": "pydl8.5/core/build",
        "program": "./dl85"
    },
]

# DL8.5 counts depth differently - we need to run experiments on depth - 1.
max_depth_num_nodes_combinations = [
    {"max-depth": "3"},
    {"max-depth": "4"},
]

data_files = [
    "../../../datasets/anneal.csv",
    "../../../datasets/audiology.csv",
    "../../../datasets/breast-wisconsin.csv",
    "../../../datasets/diabetes.csv",
    "../../../datasets/fico-binary.csv",
    "../../../datasets/german-credit.csv",
    "../../../datasets/heart-cleveland.csv",
    "../../../datasets/hepatitis.csv",
    "../../../datasets/ionosphere.csv",
    "../../../datasets/kr-vs-kp.csv",
    "../../../datasets/letter.csv",
    "../../../datasets/lymph.csv",
    "../../../datasets/mushroom.csv",
    "../../../datasets/pendigits.csv",
    "../../../datasets/splice-1.csv",
    "../../../datasets/tic-tac-toe.csv",
    "../../../datasets/vehicle.csv",
    "../../../datasets/yeast.csv"
]

timeout = 600

n = 10

base_csv_filename = "run_times_dl85_d4fixed"
csv_extension = "csv"

os.makedirs("results", exist_ok=True)

csv_file = os.path.join("results", get_next_available_filename(base_csv_filename, csv_extension))

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
                 data_file,
                combo["max-depth"],
                "-t", str(timeout)
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
                        "max_depth": str(int(combo["max-depth"]) + 1),
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

                print(f"Completed run {i + 1} for program {prog_info['program']} with file {data_file}, max_depth {combo['max-depth']}")

print(f"Results saved to {csv_file}")
