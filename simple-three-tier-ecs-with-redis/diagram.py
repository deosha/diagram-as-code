from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53

with Diagram("architecture", show=False):
    dns = Route53("dns")
    ext_lb = ELB("External ALB")
    int_lb = ELB("Internal ALB")

    with Cluster("Nginx-ECS"):
        nginx = [ECS("Nginx"),
                     ECS("Nginx"),
                     ECS("Nginx")]

    with Cluster("API-ECS"):
        backend = [ECS("Api"),
                     ECS("Api"),
                     ECS("Api")]

    with Cluster("DB Cluster"):
        db = RDS("Master")
        db - [RDS("Slave")]

    with Cluster("Redis Sentinel"):
        redis = EC2("node1")
        redis - [EC2("node2"),EC2("node3")]


    dns >> ext_lb >> nginx
    nginx >> int_lb >> backend >> redis
    #backend >> redis
    backend >> db
