from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53
from diagrams.aws.network import PrivateSubnet
from diagrams.aws.network import CF
from diagrams.aws.storage import S3, S3Glacier

with Diagram("architecture", show=False):
    dns = Route53("www.A.com")
    static_dns = CF("static.A.com")
    static_pages = S3("static pages in S3")
    archive = S3Glacier("Archived Logs to Glacier")

    with Cluster("Public Subnet"):
        ext_lb = ELB("External ALB")
   # int_lb = ELB("Internal ALB")

    with Cluster("Private Subnet"):
        int_lb_frontend = ELB("Internal ALB FE")
        int_lb_backend = ELB("Internal ALB BE")

        with Cluster("Nginx FE"):
            nginx_frontend = AutoScaling("Nginx FE")

        with Cluster("Frontend"):
            frontend = AutoScaling("Frontend")

        with Cluster("Nginx BE"):
            nginx_backend = AutoScaling("Nginx BE")

        with Cluster("Backend"):
            backend = AutoScaling("Backend")

    with Cluster("Database Subnet"):

        with Cluster("DB Cluster"):
            db = RDS("Master")
            db - [RDS("Slave")]

        vault = EC2("Vault")

        with Cluster("Redis Sentinel"):
            redis = EC2("node1")
            redis - [EC2("node2"),EC2("node3")]

    with Cluster("Central Logging and Monitoring"):
        
        with Cluster("ELK"):
            elk = EC2("ELK Cluster")
        with Cluster("Prometheus"):
            monit = EC2("Prometheus")


    dns >> ext_lb >> nginx_frontend
    static_dns >> static_pages
    nginx_frontend >> int_lb_frontend >> frontend 
    frontend >> nginx_backend >> int_lb_backend >> backend
    nginx_frontend >> elk
    nginx_backend >> elk
    frontend >> elk
    backend >> elk
    nginx_frontend >> monit
    nginx_backend >> monit
    frontend >> monit
    backend >> monit
    backend >> db
    backend >> vault
    backend >> redis
    elk >> archive
