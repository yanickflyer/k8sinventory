import csv
import inventory
from rich.progress import Progress

def export_csv(**kwargs):
    filepath = kwargs.get('filepath', None)
    report = kwargs.get('full_report', [])
    full = kwargs.get('full', False)
    cluster_name = inventory.get_cluster_name()
    filename = f"{cluster_name}_workload_report.csv" if not filepath else f"{filepath}/{cluster_name}_workload_report.csv"
    print(f"Exporting report to {filename}...")
    p = Progress()
    p.start()
    try:
        with open(filename, mode='w', newline='') as csv_file:
            if not full:
                fieldnames = ['Namespace', 'Kind', 'Name', 'Images']
            else:
                fieldnames = ['namespace', 'owner_kind', 'owner_name', 'pod_name', 'container', 'image']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            report_length = len(report)
            task = p.add_task("Writing to CSV...", total=report_length)
            for item in report:
                p.update(task, advance=1)
                if not full:
                    for image in item.get('images', []):    
                        writer.writerow({
                            'Namespace': item.get('namespace', 'Unknown'),
                            'Kind': item.get('kind', 'Unknown'),
                            'Name': item.get('name', 'Unknown'),
                            'Images': image
                        })
                else:
                    writer.writerow({
                        'namespace': item.get('namespace', 'Unknown'),
                        'owner_kind': item.get('owner_kind', 'Unknown'),
                        'owner_name': item.get('owner_name', 'Unknown'),
                        'pod_name': item.get('pod_name', 'Unknown'),
                        'container': item.get('container', 'Unknown'),
                        'image': item.get('image', 'Unknown')
                    })
        p.stop()
    except Exception as e:
        RED = '\033[31m'
        RESET = '\033[0m'
        print(f"{RED}Error exporting CSV: {e}{RESET}")
        p.stop()
        return
    print("Export completed.")