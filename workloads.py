from kubernetes import client, config
from kubernetes.client.rest import ApiException


try:
    config.load_kube_config()
except Exception as e:
    print(f"Error loading kube config: {e}")

def make_list(workload, kind):
    workload_list = []
    for workload in workload:
        if workload.metadata.owner_references:
            continue
        workload_list.append({
            "namespace": workload.metadata.namespace,
            "kind": kind,
            "name": workload.metadata.name,
            "images": [
                container.image for container in workload.spec.template.spec.containers
            ]
        })
    return workload_list

def make_cronjob_list(workload):
    kind="CronJob"
    workload_list = []
    for workload in workload:
        if workload.metadata.owner_references:
            continue
        workload_list.append({
            "namespace": workload.metadata.namespace,
            "kind": kind,
            "name": workload.metadata.name,
            "images": [
                container.image for container in workload.spec.job_template.spec.template.spec.containers
            ]
        })
    return workload_list

def get_replica_set():
    v1 = client.AppsV1Api()
    replica_sets_list = []
    try:
        replica_sets = v1.list_replica_set_for_all_namespaces()
        replica_sets = make_list(replica_sets.items, "ReplicaSet")
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->list_replica_set_for_all_namespaces: {e}")
        return []
    
def get_deployments():
    v1 = client.AppsV1Api()
    deployments_list = []
    try:
        deployments = v1.list_deployment_for_all_namespaces()
        deployments_list = make_list(deployments.items, "Deployment")
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->list_deployment_for_all_namespaces: {e}")
        return []
    return deployments_list

def get_statefulsets():
    v1 = client.AppsV1Api()
    statefulsets_list = []
    try:
        statefulsets = v1.list_stateful_set_for_all_namespaces()
        statefulsets_list = make_list(statefulsets.items, "StatefulSet")
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->list_stateful_set_for_all_namespaces: {e}")
        return []
    return statefulsets_list

def get_daemonsets():
    v1 = client.AppsV1Api()
    daemonsets_list = []
    try:
        daemonsets = v1.list_daemon_set_for_all_namespaces()
        daemonsets_list = make_list(daemonsets.items, "DaemonSet")
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->list_daemon_set_for_all_namespaces: {e}")
        return []
    return daemonsets_list

def get_jobs():
    v1 = client.BatchV1Api()
    jobs_list = []
    try:
        jobs = v1.list_job_for_all_namespaces()
        jobs_list = make_list(jobs.items, "Job")
    except ApiException as e:
        print(f"Exception when calling BatchV1Api->list_job_for_all_namespaces: {e}")
        return []
    return jobs_list

def get_cronjobs():
    v1 = client.BatchV1Api()
    cronjobs_list = []
    try:
        cronjobs = v1.list_cron_job_for_all_namespaces()
        # print(cronjobs.items)
        cronjobs_list = make_cronjob_list(cronjobs.items)
    except ApiException as e:
        print(f"Exception when calling BatchV1beta1Api->list_cron_job_for_all_namespaces: {e}")
        return []
    return cronjobs_list

def get_pods():
    v1 = client.CoreV1Api()
    try:
        pods = v1.list_pod_for_all_namespaces(watch=False)
        pods_list = []
        for pod in pods.items:
            owner_references = getattr(pod.metadata, "owner_references", [])
            if not owner_references:
                pods_list.append({
                    "namespace": pod.metadata.namespace,
                    "kind": "Pod",
                    "name": pod.metadata.name,
                    "images": [
                        container.image for container in pod.spec.containers
                    ]
                })
        return pods_list
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