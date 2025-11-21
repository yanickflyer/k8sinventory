import csv
import inventory
from rich.progress import Progress

def export_csv(report,filepath):
    cluster_name = inventory.get_cluster_name()
    filename = f"{cluster_name}_workload_report.csv" if not filepath else f"{filepath}/{cluster_name}_workload_report.csv"
    print(f"Exporting report to {filename}...")
    p = Progress()
    p.start()
    try:
        with open(filename, mode='w', newline='') as csv_file:
            fieldnames = ['Namespace', 'Kind', 'Name', 'Images']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            report_length = len(report)
            task = p.add_task("Writing to CSV...", total=report_length)
            for item in report:
                p.update(task, advance=1)
                for image in item.get('images', []):    
                    writer.writerow({
                        'Namespace': item.get('namespace', 'Unknown'),
                        'Kind': item.get('kind', 'Unknown'),
                        'Name': item.get('name', 'Unknown'),
                        'Images': image
                        # 'Images': ', '.join(item.get('images', []))
                    })
        p.stop()
    except Exception as e:
        RED = '\033[31m'
        RESET = '\033[0m'
        print(f"{RED}Error exporting CSV: {e}{RESET}")
        p.stop()
        return
    print("Export completed.")