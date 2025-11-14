import generate_inventory
from get_image import get_aks_image
from export_csv import export_csv
import json
import sys


# Check if user specified --out csv
if "--full" in sys.argv and "csv" in sys.argv:
    image_dict = get_aks_image()
    cluster_name = image_dict['cluster_name'] if image_dict else 'default_cluster_name'
    filename = f"{cluster_name}.csv"
    export_csv(image_dict, filename)  # Replace 'additional_argument' with the actual value needed
elif "--minimal" in sys.argv:
    final_report = generate_inventory.get_report_minimal()
    cluster_name = final_report['cluster_name'] if final_report else 'default_cluster_name'
    print(json.dumps(final_report))
    export_csv(final_report, cluster_name, minimal=True)

# print(json.dumps(image_dict))