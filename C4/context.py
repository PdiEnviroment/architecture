#context
from diagrams import Diagram
from diagrams.c4 import Person, Container, Database, System, SystemBoundary, Relationship

graph_attr = {
    "splines": "spline",
}

with Diagram("Diagrama de contexto da solução de inbound e outbound", direction="TB", graph_attr=graph_attr):
    intituicaoFinanceira = Person(name="Instituição Financeira", description="Intituição regulamentada e altorizado a operar cambio no pais (corretora, bancos, fintechs)")
    remessadora = Person(name="Remessadora", description="Empresa responsavel por enviar dinheiro a outros paises") 
    bacen = Person(name="BACEN", description="Banco central do brasil") 

    with SystemBoundary("Barramento Cambial"):
        backend = Container(
            name="Barramento",            
            description="Responsabilidade de receber chamadas do meio externo"
        )

    remessadora >> Relationship("Envia operação para o barramento") >> backend
    backend >> Relationship("Envia dados a intituição") >> intituicaoFinanceira
    
    intituicaoFinanceira >> Relationship("Envia confirmação bacen") >> backend
    backend >> Relationship("Envia operação para o Bacen") >> bacen


