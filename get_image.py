from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_pod_owners(pod):
    owner_refs = getattr(pod.metadata, "owner_references", None)
    if not owner_refs:
        return ("Pod", getattr(pod.metadata, "name", None))
    try:
        primary = owner_refs[0]
        kind = getattr(primary, "kind", None) or "Unknown"
        owner_name = getattr(primary, "name", None)
        if kind == "ReplicaSet":
            rs_name = owner_name
            ns = getattr(pod.metadata, "namespace", None)
            if rs_name and ns:
                try:
                    apps_v1 = client.AppsV1Api()
                    rs = apps_v1.read_namespaced_replica_set(rs_name, ns)
                    rs_owner_refs = getattr(rs.metadata, "owner_references", None)
                    if rs_owner_refs and getattr(rs_owner_refs[0], "kind", None) == "Deployment":
                        deployment_name = getattr(rs_owner_refs[0], "name", None)
                        return ("Deployment", deployment_name or "Unknown")
                except ApiException as e:
                    print(f"Error fetching ReplicaSet {rs_name} in {ns}: {e}")
            return ("ReplicaSet", rs_name)
        return (kind, owner_name)
    except Exception as e:
        print(f"Error determining owners for pod {getattr(pod.metadata, 'name', '<unknown>')}: {e}")
        return ("Unknown", None)

def _load_kube_config_safe():
    try:
        config.load_kube_config()
        print("Kube config loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading kube config: {e}")
        return False

def _collect_containers(pod):
    containers = []
    if getattr(pod.spec, "containers", None):
        containers.extend(pod.spec.containers)
    if getattr(pod.spec, "init_containers", None):
        containers.extend(pod.spec.init_containers)
    return containers

def _ensure_owner_maps(grouped, owner_kind, owner_name, ns):
    kind_map = grouped.setdefault(owner_kind, {})
    owner_map = kind_map.setdefault(owner_name, {})
    owner_map.setdefault("Namespace", ns)
    images_list = owner_map.setdefault("images", [])
    pods_list = owner_map.setdefault("pods", [])
    return images_list, pods_list

def _process_container(container, pod, images_list, pods_list):
    image = getattr(container, "image", None) or "Unknown"
    container_name = getattr(container, "name", None) or "unknown"
    if image not in images_list:
        images_list.append(image)
    pod_entry = {"Name": pod.metadata.name, "containers": container_name}
    if pod_entry not in pods_list:
        pods_list.append(pod_entry)

def get_aks_image():
    if not _load_kube_config_safe():
        return None

    try:
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)

        # Get cluster name using Kubernetes API
        cluster_info = config.list_kube_config_contexts()
        cluster_name = cluster_info[1].get("name", "default_cluster_name")

        # Structure: { "cluster_name": "<cluster_name>", <kind>: { <Name>: { Namespace: <ns>, images: [...], pods: [...] } } }
        grouped = {"cluster_name": cluster_name}

        
        for pod in pods.items:
            owner_kind, owner_name = get_pod_owners(pod)
            owner_name = owner_name or "Unknown"
            ns = getattr(pod.metadata, "namespace", None)

            images_list, pods_list = _ensure_owner_maps(grouped, owner_kind, owner_name, ns)

            for container in _collect_containers(pod):
                _process_container(container, pod, images_list, pods_list)

        return grouped
    except ApiException as e:
        print(f"Exception when calling CoreV1Api->list_pod_for_all_namespaces: {e}")
        return None