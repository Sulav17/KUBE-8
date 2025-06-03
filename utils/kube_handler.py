# utils/kube_handler.py

import yaml
import os

KUBECONFIG_PATH = os.path.expanduser("~/.kube/config")

def load_kube_contexts():
    with open(KUBECONFIG_PATH, "r") as f:
        kubeconfig = yaml.safe_load(f)
    return [ctx["name"] for ctx in kubeconfig.get("contexts", [])]
