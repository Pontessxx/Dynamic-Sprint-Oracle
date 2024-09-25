Aqui está a versão atualizada do README com a adição da comparação entre as abordagens em Java e Python:

---

# Projeto: Sistema de Consultas e Filtros de Tabelas de Banco de Dados Oracle

## Descrição Geral

Este projeto implementa um sistema de consultas em um banco de dados Oracle utilizando Python. Através de um menu interativo, o usuário pode acessar diferentes tabelas relacionadas ao sistema de treinamento em procedimentos médicos, realizar consultas, e aplicar filtros personalizados para visualizar dados específicos. 

O sistema utiliza a biblioteca `oracledb` para conexão com o banco de dados Oracle e as bibliotecas `InquirerPy` para criação de menus e interação com o usuário no terminal, além de `tabulate` para exibir os resultados em formato tabular.

### Funcionalidades Principais

1. **Consulta de Sessões de Treinamento**: Permite ao usuário visualizar todas as sessões de treinamento e filtrar os resultados por nome de usuário.
2. **Consulta de Feedback dos Usuários**: Exibe feedbacks dados pelos usuários, com a possibilidade de filtrar por nome de usuário.
3. **Consulta de Histórico de Manutenção**: Exibe o histórico de manutenção de dispositivos, permitindo filtrar por tipo de dispositivo.
4. **Outras Consultas**: Sistema facilmente expansível para novas tabelas, como conquistas dos usuários e métricas de desempenho.

---

## Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento da aplicação.
- **OracleDB (oracledb)**: Biblioteca para conectar-se e interagir com o banco de dados Oracle.
- **InquirerPy**: Biblioteca para criação de menus e interação com o terminal.
- **Tabulate**: Utilizada para exibir os resultados das consultas em formato de tabela.

---

## Comparação com Java: DTO, DMO e DIO

Durante o desenvolvimento de sistemas de conexão com banco de dados em Java, utilizamos as estruturas **DTO (Data Transfer Object)**, **DMO (Data Model Object)** e **DIO (Data Input/Output Object)** para organizar o código, transferir dados e realizar a comunicação com o banco de dados Oracle. Essa arquitetura, muito comum em sistemas Java, promove um design claro, orientado a objetos e modular para a interação com o banco de dados.

Por outro lado, optamos por desenvolver a consulta em Python neste projeto por várias razões:
- **Ampla gama de bibliotecas**: Python possui uma vasta quantidade de bibliotecas como `InquirerPy` e `tabulate`, que permitem uma interação mais intuitiva e dinâmica com o usuário.
- **Maior rapidez de desenvolvimento**: Em comparação ao Java, Python oferece uma sintaxe mais enxuta e permite o desenvolvimento de funcionalidades de maneira mais rápida e simples, sem a necessidade de grandes configurações.
- **Performance**: A integração com bibliotecas nativas e de terceiros oferece um processamento eficiente, mesmo ao manipular grandes volumes de dados.
  
Essa escolha foi feita para atender a necessidades que requerem uma interação mais ágil e uma interface simples, sem sacrificar a performance e a modularidade.

---

## Estrutura de Classes

O projeto foi organizado em várias classes, cada uma responsável por uma tabela específica e pelas operações relacionadas a essa tabela:

- **DatabaseConnection**: Classe responsável pela conexão ao banco de dados Oracle.
- **TrainingSessions**: Implementa as consultas e filtros para a tabela de sessões de treinamento.
- **UserFeedback**: Implementa as consultas e filtros para a tabela de feedback dos usuários.
- **MaintenanceHistory**: Implementa as consultas e filtros para a tabela de histórico de manutenção.

Essa abordagem modular ajuda a manter o código organizado e facilita a adição de novas funcionalidades no futuro.

### Estrutura das Classes:

- **DatabaseConnection**: Gerencia a conexão com o banco de dados Oracle e fornece um cursor para execução de consultas.
- **TrainingSessions**: Consulta a tabela `Sessoes_Treinamento` e permite filtrar as sessões por nome de usuário.
- **UserFeedback**: Consulta a tabela `Feedback_Usuarios` e permite filtrar os feedbacks por nome de usuário.
- **MaintenanceHistory**: Consulta a tabela `Historico_Manutencao_Dispositivos` e permite filtrar o histórico por dispositivo.

