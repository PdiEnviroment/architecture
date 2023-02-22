from diagrams import Diagram
from diagrams import Cluster, Diagram, Edge

from diagrams.aws.network import CF, APIGateway;
from diagrams.aws.compute import ECS, Lambda;
from diagrams.aws.database import DDB, Elasticache, RDS;
from diagrams.aws.integration import SQS;

with Diagram("Diagrama de contexto da solução de inbound e outbound"):
    fd_portal = CF("Front End") 
    gt_gateway = APIGateway("Gateway")

    with Cluster("Barramento Cambial"):
        api_mercado = ""
            
        sq_barramento = SQS("Barramento")

        with Cluster("Contexto de Mercado"):
            db_mercado = Elasticache("Base Mercado")
            api_mercado = ECS("Mercado")

            ag_mercado = Lambda("Agent Mercado")            

            api_mercado >> db_mercado

            ag_mercado >> db_mercado

        with Cluster("Contexto de Negociação"):
            api_negociador = ECS("Negociador")
            db_negociador = DDB("Base Negociador")

            api_oraculo = ECS("Oraculo")
            db_oraculo = DDB("Base Oraculo")

            api_negociador >> db_negociador
            gt_gateway >> api_negociador

            api_negociador >> api_oraculo
            api_oraculo >> db_oraculo

            api_oraculo >> api_mercado

            api_negociador \
                >> Edge(color="darkgreen") \
                << sq_barramento       

        with Cluster("Contexto de Fechamemto"):
            api_fechamento = ECS("Fechamento")
            db_fechamento = DDB("Base Fechamento")

            api_fechamento >> db_fechamento

            gt_gateway >> api_fechamento

            api_fechamento >> api_mercado

            api_fechamento \
                >> Edge(color="darkgreen") \
                << sq_barramento       


        with Cluster("Contexto Parceiros"):
            api_parceiros = ECS("Parceiros")
            db_parceiros = RDS("DB Parceiros")

            api_parceiros >> db_parceiros

            gt_gateway >> api_parceiros

            api_parceiros \
                >> Edge(color="darkgreen") \
                << sq_barramento        
    
     

    fd_portal \
        >> Edge(color="darkgreen") \
        << gt_gateway        
    