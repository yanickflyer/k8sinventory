import workloads, csv
from rich.progress import Progress

def get_report(filepath):
    with Progress() as p:
        p.start()
        task1 = p.add_task("Retrieving Deployments...", total=1000)
        task2 = p.add_task("Retrieving StatefulSets...", total=1000)
        task3 = p.add_task("Retrieving DaemonSets...", total=1000)
        task4 = p.add_task("Retrieving CronJobs...", total=1000)
        task5 = p.add_task("Retrieving Jobs...", total=1000)
        task6 = p.add_task("Retrieving Pods...", total=1000)
        full_report = []
        while not p.finished:
            print("Generating Report")
            full_report = workloads.get_deployments()
            p.update(task1, advance=1000)
            full_report.extend(workloads.get_statefulsets())
            p.update(task2, advance=1000)
            full_report.extend(workloads.get_daemonsets())
            p.update(task3, advance=1000)
            full_report.extend(workloads.get_jobs())
            p.update(task4, advance=1000)
            full_report.extend(workloads.get_cronjobs())
            p.update(task5, advance=1000)
            full_report.extend(workloads.get_pods())
            p.update(task6, advance=1000)
            p.stop()
    export_csv(full_report,filepath)
    return
    
def export_csv(report,filepath):
    cluster_name = workloads.get_cluster_name()
    filename = f"{cluster_name}_workload_report.csv" if not filepath else f"{filepath}/{cluster_name}_workload_report.csv"
    print(f"Exporting report to {filename}...")
    try:
        with open(filename, mode='w', newline='') as csv_file:
            fieldnames = ['Namespace', 'Kind', 'Name', 'Images']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in report:
                for image in item.get('images', []):    
                    writer.writerow({
                        'Namespace': item.get('namespace', 'Unknown'),
                        'Kind': item.get('kind', 'Unknown'),
                        'Name': item.get('name', 'Unknown'),
                        'Images': image
                        # 'Images': ', '.join(item.get('images', []))
                    })
    except Exception as e:
        RED = '\033[31m'
        RESET = '\033[0m'
        print(f"{RED}Error exporting CSV: {e}{RESET}")
        return
    print("Export completed.")
