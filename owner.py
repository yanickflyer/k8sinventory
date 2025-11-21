from kubernetes import client, config
from kubernetes.client.rest import ApiException


try:
    config.load_kube_config()
except Exception as e:
    print(f"Error loading kube config: {e}")

def get_replica_set_owner(replica_set_name, namespace):
    v1 = client.AppsV1Api()
    try:
        rs = v1.read_namespaced_replica_set(
            replica_set_name, 
            namespace
        )
        rs_owner = next(
            (owner for owner in getattr(rs.metadata, "owner_references", []) 
             if owner.controller), 
            None
        )
        if rs_owner:
            return rs_owner.kind, rs_owner.name
    except ApiException:
        pass
    return None, None

def get_job_owner(job_name, namespace):
    v1 = client.BatchV1Api()
    try:
        job = v1.read_namespaced_job(
            job_name, 
            namespace
        )
        job_owner = next(
            (owner for owner in getattr(job.metadata, "owner_references", []) 
             if owner.controller), 
            None
        )
        if job_owner:
            return job_owner.kind, job_owner.name
    except ApiException:
        pass
    return None, None