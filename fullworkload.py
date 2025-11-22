import owner
from rich.progress import Progress
from inventory import get_pods
from csvexport import export_csv

def get_report(filepath):
    with Progress() as p:
        p.start()
        task1 = p.add_task("Retrieving Pods...", total=1000)
        p.update(task1, advance=500)
        pods = get_pods(True)
        p.update(task1, advance=500)
        pod_count = len(pods)
        pod_list = []
        task2 = p.add_task("Retrieving Containers, Images and main Pod owner...", total=pod_count)
        for pod in pods:
            owner_references = get_mainowner(pod)
            for container in pod.spec.containers:
                pod_entry = {
                    "namespace": pod.metadata.namespace,
                    "owner_kind": owner_references[0] if owner_references else None,
                    "owner_name": owner_references[1] if owner_references else None,
                    "pod_name": pod.metadata.name,
                    "container": container.name,
                    "image": container.image,
                }
                pod_list.append(pod_entry)
            # Process each pod here if needed
            p.update(task2, advance=1)
        p.stop()
        export_csv(full = True, filepath=filepath, full_report=pod_list)
    return pod_list

def get_mainowner(pod):
    owner_references = getattr(pod.metadata, "owner_references", [])
    owner_references = owner_references[0] if owner_references else None
    if not owner_references:
        return None
    elif owner_references:
        if owner_references.kind == "ReplicaSet":
            name = owner_references.name if hasattr(owner_references, 'name') else None
            main_owner = owner.get_replica_set_owner(name, pod.metadata.namespace)
            return main_owner
        elif owner_references.kind == "Job":
            name = owner_references.name if hasattr(owner_references, 'name') else None
            main_owner = owner.get_job_owner(name, pod.metadata.namespace)
            return main_owner
    return owner_references.name, owner_references.kind