---

## Desafios Enfrentados

### 1. **Conexão com Banco de Dados Oracle**
   - O primeiro desafio foi garantir a conexão correta ao banco de dados Oracle utilizando a biblioteca `oracledb`. Houve problemas relacionados à configuração do cliente Oracle, mas foram resolvidos ao instalar a versão correta do cliente e garantir que o ambiente estivesse devidamente configurado.

### 2. **Estruturação do Código**
   - Inicialmente, todas as consultas e filtros estavam em uma única classe, o que dificultava a manutenção e expansão do código. A reestruturação do código utilizando classes separadas para cada tabela foi fundamental para melhorar a organização e escalabilidade do sistema.

### 3. **Interação com o Usuário no Terminal**
   - Criar uma interface interativa no terminal, utilizando `InquirerPy`, foi desafiador, principalmente para gerenciar múltiplos filtros dinâmicos. Para superar isso, foram implementadas funções específicas de filtro para cada tabela, o que tornou o código mais modular e flexível.

### 4. **Aplicação de Filtros**
   - Implementar filtros dinâmicos, como filtrar por nome de usuário ou tipo de dispositivo, exigiu a criação de funções dedicadas para cada tipo de consulta. Esse foi um desafio interessante que, ao ser resolvido, tornou o sistema altamente flexível e adaptável a diferentes tipos de consultas e filtros.

---

## Lógica por Trás do Código

O código segue uma abordagem modular e orientada a objetos. Cada tabela do banco de dados possui sua própria classe, responsável por:
- Fazer as consultas SQL.
- Aplicar filtros específicos a cada consulta, baseados nas escolhas do usuário.

O fluxo de execução é simples:
1. O usuário seleciona uma tabela ou ação no menu principal.
2. O sistema exibe os dados completos daquela tabela.
3. O usuário é questionado se deseja aplicar filtros. Caso sim, o sistema oferece opções de filtros baseadas nos dados disponíveis.
4. Após aplicar os filtros, os resultados filtrados são exibidos em formato de tabela.

### Exemplos de Filtros Implementados

- **Filtro por Nome de Usuário**: Utilizado nas tabelas de sessões de treinamento e feedback dos usuários.
- **Filtro por Tipo de Dispositivo**: Aplicado na tabela de histórico de manutenção.
- **Filtro por Métrica**: Pode ser aplicado em tabelas de métricas de desempenho.

---

## Como Isso Auxilia/Impacta o Projeto

- **Organização e Escalabilidade**: A separação do código em diferentes classes para cada tabela torna o sistema mais organizado, fácil de manter e escalável. Novas tabelas podem ser facilmente adicionadas sem impactar as funcionalidades existentes.
  
- **Eficiência e Usabilidade**: A implementação de filtros personalizados melhora a usabilidade do sistema, permitindo que os usuários visualizem rapidamente as informações que são mais relevantes para eles.
  
- **Facilidade de Interação**: A interface no terminal, construída com `InquirerPy`, oferece uma maneira intuitiva de navegar pelos dados e aplicar filtros sem precisar digitar comandos ou SQL diretamente, o que melhora a experiência do usuário.

---

## Como Executar o Projeto

1. **Instalação de Dependências**:
   - Clone este repositório.
   - Instale as dependências do projeto executando:
     ```bash
     pip install oracledb InquirerPy tabulate
     ```

2. **Configuração do Banco de Dados**:
   - Certifique-se de que as credenciais do banco de dados Oracle estão corretas no arquivo `main.py` (usuário, senha e DSN).

3. **Executar o Projeto**:
   - Para executar o sistema, basta rodar o seguinte comando no terminal:
     ```bash
     python main.py
     ```

---

## Conclusão

Este projeto serve como um exemplo prático de como construir um sistema de consultas interativo, modular e escalável, que pode ser adaptado para diferentes necessidades de negócios. Ele demonstra o poder da programação orientada a objetos combinada com bibliotecas modernas de Python para criar interfaces intuitivas e eficientes, mesmo em um ambiente de terminal.

