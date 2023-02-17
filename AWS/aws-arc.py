from diagrams import Diagram
from diagrams import Cluster, Diagram, Edge

from diagrams.aws.network import CF, APIGateway;
from diagrams.aws.database import RDS

with Diagram("Diagrama de contexto da solução de inbound e outbound"):
    fd_portal = CF("Front End") 
    gt_gateway = APIGateway("Gateway")
    
    
    fd_portal \
        >> Edge(color="darkgreen") \
        << gt_gateway        
    