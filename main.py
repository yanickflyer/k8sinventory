import generate_inventory
from export_csv import export_csv
import json
import sys


# Check if user specified --out csv
if "--full" in sys.argv:
    final_report = generate_inventory.get_report(minimal=False)
    cluster_name = final_report['cluster_name'] if final_report else 'default_cluster_name'
    print(json.dumps(final_report))
    export_csv(final_report, cluster_name, minimal=False)
elif "--minimal" in sys.argv:
    final_report = generate_inventory.get_report()
    cluster_name = final_report['cluster_name'] if final_report else 'default_cluster_name'
    print(json.dumps(final_report))
    export_csv(final_report, cluster_name, minimal=True)