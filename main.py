import oracledb
from InquirerPy import prompt
from tabulate import tabulate

# Classe responsável pela conexão ao banco de dados
class DatabaseConnection:
    def __init__(self, username, password, dsn):
        """
        Inicializa a classe de conexão com as credenciais do banco de dados.
        
        :param username: Nome de usuário do banco de dados.
        :param password: Senha do banco de dados.
        :param dsn: Data Source Name (localização do banco de dados).
        """
        self.username = username
        self.password = password
        self.dsn = dsn
        self.connection = None

    def connect(self):
        """
        Estabelece a conexão com o banco de dados Oracle usando oracledb.
        """
        try:
            self.connection = oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
            print("Conexão bem-sucedida!")
        except oracledb.DatabaseError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def close(self):
        """
        Fecha a conexão com o banco de dados se ela estiver aberta.
        """
        if self.connection:
            self.connection.close()
            print("Conexão fechada.")

    def get_cursor(self):
        """
        Retorna o cursor da conexão com o banco de dados, necessário para realizar consultas SQL.
        
        :return: Cursor do banco de dados.
        """
        if self.connection:
            return self.connection.cursor()
        else:
            raise Exception("Conexão não estabelecida.")

# Classe responsável pelos selects
class SelectQueries:
    def __init__(self, db_connection):
        """
        Inicializa a classe de consultas, associando-a à conexão com o banco de dados.
        
        :param db_connection: Instância da conexão ao banco de dados.
        """
        self.db_connection = db_connection

    def fetch_training_sessions(self, filters=None):
        """
        Realiza a consulta das sessões de treinamento no banco de dados.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            st.ID_Sessao,
            u.Nome AS Usuario,
            p.Nome AS Procedimento,
            d.Nome AS Dispositivo,
            st.Data,
            st.Duracao,
            st.Resultado
        FROM 
            Sessoes_Treinamento st
        INNER JOIN 
            Usuarios u ON st.ID_Usuario = u.ID_Usuario
        INNER JOIN 
            Procedimentos p ON st.ID_Procedimento = p.ID_Procedimento
        INNER JOIN 
            Dispositivos d ON st.ID_Dispositivo = d.ID_Dispositivo
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def fetch_user_feedback(self, filters=None):
        """
        Realiza a consulta de feedbacks dos usuários no banco de dados.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            fu.ID_Feedback,
            u.Nome AS Usuario,
            p.Nome AS Procedimento,
            fu.Comentario,
            fu.Pontuacao
        FROM 
            Feedback_Usuarios fu
        INNER JOIN 
            Sessoes_Treinamento st ON fu.ID_Sessao = st.ID_Sessao
        INNER JOIN 
            Usuarios u ON st.ID_Usuario = u.ID_Usuario
        INNER JOIN 
            Procedimentos p ON st.ID_Procedimento = p.ID_Procedimento
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def fetch_instructor_feedback(self, filters=None):
        """
        Realiza a consulta de feedbacks dos instrutores no banco de dados.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            ra.ID_Relatorio,
            u.Nome AS Usuario,
            p.Nome AS Procedimento,
            ra.Feedback_Instrutor,
            ra.Pontuacao_Total
        FROM 
            Relatorios_Avaliacao ra
        INNER JOIN 
            Sessoes_Treinamento st ON ra.ID_Sessao = st.ID_Sessao
        INNER JOIN 
            Usuarios u ON st.ID_Usuario = u.ID_Usuario
        INNER JOIN 
            Procedimentos p ON st.ID_Procedimento = p.ID_Procedimento
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def fetch_maintenance_history(self, filters=None):
        """
        Realiza a consulta do histórico de manutenção de dispositivos.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            hmd.ID_Manutencao,
            d.Nome AS Dispositivo,
            hmd.Data_Manutencao,
            hmd.Descricao,
            hmd.Responsavel
        FROM 
            Historico_Manutencao_Dispositivos hmd
        INNER JOIN 
            Dispositivos d ON hmd.ID_Dispositivo = d.ID_Dispositivo
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def fetch_user_achievements(self, filters=None):
        """
        Realiza a consulta de conquistas dos usuários.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            c.Nome_Conquista,
            u.Nome AS Usuario,
            c.Descricao,
            c.Data_Conquista
        FROM 
            Conquistas c
        INNER JOIN 
            Usuarios u ON c.ID_Usuario = u.ID_Usuario
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def fetch_user_preferences(self, filters=None):
        """
        Realiza a consulta de preferências dos usuários.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            u.Nome AS Usuario,
            pt.Preferencias_Json
        FROM 
            Preferencias_Treinamento pt
        INNER JOIN 
            Usuarios u ON pt.ID_Usuario = u.ID_Usuario
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def fetch_user_metrics(self, filters=None):
        """
        Realiza a consulta de métricas dos usuários.
        
        :param filters: Lista de filtros para aplicar à consulta (opcional).
        :return: Colunas e linhas do resultado da consulta.
        """
        query = """
        SELECT 
            md.ID_Metrica,
            u.Nome AS Usuario,
            md.Tipo_Metrica,
            md.Valor
        FROM 
            Metrics_Desempenho md
        INNER JOIN 
            Sessoes_Treinamento st ON md.ID_Sessao = st.ID_Sessao
        INNER JOIN 
            Usuarios u ON st.ID_Usuario = u.ID_Usuario
        """
        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    # Função para buscar os nomes dos usuários
    def fetch_users(self):
        """
        Realiza a consulta dos nomes distintos dos usuários.
        
        :return: Lista de nomes dos usuários.
        """
        query = """
        SELECT DISTINCT u.Nome
        FROM Usuarios u
        """
        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        users = [row[0] for row in cursor.fetchall()]
        return users

    # Função para buscar os dispositivos
    def fetch_devices(self):
        """
        Realiza a consulta dos dispositivos distintos.
        
        :return: Lista de dispositivos.
        """
        query = """
        SELECT DISTINCT d.Nome
        FROM Dispositivos d
        """
        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        devices = [row[0] for row in cursor.fetchall()]
        return devices


