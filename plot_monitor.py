import matplotlib.pyplot as plt

def parse_log_file(filename):
    """Parse the log file to extract usage statistics."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    run_cpu_usage, run_gpu_usage, run_ram_usage = [], [], []
    current_cpu, current_gpu, current_ram = 0, 0, 0

    for line in lines:
        if line.startswith("Run"):
            if current_cpu or current_gpu or current_ram:
                run_cpu_usage.append(current_cpu)
                run_gpu_usage.append(current_gpu)
                run_ram_usage.append(current_ram)
                current_cpu = current_gpu = current_ram = 0
        elif line.strip() and not line.startswith("Process"):
            _, cpu, ram, gpu = line.split()
            current_cpu += float(cpu.strip('%'))
            current_ram += float(ram.strip('%'))
            current_gpu += float(gpu.strip('%'))

    if current_cpu or current_gpu or current_ram:
        run_cpu_usage.append(current_cpu)
        run_gpu_usage.append(current_gpu)
        run_ram_usage.append(current_ram)

    return run_cpu_usage, run_gpu_usage, run_ram_usage

def plot_and_save(data, title, ylabel, filename):
    """Plot and save the data."""
    plt.figure(figsize=(10, 6))
    plt.plot([i * 5 for i in range(len(data))], data, label=title, linewidth=2)
    plt.xlabel('Time (seconds)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    log_filename = 'process_monitoring_log.txt'
    cpu_usage, gpu_usage, ram_usage = parse_log_file(log_filename)

    # Plot and save each graph
    plot_and_save(cpu_usage, 'CPU Usage Over Time', 'CPU Usage (%)', 'cpu_usage.png')
    plot_and_save(gpu_usage, 'GPU Usage Over Time', 'GPU Usage (%)', 'gpu_usage.png')
    plot_and_save(ram_usage, 'RAM Usage Over Time', 'RAM Usage (%)', 'ram_usage.png')

    # Plot and save the combined graph
    plt.figure(figsize=(10, 6))
    plt.plot([i * 5 for i in range(len(cpu_usage))], cpu_usage, label='CPU Usage (%)', linewidth=2)
    plt.plot([i * 5 for i in range(len(gpu_usage))], gpu_usage, label='GPU Usage (%)', linewidth=2)
    plt.plot([i * 5 for i in range(len(ram_usage))], ram_usage, label='RAM Usage (%)', linewidth=2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Usage (%)')
    plt.title('Total Usage Over Time')
    plt.legend()
    plt.savefig('total_usage.png')
    plt.close()
