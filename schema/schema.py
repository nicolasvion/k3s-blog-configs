from diagrams import Cluster, Diagram
from diagrams.k8s.compute import Pod, Deployment, RS
from diagrams.k8s.network import Ingress
from diagrams.aws.general import Users
from diagrams.onprem.certificates import CertManager, LetsEncrypt
from diagrams.k8s.podconfig import Secret

graph_attr = {
    "pad": "1",
    "fontsize": "8",
    "fontname": "IBM Plex Mono bold",
    "bgcolor": "transparent"
}

node_attr = {
    "width": "1",
    "height": "1",
    "fontsize": "8",
    "fontname": "IBM Plex Mono"
}

with Diagram("Setup a blog on k3s", show=False, graph_attr=graph_attr, node_attr=node_attr, direction="TB"):
    users = Users("Users")
    with Cluster("LetsEncrypt API Servers", graph_attr=graph_attr):
        letsencrypt = LetsEncrypt("LE SSL Certificate")
    with Cluster("BareMetal Server", graph_attr=graph_attr):
        with Cluster("K8S Cluster", graph_attr=graph_attr):
            with Cluster("NS Cert-Manager", graph_attr=graph_attr):
                certificate_request = CertManager("mywebsite.com")
            with Cluster("NS www", graph_attr=graph_attr):
                website_secret = Secret("mywebsite.com")
                with Cluster("Ingress", graph_attr=graph_attr):
                    ingress = Ingress("https")
                with Cluster("Pods", graph_attr=graph_attr):
                    pod = Pod('website')
                with Cluster("Deployment", graph_attr=graph_attr):
                    pod_deploy = Deployment("website")
                with Cluster("RS", graph_attr=graph_attr):
                    pod_rs = RS("website")

    letsencrypt >> website_secret >> ingress

    certificate_request >> letsencrypt
    users >> ingress >> pod

    pod_rs >> pod
    pod_deploy >> pod
