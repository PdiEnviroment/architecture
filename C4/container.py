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
        gatewayApi = Container(
            name="Gateway Barramento",            
            description="Responsabilidade receber as chamadas do meio externo e direcionar para o recurso correto"
        )

        portal = Container(
            name="Portal Transações",
            description="Prover recursos para o usuario",
            technology="SPA (Angular, React, Vue Js)"
        )

        with SystemBoundary("Contexto de Negociacao"):
            co_negociador = Container(name = "API Negociador", description= "Responsavel por realizar a negociação do ambiente")
            co_oraculo = Container(name = "API do Oraculo da Negociacao", description="Estabelecimento de algumas premissas para que a mesma ocorra")
            db_oraculo = Database(name = "DB Oraculo", description="Base de dados com os oraculos da transcao",technology="NoSQL")
            db_negociador = Database(name = "DB Negociacao", description="Base de dados Negociacao", technology="SQL")

            co_negociador >> Relationship("Persiste dados") >> db_negociador
            co_oraculo >> Relationship("Persiste dados") >> db_oraculo
            co_negociador >> Relationship("Consulta oraculo") >> co_oraculo            

        with SystemBoundary("Contexto de Mercado"):
           co_mercado = Container(name= "API Mercado", description= "Api criada para realizar consultas do mercado")        
           db_negociador = Database(name="DB Mercado",description="Responsavel por persistir taxas do mercado",technology="Cache")
           ag_negociador = Container(name= "Agent Mercado", description="Responsavel por consultar fontes externas e deixar disponivel")

           ag_negociador >> Relationship("Persiste dados para o ambiente") >> db_negociador
           co_mercado >> Relationship("Consulta a base de cache") >> db_negociador

        with SystemBoundary("Contexto de Fechamento"):
            co_fechamento = Container(name = "API Fechamento", description= "Api que realiza fechamento")
            db_fechamento = Database(name= "DB Fechamento", description="Armazenamento de todas as operações fechadas", technology="NoSQL")

            co_fechamento >> Relationship("Salva a transação") >> db_fechamento

    biro = System(name="Biro de taxas", description="Fornecimento de taxas do mercado para operação", external=True)

    remessadora >> Relationship("Acessa o portal") >> portal

    intituicaoFinanceira >> Relationship("Acessa o portal") >> portal

    portal >> Relationship("Envia propostas de negociação / Fechamentos") >> gatewayApi

    ag_negociador >> Relationship("Consulta Biro") >> biro

    co_oraculo >> Relationship("Consulta taxas a mercado") >> co_mercado

    #Relacionamento do Gateway
    gatewayApi >> Relationship("Consome API") >> co_negociador
    gatewayApi >> Relationship("Consome API") >> co_fechamento

