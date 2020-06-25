from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB

with Diagram("architecture", show=False):
    
    with Cluster("Database Private Subnets"):
        int_lb = ELB("Internal NLB")

        with Cluster("Proxy Sql"):
            proxysql = EC2("node1")
            proxysql - [EC2("node2")]

        with Cluster("MySQL DB"):
            db = EC2("master")
            db - [EC2("Candidate Master"), EC2("Slave1"), EC2("Slave2"), EC2("Delayed_Slave")]

        int_lb >> proxysql >> db
