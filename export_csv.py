import csv

def export_csv(image_list, path):
    csv_columns = ["Kind", "Name", "Namespace", "Image", "Pods Name", "Containers Name"]
    try:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for kind, owners in image_list.items():
                for owner_name, details in owners.items():
                    namespace = details.get("Namespace", "Unknown")
                    images = details.get("images", [])
                    pods = details.get("pods", [])
                    for image in images:
                        for pod in pods:
                            writer.writerow([kind, owner_name, namespace, image, pod["Name"], pod["containers"]])
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        exit(1)

    return True