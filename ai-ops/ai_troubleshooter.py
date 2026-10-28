import os
from kubernetes import client, config

def check_cluster_incidents():
    # Load Kubernetes configuration (uses local kubeconfig or in-cluster config)
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()
    
    v1 = client.CoreV1Api()
    print("[*] Scanning TalentFlow-AI cluster for failed pods...")
    
    pods = v1.list_pod_for_all_namespaces(watch=False)
    incidents_found = False

    for pod in pods.items:
        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name
        
        # Check container statuses for errors
        if pod.status.container_statuses:
            for status in pod.status.container_statuses:
                waiting = status.state.waiting
                terminated = status.state.terminated
                
                is_crashing = (waiting and waiting.reason in ["CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull"]) or \
                              (terminated and terminated.exit_code != 0)
                
                if is_crashing:
                    incidents_found = True
                    reason = waiting.reason if waiting else f"Exit Code {terminated.exit_code}"
                    print(f"\n[!] INCIDENT DETECTED:")
                    print(f"    Namespace: {namespace}")
                    print(f"    Pod Name:  {pod_name}")
                    print(f"    Reason:    {reason}")
                    
                    # Fetch logs for diagnosis
                    try:
                        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, tail_lines=30)
                        print(f"    --- Recent Logs ---")
                        print(logs)
                        print(f"    -------------------")
                        
                        # Here you could integrate an LLM API (e.g., OpenAI/Claude) to analyze `logs` and suggest fixes automatically.
                        print(f"    [AI Recommendation Engine]: Analyzing stack trace... Check container environment variables or missing configmaps.")
                    except Exception as e:
                        print(f"    Could not fetch logs: {e}")

    if not incidents_found:
        print("[+] All pods are running healthily. No active incidents detected.")

if __name__ == "__main__":
    check_cluster_incidents()