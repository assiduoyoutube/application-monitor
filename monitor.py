import psutil
import time
import GPUtil

application = "brave.exe"

how_many_runs = 10

# Define the list of applications you want to monitor
applications_to_monitor = [application]

def get_process_info(filename):
    global how_many_runs
    """Continuously gets hardware usage information for specified applications and saves it to a file."""
    run_number = 1

    while run_number <= how_many_runs:
        with open(filename, 'w' if run_number == 1 else 'a') as file:
            file.write(f"Run #{run_number}\n")
            file.write("Process CPU_Usage RAM_Usage GPU_Usage\n")

            # First call to cpu_percent to start measuring
            for process in psutil.process_iter():
                process.cpu_percent()

            # Sleep for a longer period to average CPU usage (e.g., 5 seconds)
            time.sleep(5)

            num_cores = psutil.cpu_count()

            # Get GPU usage
            gpus = GPUtil.getGPUs()
            gpu_usage = gpus[0].load * 100 if gpus else 0  # Assuming a single GPU

            for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                if process.info['name'] in applications_to_monitor:
                    # Normalize CPU usage to total CPU power
                    normalized_cpu_usage = process.info['cpu_percent'] / num_cores
                    file.write(f"{process.info['name']} {normalized_cpu_usage:.2f}% {process.info['memory_percent']:.2f}% {gpu_usage:.2f}%\n")

            run_number += 1

if __name__ == "__main__":
    output_filename = 'process_monitoring_log.txt'
    get_process_info(output_filename)
