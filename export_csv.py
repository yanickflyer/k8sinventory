import csv

def export_csv(image_dict, filename, minimal=True):
    if not image_dict:
        print("No image data to export.")
        return

    with open(f"{filename}.csv", mode='w', newline='') as csv_file:
        if minimal:
            fieldnames = ['Cluster','Kind', 'Name', 'Namespace', 'Image']
        else:
            fieldnames = ['Cluster','Kind', 'Name', 'Namespace', 'Image', 'Container Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        
        cluster_name = image_dict.get('cluster_name', 'default_cluster_name')
        workloads = image_dict.get('workloads', {})
        if minimal:
            for workload in workloads:
                namespace = workload.get('namespace', 'Unknown')
                kind = workload.get('kind', 'Unknown')
                name = workload.get('name', 'Unknown')
                images = workload.get('images', [])
                for image in images:
                    writer.writerow({
                        'Cluster': cluster_name,
                        'Namespace': namespace,
                        'Kind': kind,
                        'Name': name,
                        'Image': image
                    })
        else:
            for workload in workloads:
                namespace = workload.get('namespace', 'Unknown')
                kind = workload.get('kind', 'Unknown')
                name = workload.get('name', 'Unknown')
                image = workload.get('images', 'Unknown')
                container = workload.get('container', 'Unknown')
                writer.writerow({
                    'Cluster': cluster_name,
                    'Namespace': namespace,
                    'Kind': kind,
                    'Name': name,
                    'Image': image,
                    'Container Name': container
                })