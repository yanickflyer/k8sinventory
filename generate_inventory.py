from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_pods():
    try:
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
        return pods.items
    except ApiException as e:
        print(f"Error fetching pods: {e}")
        return []
    
def get_cluster_name():
    try:
        cluster_info = config.list_kube_config_contexts()
        return cluster_info[1].get("name", "default_cluster_name")
    except Exception as e:
        print(f"Error fetching cluster name: {e}")
        return "default_cluster_name"
    
def get_pod_images(pod):
    """Extract container images from a pod."""
    images = []
    if pod.spec.containers:
        images.extend([c.image for c in pod.spec.containers])
    return images

def get_pod_containers(pod):
    """Extract container names from a pod."""
    containers = []
    if pod.spec.containers:
        containers.extend([(c.name, c.image) for c in pod.spec.containers])
    return containers

def get_pod_owners(pod):
    """
    Recursively traces the ownership chain to find the root controller.
    Returns the kind, name, and images of the initial controller, or the pod itself.
    """
    owner_references = getattr(pod.metadata, "owner_references", [])
    images = get_pod_images(pod)
    
    if not owner_references:
        return "Pod", pod.metadata.name, images
    
    controller_owner = next(
        (owner for owner in owner_references if owner.controller), 
        None
    )
    
    if not controller_owner:
        return "Pod", pod.metadata.name, images
    
    if controller_owner.kind == "ReplicaSet":
        try:
            v1 = client.AppsV1Api()
            rs = v1.read_namespaced_replica_set(
                controller_owner.name, 
                pod.metadata.namespace
            )
            rs_owner = next(
                (owner for owner in getattr(rs.metadata, "owner_references", []) 
                 if owner.controller), 
                None
            )
            if rs_owner:
                return rs_owner.kind, rs_owner.name, images
        except ApiException:
            pass
    
    return controller_owner.kind, controller_owner.name, images


try:
    config.load_kube_config()
    print("Kube config loaded successfully.")
except Exception as e:
    print(f"Error loading kube config: {e}")

def get_report(minimal=True):
    report = {}
    cluster_name = get_cluster_name()
    report['cluster_name'] = cluster_name
    pods = get_pods()
    load_report = []
    for pod in pods:
        owner_kind, owner_name, pod_images = get_pod_owners(pod)
        containers = get_pod_containers(pod)
        if not minimal:
            for container in containers:
                pod_entry = {
                    "kind": owner_kind,
                    "name": owner_name,
                    "namespace": getattr(pod.metadata, "namespace", None),
                    "Pod Name": getattr(pod.metadata, "name", None),
                    "images": container[1],
                    "container": container[0],
                }
                load_report.append(pod_entry)
        else:
            pod_entry = {
                "kind": owner_kind,
                "name": owner_name,
                "namespace": getattr(pod.metadata, "namespace", None),
                "images": pod_images,
            }
            load_report.append(pod_entry)

            # De-duplicate entries (preserve order)
            seen = set()
            unique = []
            for item in load_report:
                key = (
                    item.get("kind"),
                    item.get("name"),
                    item.get("namespace"),
                    tuple(item.get("images") or []),
                )
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            load_report = unique

    report['workloads'] = load_report
    return report