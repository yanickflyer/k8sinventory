import csv

def export_csv(image_dict, filename):
    if not image_dict:
        print("No image data to export.")
        return

    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['Cluster','Kind', 'Name', 'Namespace', 'Image', 'Pod Name', 'Container Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        
        for kind, resources in image_dict.items():
            if kind == 'cluster_name':
                continue
            
            for resource_name, resource_data in resources.items():
                namespace = resource_data.get('Namespace', '')
                cluster_name = image_dict.get('cluster_name', 'default_cluster_name')
                images = resource_data.get('images', [])
                pods = resource_data.get('pods', [])
                
                for image in images:
                    for pod in pods:
                        writer.writerow({
                            'Cluster': cluster_name,
                            'Kind': kind,
                            'Name': resource_name,
                            'Namespace': namespace,
                            'Image': image,
                            'Pod Name': pod.get('Name', ''),
                            'Container Name': pod.get('containers', '')
                        })

def export_csv(image_dict, filename, minimal=True):
    if not minimal:
        return None
    if not image_dict:
        print("No image data to export.")
        return

    with open(f"{filename}.csv", mode='w', newline='') as csv_file:
        fieldnames = ['Cluster','Kind', 'Name', 'Namespace', 'Image']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        
        cluster_name = image_dict.get('cluster_name', 'default_cluster_name')
        workloads = image_dict.get('workloads', {})
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