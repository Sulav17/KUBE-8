import os
from fastapi import APIRouter, HTTPException
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

KUBE_MODE = os.getenv("KUBERNETES_MODE", "local").lower()
K8S_ENABLED = False
IS_LOCAL = False

try:
    if KUBE_MODE == "local":
        config.load_kube_config()
        IS_LOCAL = True
        K8S_ENABLED = True
        print("[INFO] Loaded Kubernetes config from ~/.kube/config")
    elif KUBE_MODE == "incluster":
        config.load_incluster_config()
        K8S_ENABLED = True
        print("[INFO] Loaded Kubernetes config from in-cluster environment")
    elif KUBE_MODE == "disabled":
        print("[INFO] Kubernetes integration is disabled via .env")
    else:
        raise ValueError(f"Invalid KUBERNETES_MODE: {KUBE_MODE}")
except (ConfigException, ValueError) as e:
    print(f"[WARNING] Could not load Kubernetes config: {str(e)}")

@router.get("/context")
def get_kube_context():
    if not K8S_ENABLED:
        raise HTTPException(status_code=503, detail="Kubernetes is not configured")
    if not IS_LOCAL:
        raise HTTPException(status_code=400, detail="Only available in local mode")

    contexts, current_context = config.list_kube_config_contexts()
    return {
        "current_context": current_context["name"],
        "contexts": [ctx["name"] for ctx in contexts],
    }

@router.get("/namespaces")
def list_namespaces():
    if not K8S_ENABLED:
        raise HTTPException(status_code=503, detail="Kubernetes is not configured")

    try:
        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pods/{namespace}")
def list_pods(namespace: str):
    if not K8S_ENABLED:
        raise HTTPException(status_code=503, detail="Kubernetes is not configured")

    try:
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace)
        return [pod.metadata.name for pod in pods.items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