# Funções de filtro para cada tipo de consulta
def get_filters_by_name(select_queries):
    """
    Gera filtros de consulta baseado no nome do usuário.
    
    :param select_queries: Instância de consultas.
    :return: Lista de filtros SQL.
    """
    users = select_queries.fetch_users()
    filter_options = [
        {
            "type": "list",
            "name": "usuario",
            "message": "Filtrar por nome de usuário:",
            "choices": users
        }
    ]
    filters = prompt(filter_options)
    selected_user = filters['usuario']
    return [f"u.Nome = '{selected_user}'"]


# Função para filtrar histórico de manutenção por dispositivo
def get_filters_by_device(select_queries):
    """
    Gera filtros de consulta baseado no dispositivo.
    
    :param select_queries: Instância de consultas.
    :return: Lista de filtros SQL.
    """
    devices = select_queries.fetch_devices()
    filter_options = [
        {
            "type": "list",
            "name": "dispositivo",
            "message": "Filtrar por dispositivo:",
            "choices": devices
        }
    ]
    filters = prompt(filter_options)
    selected_device = filters['dispositivo']
    return [f"d.Nome = '{selected_device}'"]


# Função que exibe o menu principal
def show_menu():
    """
    Exibe o menu principal para o usuário.
    
    :return: A consulta escolhida pelo usuário.
    """
    menu_options = [
        {
            "type": "list",
            "name": "query_choice",
            "message": "Escolha a consulta que deseja executar:",
            "choices": [
                "Consultar sessões de treinamento",
                "Consultar feedback dos usuários",
                "Consultar feedback dos instrutores",
                "Consultar histórico de manutenção",
                "Consultar conquistas dos usuários",
                "Consultar preferências dos usuários",
                "Consultar métricas dos usuários",
                "Sair"
            ]
        }
    ]
    answers = prompt(menu_options)
    return answers["query_choice"]


