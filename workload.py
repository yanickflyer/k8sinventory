import inventory, csv
from rich.progress import Progress
from csvexport import export_csv

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
            full_report = inventory.get_deployments()
            p.update(task1, advance=1000)
            full_report.extend(inventory.get_statefulsets())
            p.update(task2, advance=1000)
            full_report.extend(inventory.get_daemonsets())
            p.update(task3, advance=1000)
            full_report.extend(inventory.get_jobs())
            p.update(task4, advance=1000)
            full_report.extend(inventory.get_cronjobs())
            p.update(task5, advance=1000)
            full_report.extend(inventory.get_pods())
            p.update(task6, advance=1000)
            p.stop()
    export_csv(full_report,filepath)
    return
