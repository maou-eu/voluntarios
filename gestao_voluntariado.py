import sqlite3

# Configuração do banco de dados SQLite
db_file = 'projeto_voluntariado.db'

def criar_conexao():
    try:
        conn = sqlite3.connect(db_file)
        print("Conectado ao SQLite")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao SQLite: {e}")
        return None

# Criar tabelas
def criar_tabelas(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS voluntarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_inicio DATE NOT NULL,
        quadro_clinico TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS participantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        dados_relevantes TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS designacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voluntario_id INTEGER,
        participante_id INTEGER,
        FOREIGN KEY(voluntario_id) REFERENCES voluntarios(id),
        FOREIGN KEY(participante_id) REFERENCES participantes(id)
    )
    ''')
    
    conn.commit()
    cursor.close()

# Funções para gerenciamento
def adicionar_voluntario(conn, nome, data_inicio, quadro_clinico):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO voluntarios (nome, data_inicio, quadro_clinico)
    VALUES (?, ?, ?)
    ''', (nome, data_inicio, quadro_clinico))
    conn.commit()
    cursor.close()
    print("Voluntário adicionado com sucesso.")

def adicionar_participante(conn, nome, dados_relevantes):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO participantes (nome, dados_relevantes)
    VALUES (?, ?)
    ''', (nome, dados_relevantes))
    conn.commit()
    cursor.close()
    print("Participante adicionado com sucesso.")

def designar_voluntario(conn, voluntario_id, participante_id):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO designacoes (voluntario_id, participante_id)
    VALUES (?, ?)
    ''', (voluntario_id, participante_id))
    conn.commit()
    cursor.close()
    print("Voluntário designado ao participante com sucesso.")

def listar_voluntarios(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voluntarios')
    return cursor.fetchall()

def listar_participantes(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM participantes')
    return cursor.fetchall()

def listar_designacoes(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM designacoes')
    return cursor.fetchall()

# Função principal para o menu
def menu(conn):
    while True:
        print("\nMenu:")
        print("1. Adicionar Voluntário")
        print("2. Adicionar Participante")
        print("3. Designar Voluntário")
        print("4. Listar Voluntários")
        print("5. Listar Participantes")
        print("6. Listar Designações")
        print("7. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            nome = input("Nome do Voluntário: ")
            data_inicio = input("Data de Início (YYYY-MM-DD): ")
            quadro_clinico = input("Quadro Clínico: ")
            adicionar_voluntario(conn, nome, data_inicio, quadro_clinico)
        
        elif escolha == '2':
            nome = input("Nome do Participante: ")
            dados_relevantes = input("Dados Relevantes: ")
            adicionar_participante(conn, nome, dados_relevantes)
        
        elif escolha == '3':
            voluntario_id = int(input("ID do Voluntário: "))
            participante_id = int(input("ID do Participante: "))
            designar_voluntario(conn, voluntario_id, participante_id)
        
        elif escolha == '4':
            print("\nVoluntários:")
            for v in listar_voluntarios(conn):
                print(v)
        
        elif escolha == '5':
            print("\nParticipantes:")
            for p in listar_participantes(conn):
                print(p)
        
        elif escolha == '6':
            print("\nDesignações:")
            for d in listar_designacoes(conn):
                print(d)
        
        elif escolha == '7':
            conn.close()
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    conn = criar_conexao()
    if conn:
        criar_tabelas(conn)
        menu(conn)