# Perguntar se o usuário deseja aplicar filtros
def ask_apply_filters():
    """
    Pergunta ao usuário se ele deseja aplicar filtros na consulta.
    
    :return: Boolean indicando se o usuário deseja aplicar filtros.
    """
    filter_option = [
        {
            "type": "confirm",
            "name": "apply_filters",
            "message": "Deseja aplicar filtros?",
            "default": False
        }
    ]
    answer = prompt(filter_option)
    return answer["apply_filters"]


# Função principal que gerencia o menu e as escolhas
def main():
    """
    Função principal que executa o sistema de consultas, 
    permitindo que o usuário escolha qual tabela consultar e aplique filtros.
    """
    username = 'rm98036'
    password = '191004'
    dsn = 'oracle.fiap.com.br:1521/orcl'

    db = DatabaseConnection(username, password, dsn)
    try:
        db.connect()
        
        queries = SelectQueries(db)
        
        while True:
            choice = show_menu()
            
            if choice == "Consultar sessões de treinamento":
                columns, sessions = queries.fetch_training_sessions()
                print("Sessões de Treinamento (completa):")
                print(tabulate(sessions, headers=columns, tablefmt="pretty"))

            elif choice == "Consultar feedback dos usuários":
                columns, feedbacks = queries.fetch_user_feedback()
                print("Feedback dos Usuários (completo):")
                print(tabulate(feedbacks, headers=columns, tablefmt="pretty"))

                if ask_apply_filters():
                    filters = get_filters_by_name(queries)
                    columns, filtered_feedbacks = queries.fetch_user_feedback(filters)
                    print("Feedback dos Usuários (filtrado):")
                    print(tabulate(filtered_feedbacks, headers=columns, tablefmt="pretty"))

            elif choice == "Consultar feedback dos instrutores":
                columns, feedbacks = queries.fetch_instructor_feedback()
                print("Feedback dos Instrutores (completo):")
                print(tabulate(feedbacks, headers=columns, tablefmt="pretty"))

                if ask_apply_filters():
                    filters = get_filters_by_name(queries)
                    columns, filtered_feedbacks = queries.fetch_instructor_feedback(filters)
                    print("Feedback dos Instrutores (filtrado):")
                    print(tabulate(filtered_feedbacks, headers=columns, tablefmt="pretty"))

            elif choice == "Consultar histórico de manutenção":
                columns, history = queries.fetch_maintenance_history()
                print("Histórico de Manutenção (completo):")
                print(tabulate(history, headers=columns, tablefmt="pretty"))

                if ask_apply_filters():
                    filters = get_filters_by_device(queries)
                    columns, filtered_history = queries.fetch_maintenance_history(filters)
                    print("Histórico de Manutenção (filtrado):")
                    print(tabulate(filtered_history, headers=columns, tablefmt="pretty"))

            elif choice == "Consultar conquistas dos usuários":
                columns, achievements = queries.fetch_user_achievements()
                print("Conquistas dos Usuários (completo):")
                print(tabulate(achievements, headers=columns, tablefmt="pretty"))

                if ask_apply_filters():
                    filters = get_filters_by_name(queries)
                    columns, filtered_achievements = queries.fetch_user_achievements(filters)
                    print("Conquistas dos Usuários (filtrado):")
                    print(tabulate(filtered_achievements, headers=columns, tablefmt="pretty"))

            elif choice == "Consultar preferências dos usuários":
                columns, preferences = queries.fetch_user_preferences()
                print("Preferências dos Usuários (completo):")
                print(tabulate(preferences, headers=columns, tablefmt="pretty"))

                if ask_apply_filters():
                    filters = get_filters_by_name(queries)
                    columns, filtered_preferences = queries.fetch_user_preferences(filters)
                    print("Preferências dos Usuários (filtrado):")
                    print(tabulate(filtered_preferences, headers=columns, tablefmt="pretty"))

            elif choice == "Consultar métricas dos usuários":
                columns, metrics = queries.fetch_user_metrics()
                print("Métricas dos Usuários (completo):")
                print(tabulate(metrics, headers=columns, tablefmt="pretty"))

            elif choice == "Sair":
                print("Saindo...")
                break

    finally:
        db.close()


if __name__ == "__main__":
    main()
