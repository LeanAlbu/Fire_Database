import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import subprocess

class SistemaQueimadas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoramento de Focos de Queimada")
        self.root.geometry("900x600")
        self.root.minsize(900, 600)
        
        # Conexão com o banco de dados
        self.conn = None
        self.cursor = None
        
        # Frame principal
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de conexão com o BD
        self.connection_frame = ttk.LabelFrame(self.main_frame, text="Conexão com o Banco de Dados", padding="10")
        self.connection_frame.pack(fill=tk.X, pady=5)
        
        # Campos para conexão
        ttk.Label(self.connection_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.host_entry = ttk.Entry(self.connection_frame, width=15)
        self.host_entry.grid(row=0, column=1, padx=5, pady=2)
        self.host_entry.insert(0, "localhost")
        
        ttk.Label(self.connection_frame, text="Porta:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.port_entry = ttk.Entry(self.connection_frame, width=6)
        self.port_entry.grid(row=0, column=3, padx=5, pady=2)
        self.port_entry.insert(0, "5432")
        
        ttk.Label(self.connection_frame, text="Banco:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.dbname_entry = ttk.Entry(self.connection_frame, width=15)
        self.dbname_entry.grid(row=0, column=5, padx=5, pady=2)
        self.dbname_entry.insert(0, "firebase")
        
        ttk.Label(self.connection_frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.user_entry = ttk.Entry(self.connection_frame, width=15)
        self.user_entry.grid(row=1, column=1, padx=5, pady=2)
        self.user_entry.insert(0, "postgres")
        
        ttk.Label(self.connection_frame, text="Senha:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.password_entry = ttk.Entry(self.connection_frame, width=15, show="*")
        self.password_entry.grid(row=1, column=3, padx=5, pady=2)
        
        self.connect_button = ttk.Button(self.connection_frame, text="Conectar", command=self.conectar_bd)
        self.connect_button.grid(row=1, column=5, padx=5, pady=2)
        
        self.status_label = ttk.Label(self.connection_frame, text="Status: Desconectado", foreground="red")
        self.status_label.grid(row=1, column=4, sticky=tk.W, padx=5, pady=2)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Aba de registros de queimadas
        self.tab_registros = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_registros, text="Focos de Queimada")
        
        # Aba de estatísticas
        self.tab_estatisticas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_estatisticas, text="Estatísticas")
        
        # Aba de configurações
        self.tab_config = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_config, text="Configurações")
        
        # Conteúdo da aba de registros
        self.setup_registros_tab()
        
        # Conteúdo da aba de estatísticas
        self.setup_estatisticas_tab()
        
        # Conteúdo da aba de configurações
        self.setup_config_tab()
        
        # Barra de status
        self.status_bar = ttk.Label(self.root, text="Sistema de Monitoramento de Focos de Queimada", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_registros_tab(self):
        # Frame de busca
        search_frame = ttk.LabelFrame(self.tab_registros, text="Buscar Focos")
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Município:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_municipio_entry = ttk.Entry(search_frame, width=20)
        self.search_municipio_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Data Inicial:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.search_data_ini = ttk.Entry(search_frame, width=10)
        self.search_data_ini.grid(row=0, column=3, padx=5, pady=5)
        self.search_data_ini.insert(0, "AAAA-MM-DD")
        
        #ttk.Label(search_frame, text="Data Final:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        #self.search_data_fim = ttk.Entry(search_frame, width=10)
        #self.search_data_fim.grid(row=0, column=5, padx=5, pady=5)
        #self.search_data_fim.insert(0, "AAAA-MM-DD")
        
        ttk.Label(search_frame, text="Potência Mínima:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        self.search_potencia_min = ttk.Entry(search_frame, width=8)
        self.search_potencia_min.grid(row=0, column=7, padx=5, pady=5)
        
        self.search_button = ttk.Button(search_frame, text="Buscar", command=self.buscar_registros)
        self.search_button.grid(row=0, column=8, padx=5, pady=5)
        
        # Frame de registros
        registros_frame = ttk.LabelFrame(self.tab_registros, text="Focos de Queimada Detectados")
        registros_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tabela de registros
        columns = ('id', 'data_hora', 'municipio', 'regiao', 'bioma', 'latitude', 'longitude', 'potencia', 'satelite')
        self.registros_tree = ttk.Treeview(registros_frame, columns=columns, show='headings')
        
        # Definir cabeçalhos
        self.registros_tree.heading('id', text='ID')
        self.registros_tree.heading('data_hora', text='Data/Hora')
        self.registros_tree.heading('municipio', text='Município')
        self.registros_tree.heading('regiao', text='Região')
        self.registros_tree.heading('bioma', text='Bioma')
        self.registros_tree.heading('latitude', text='Latitude')
        self.registros_tree.heading('longitude', text='Longitude')
        self.registros_tree.heading('potencia', text='Potência')
        self.registros_tree.heading('satelite', text='Satélite')
        
        # Definir larguras das colunas
        self.registros_tree.column('id', width=50, anchor=tk.CENTER)
        self.registros_tree.column('data_hora', width=120, anchor=tk.CENTER)
        self.registros_tree.column('municipio', width=120)
        self.registros_tree.column('regiao', width=120)
        self.registros_tree.column('bioma', width=100)
        self.registros_tree.column('latitude', width=80, anchor=tk.CENTER)
        self.registros_tree.column('longitude', width=80, anchor=tk.CENTER)
        self.registros_tree.column('potencia', width=80, anchor=tk.CENTER)
        self.registros_tree.column('satelite', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(registros_frame, orient=tk.VERTICAL, command=self.registros_tree.yview)
        self.registros_tree.configure(yscroll=scrollbar.set)
        
        # Posicionar tabela e scrollbar
        self.registros_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Adicionar menu de contexto
        self.registros_tree.bind("<Button-3>", self.show_context_menu)
        self.registros_tree.bind("<Double-1>", self.ver_detalhes)
        
        # Frame de ações
        actions_frame = ttk.Frame(self.tab_registros)
        actions_frame.pack(fill=tk.X, pady=5)
        
        self.add_button = ttk.Button(actions_frame, text="Adicionar", command=self.adicionar_registro)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(actions_frame, text="Editar", command=self.editar_registro)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(actions_frame, text="Excluir", command=self.excluir_registro)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(actions_frame, text="Exportar", command=self.exportar_dados)
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = ttk.Button(actions_frame, text="Atualizar", command=self.carregar_registros)
        self.refresh_button.pack(side=tk.RIGHT, padx=5)

    def setup_estatisticas_tab(self):
        # Frame principal para estatísticas
        stats_frame = ttk.Frame(self.tab_estatisticas)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para opções de filtro
        filter_frame = ttk.LabelFrame(stats_frame, text="Filtros")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Período:").grid(row=0, column=0, padx=5, pady=5)
        self.periodo_combo = ttk.Combobox(filter_frame, values=["Último mês", "Últimos 3 meses", "Último ano", "Todo período"])
        self.periodo_combo.grid(row=0, column=1, padx=5, pady=5)
        self.periodo_combo.current(3)
        
        ttk.Label(filter_frame, text="Agrupar por:").grid(row=0, column=2, padx=5, pady=5)
        self.agrupar_combo = ttk.Combobox(filter_frame, values=["Município", "Região", "Bioma", "Mês"])
        self.agrupar_combo.grid(row=0, column=3, padx=5, pady=5)
        self.agrupar_combo.current(0)
        
        self.gerar_stats_button = ttk.Button(filter_frame, text="Gerar Estatísticas", command=self.gerar_estatisticas)
        self.gerar_stats_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Frame para gráficos
        self.chart_frame = ttk.LabelFrame(stats_frame, text="Visualização")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área para resumo estatístico
        self.stats_summary = ttk.LabelFrame(stats_frame, text="Resumo")
        self.stats_summary.pack(fill=tk.X, pady=5)
        
        self.summary_text = tk.Text(self.stats_summary, height=6, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.summary_text.config(state=tk.DISABLED)

    def setup_config_tab(self):
        # Frame para configurações do banco de dados
        db_config_frame = ttk.LabelFrame(self.tab_config, text="Banco de Dados")
        db_config_frame.pack(fill=tk.X, pady=5)
        
        # Botão para criar tabelas
        self.create_tables_button = ttk.Button(db_config_frame, text="Criar/Verificar Tabelas", command=self.criar_tabelas)
        self.create_tables_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Botão para backup
        self.backup_button = ttk.Button(db_config_frame, text="Fazer Backup", command=self.fazer_backup)
        self.backup_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame para configurações do sistema
        sys_config_frame = ttk.LabelFrame(self.tab_config, text="Configurações do Sistema")
        sys_config_frame.pack(fill=tk.X, pady=5)
        
        # Tema
        ttk.Label(sys_config_frame, text="Tema:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.theme_combo = ttk.Combobox(sys_config_frame, values=["Claro", "Escuro"])
        self.theme_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.theme_combo.current(0)
        
        # Sobre o sistema
        about_frame = ttk.LabelFrame(self.tab_config, text="Sobre")
        about_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        about_text = "Sistema de Monitoramento de Focos de Queimada\n\n" + \
                     "Versão 1.0\n" + \
                     "Este sistema foi desenvolvido para monitorar focos de queimada detectados por satélites.\n\n" + \
                     "Funcionalidades:\n" + \
                     "- Registrar focos de queimada\n" + \
                     "- Visualizar e editar registros\n" + \
                     "- Gerar estatísticas e visualizações\n" + \
                     "- Exportar dados para análise externa"
        
        about_label = ttk.Label(about_frame, text=about_text, wraplength=500, justify=tk.LEFT)
        about_label.pack(padx=10, pady=10)

    def conectar_bd(self):
        try:
            # Obter informações de conexão
            host = self.host_entry.get()
            port = self.port_entry.get()
            dbname = self.dbname_entry.get()
            user = self.user_entry.get()
            password = self.password_entry.get()
            
            # Tentativa de conexão
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            self.cursor = self.conn.cursor()
            
            # Atualizar status
            self.status_label.config(text="Status: Conectado", foreground="green")
            messagebox.showinfo("Conexão", "Conexão estabelecida com sucesso!")
            
            # Verificar se as tabelas existem
            self.verificar_tabelas()
            
            # Carregar dados
            self.carregar_registros()
            
        except Exception as e:
            self.status_label.config(text="Status: Erro", foreground="red")
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{str(e)}")
    
    def verificar_tabelas(self):
        try:
            # Verificar se a tabela focos_de_queimada existe
            self.cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'focos_de_queimada'
                );
            """)
            
            if not self.cursor.fetchone()[0]:
                if messagebox.askyesno("Tabela não encontrada", "A tabela 'focos_de_queimada' não existe. Deseja criá-la?"):
                    self.criar_tabelas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar tabelas: {str(e)}")
    
    def criar_tabelas(self):
        try:
            if self.conn and self.cursor:
                # Criar tabela de regiões imediatas
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS regioes_imediatas (
                        codigo_regiao integer PRIMARY KEY,
                        bioma character varying(30) NOT NULL,
                        area_km2 numeric(10,2) NOT NULL,
                        nome_regiao character varying(50) NOT NULL UNIQUE,
                        clima_regiao character varying(50) NOT NULL,
                        CONSTRAINT ck_km2_positivo CHECK (area_km2 > 0)
                    );
                """)
                
                # Criar tabela de municípios
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS municipios (
                        id_municipio integer PRIMARY KEY,
                        nome_municipio character varying(50) NOT NULL UNIQUE,
                        area_km2 numeric(6,2) NOT NULL,
                        populacao integer NOT NULL,
                        codigo_regiao integer NOT NULL REFERENCES regioes_imediatas(codigo_regiao),
                        CONSTRAINT ck_area_positiva CHECK (area_km2 > 0)
                    );
                """)
                
                # Criar tabela de focos de queimada
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS focos_de_queimada (
                        id_queimada SERIAL PRIMARY KEY,
                        data_hora timestamp(0) without time zone NOT NULL,
                        latitude numeric(9,3) NOT NULL,
                        longitude numeric(9,3) NOT NULL,
                        potencia_rad real NOT NULL,
                        id_municipio integer REFERENCES municipios(id_municipio),
                        CONSTRAINT unq_foco_queimada UNIQUE (data_hora, latitude, longitude),
                        CONSTRAINT id_municipio_positivo CHECK (id_municipio > 0)
                    );
                """)
                
                # Criar tabela de satélites
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS satelites (
                        id_satelite SERIAL PRIMARY KEY,
                        nome_satelite character varying(30) NOT NULL UNIQUE,
                        agencia character varying(50) NOT NULL,
                        tipo_orbita character varying(50) NOT NULL,
                        status_operacional boolean NOT NULL,
                        CONSTRAINT ck_valor_logico CHECK (status_operacional IN (TRUE, FALSE))
                    );
                """)
                
                # Criar tabela de associação entre queimadas e satélites
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS satelite_queimada (
                        id_queimada integer REFERENCES focos_de_queimada(id_queimada),
                        id_satelite integer REFERENCES satelites(id_satelite),
                        PRIMARY KEY (id_queimada, id_satelite)
                    );
                """)
                
                # Confirmar alterações
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Tabelas criadas/verificadas com sucesso!")
            else:
                messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
                
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Erro", f"Erro ao criar tabelas: {str(e)}")
    
    def carregar_registros(self):
        try:
            if self.conn and self.cursor:
                # Limpar tabela atual
                for i in self.registros_tree.get_children():
                    self.registros_tree.delete(i)
                
                # Buscar dados com JOIN entre as tabelas
                self.cursor.execute("""
                    SELECT 
                        f.id_queimada, 
                        f.data_hora, 
                        m.nome_municipio, 
                        r.nome_regiao, 
                        r.bioma,
                        f.latitude, 
                        f.longitude, 
                        f.potencia_rad,
                        STRING_AGG(s.nome_satelite, ', ') AS satelites
                    FROM focos_de_queimada f
                    LEFT JOIN municipios m ON f.id_municipio = m.id_municipio
                    LEFT JOIN regioes_imediatas r ON m.codigo_regiao = r.codigo_regiao
                    LEFT JOIN satelite_queimada sq ON f.id_queimada = sq.id_queimada
                    LEFT JOIN satelites s ON sq.id_satelite = s.id_satelite
                    GROUP BY f.id_queimada, m.nome_municipio, r.nome_regiao, r.bioma
                    ORDER BY f.data_hora DESC;
                """)
                
                # Inserir na tabela
                registros = self.cursor.fetchall()
                for reg in registros:
                    self.registros_tree.insert('', tk.END, values=reg)
                
                self.status_bar.config(text=f"{len(registros)} focos encontrados")
            else:
                messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar registros: {str(e)}")
    
    def buscar_registros(self):
        try:
            if self.conn and self.cursor:
                # Limpar tabela atual
                for i in self.registros_tree.get_children():
                    self.registros_tree.delete(i)
                
                # Construir consulta SQL
                sql = """
                    SELECT 
                        f.id_queimada, 
                        f.data_hora, 
                        m.nome_municipio, 
                        r.nome_regiao, 
                        r.bioma,
                        f.latitude, 
                        f.longitude, 
                        f.potencia_rad,
                        STRING_AGG(s.nome_satelite, ', ') AS satelites
                    FROM focos_de_queimada f
                    LEFT JOIN municipios m ON f.id_municipio = m.id_municipio
                    LEFT JOIN regioes_imediatas r ON m.codigo_regiao = r.codigo_regiao
                    LEFT JOIN satelite_queimada sq ON f.id_queimada = sq.id_queimada
                    LEFT JOIN satelites s ON sq.id_satelite = s.id_satelite
                    WHERE 1=1
                """
                params = []
                
                # Filtro por município
                municipio = self.search_municipio_entry.get()
                if municipio:
                    sql += " AND m.nome_municipio ILIKE %s"
                    params.append(f'%{municipio}%')
                
                # Filtro por data inicial
                data_ini = self.search_data_ini.get()
                if data_ini and data_ini != "AAAA-MM-DD":
                    sql += " AND f.data_hora >= %s"
                    params.append(data_ini)
                
                # Filtro por data final
                data_fim = self.search_data_fim.get()
                if data_fim and data_fim != "AAAA-MM-DD":
                    sql += " AND f.data_hora <= %s"
                    params.append(data_fim)
                
                # Filtro por potência mínima
                potencia_min = self.search_potencia_min.get()
                if potencia_min:
                    sql += " AND f.potencia_rad >= %s"
                    params.append(float(potencia_min))
                
                # Agrupamento e ordenação
                sql += " GROUP BY f.id_queimada, m.nome_municipio, r.nome_regiao, r.bioma"
                sql += " ORDER BY f.data_hora DESC"
                
                # Executar consulta
                self.cursor.execute(sql, params)
                
                # Inserir na tabela
                registros = self.cursor.fetchall()
                for reg in registros:
                    self.registros_tree.insert('', tk.END, values=reg)
                
                self.status_bar.config(text=f"{len(registros)} focos encontrados")
            else:
                messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar registros: {str(e)}")
    
    def adicionar_registro(self):
        if not self.conn or not self.cursor:
            messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
            return
        
        # Criar janela de formulário
        add_window = tk.Toplevel(self.root)
        add_window.title("Adicionar Foco de Queimada")
        add_window.geometry("500x600")
        add_window.transient(self.root)
        add_window.focus_set()
        add_window.grab_set()
        
        # Formulário
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Data e Hora
        ttk.Label(form_frame, text="Data e Hora:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        data_hora_entry = ttk.Entry(form_frame, width=20)
        data_hora_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        data_hora_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Latitude
        ttk.Label(form_frame, text="Latitude:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        latitude_entry = ttk.Entry(form_frame, width=15)
        latitude_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Longitude
        ttk.Label(form_frame, text="Longitude:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        longitude_entry = ttk.Entry(form_frame, width=15)
        longitude_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Potência Radiante
        ttk.Label(form_frame, text="Potência Radiante:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        potencia_entry = ttk.Entry(form_frame, width=10)
        potencia_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Município
        ttk.Label(form_frame, text="Município:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Buscar municípios disponíveis
        municipios = []
        try:
            self.cursor.execute("SELECT id_municipio, nome_municipio FROM municipios ORDER BY nome_municipio")
            municipios = self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar municípios: {str(e)}")
        
        municipio_combo = ttk.Combobox(form_frame, values=[m[1] for m in municipios], state="readonly")
        municipio_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Satélites
        ttk.Label(form_frame, text="Satélite(s):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Buscar satélites disponíveis
        satelites = []
        try:
            self.cursor.execute("SELECT id_satelite, nome_satelite FROM satelites ORDER BY nome_satelite")
            satelites = self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar satélites: {str(e)}")
        
        satelite_listbox = tk.Listbox(form_frame, selectmode=tk.MULTIPLE, height=4)
        satelite_listbox.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        for sat in satelites:
            satelite_listbox.insert(tk.END, sat[1])
        
        # Função para salvar
        def salvar():
            try:
                # Validar dados
                data_hora = data_hora_entry.get()
                latitude = latitude_entry.get()
                longitude = longitude_entry.get()
                potencia = potencia_entry.get()
                
                # Verificar campos obrigatórios
                if not data_hora or not latitude or not longitude or not potencia:
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                    return
                
                # Obter ID do município selecionado
                municipio_nome = municipio_combo.get()
                id_municipio = None
                for m in municipios:
                    if m[1] == municipio_nome:
                        id_municipio = m[0]
                        break
                
                if not id_municipio:
                    messagebox.showerror("Erro", "Selecione um município válido!")
                    return
                
                # Inserir no banco de dados
                self.cursor.execute("""
                    INSERT INTO focos_de_queimada 
                    (data_hora, latitude, longitude, potencia_rad, id_municipio) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_queimada;
                """, (data_hora, float(latitude), float(longitude), float(potencia), id_municipio))
                
                id_queimada = self.cursor.fetchone()[0]
                
                # Adicionar associações com satélites
                selected_satelites = satelite_listbox.curselection()
                for idx in selected_satelites:
                    nome_satelite = satelite_listbox.get(idx)
                    id_satelite = None
                    for s in satelites:
                        if s[1] == nome_satelite:
                            id_satelite = s[0]
                            break
                    
                    if id_satelite:
                        self.cursor.execute("""
                            INSERT INTO satelite_queimada (id_queimada, id_satelite)
                            VALUES (%s, %s)
                        """, (id_queimada, id_satelite))
                
                # Confirmar alterações
                self.conn.commit()
                
                # Mostrar mensagem de sucesso
                messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
                
                # Fechar janela
                add_window.destroy()
                
                # Atualizar registros
                self.carregar_registros()
                
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Erro", f"Erro ao adicionar registro: {str(e)}")
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=add_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def editar_registro(self):
        # Verificar se há conexão
        if not self.conn or not self.cursor:
            messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
            return
            
        # Verificar se há registro selecionado
        selected = self.registros_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um registro para editar!")
            return
        
        # Obter ID do registro selecionado
        item = self.registros_tree.item(selected[0])
        registro_id = item['values'][0]
        
        # Buscar dados completos do registro
        self.cursor.execute("""
            SELECT 
                f.id_queimada, 
                f.data_hora, 
                f.latitude, 
                f.longitude, 
                f.potencia_rad,
                m.id_municipio,
                m.nome_municipio,
                STRING_AGG(s.nome_satelite, ', ') AS satelites
            FROM focos_de_queimada f
            LEFT JOIN municipios m ON f.id_municipio = m.id_municipio
            LEFT JOIN satelite_queimada sq ON f.id_queimada = sq.id_queimada
            LEFT JOIN satelites s ON sq.id_satelite = s.id_satelite
            WHERE f.id_queimada = %s
            GROUP BY f.id_queimada, m.id_municipio, m.nome_municipio
        """, (registro_id,))
        
        registro = self.cursor.fetchone()
        if not registro:
            messagebox.showerror("Erro", "Registro não encontrado!")
            return
        
        # Criar janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Registro #{registro_id}")
        edit_window.geometry("500x600")
        edit_window.transient(self.root)
        edit_window.focus_set()
        edit_window.grab_set()
        
        # Formulário
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Data e Hora
        ttk.Label(form_frame, text="Data e Hora:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        data_hora_entry = ttk.Entry(form_frame, width=20)
        data_hora_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        data_hora_entry.insert(0, registro[1])
        
        # Latitude
        ttk.Label(form_frame, text="Latitude:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        latitude_entry = ttk.Entry(form_frame, width=15)
        latitude_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        latitude_entry.insert(0, registro[2])
        
        # Longitude
        ttk.Label(form_frame, text="Longitude:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        longitude_entry = ttk.Entry(form_frame, width=15)
        longitude_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        longitude_entry.insert(0, registro[3])
        
        # Potência Radiante
        ttk.Label(form_frame, text="Potência Radiante:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        potencia_entry = ttk.Entry(form_frame, width=10)
        potencia_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        potencia_entry.insert(0, registro[4])
        
        # Município
        ttk.Label(form_frame, text="Município:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Buscar municípios disponíveis
        municipios = []
        try:
            self.cursor.execute("SELECT id_municipio, nome_municipio FROM municipios ORDER BY nome_municipio")
            municipios = self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar municípios: {str(e)}")
        
        municipio_combo = ttk.Combobox(form_frame, values=[m[1] for m in municipios], state="readonly")
        municipio_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        municipio_combo.set(registro[6])
        
        # Satélites
        ttk.Label(form_frame, text="Satélite(s):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Buscar satélites disponíveis
        satelites = []
        try:
            self.cursor.execute("SELECT id_satelite, nome_satelite FROM satelites ORDER BY nome_satelite")
            satelites = self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar satélites: {str(e)}")
        
        satelite_listbox = tk.Listbox(form_frame, selectmode=tk.MULTIPLE, height=4)
        satelite_listbox.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        for sat in satelites:
            satelite_listbox.insert(tk.END, sat[1])
            if registro[7] and sat[1] in registro[7]:
                satelite_listbox.selection_set(tk.END)
        
        # Função para salvar
        def salvar():
            try:
                # Validar dados
                data_hora = data_hora_entry.get()
                latitude = latitude_entry.get()
                longitude = longitude_entry.get()
                potencia = potencia_entry.get()
                
                # Verificar campos obrigatórios
                if not data_hora or not latitude or not longitude or not potencia:
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                    return
                
                # Obter ID do município selecionado
                municipio_nome = municipio_combo.get()
                id_municipio = None
                for m in municipios:
                    if m[1] == municipio_nome:
                        id_municipio = m[0]
                        break
                
                if not id_municipio:
                    messagebox.showerror("Erro", "Selecione um município válido!")
                    return
                
                # Atualizar no banco de dados
                self.cursor.execute("""
                    UPDATE focos_de_queimada SET
                    data_hora = %s,
                    latitude = %s,
                    longitude = %s,
                    potencia_rad = %s,
                    id_municipio = %s
                    WHERE id_queimada = %s
                """, (data_hora, float(latitude), float(longitude), float(potencia), id_municipio, registro_id))
                
                # Remover associações existentes com satélites
                self.cursor.execute("""
                    DELETE FROM satelite_queimada WHERE id_queimada = %s
                """, (registro_id,))
                
                # Adicionar novas associações com satélites
                selected_satelites = satelite_listbox.curselection()
                for idx in selected_satelites:
                    nome_satelite = satelite_listbox.get(idx)
                    id_satelite = None
                    for s in satelites:
                        if s[1] == nome_satelite:
                            id_satelite = s[0]
                            break
                    
                    if id_satelite:
                        self.cursor.execute("""
                            INSERT INTO satelite_queimada (id_queimada, id_satelite)
                            VALUES (%s, %s)
                        """, (registro_id, id_satelite))
                
                # Confirmar alterações
                self.conn.commit()
                
                # Mostrar mensagem de sucesso
                messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
                
                # Fechar janela
                edit_window.destroy()
                
                # Atualizar registros
                self.carregar_registros()
                
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Erro", f"Erro ao atualizar registro: {str(e)}")
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)

    def excluir_registro(self):
        # Verificar se há conexão
        if not self.conn or not self.cursor:
            messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
            return
            
        # Verificar se há registro selecionado
        selected = self.registros_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir!")
            return
        
        # Obter ID do registro selecionado
        item = self.registros_tree.item(selected[0])
        registro_id = item['values'][0]
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o registro #{registro_id}?"):
            try:
                # Excluir registro
                self.cursor.execute("DELETE FROM focos_de_queimada WHERE id_queimada = %s", (registro_id,))
                self.conn.commit()
                
                # Atualizar lista de registros
                self.carregar_registros()
                
                messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Erro", f"Erro ao excluir registro: {str(e)}")
    
    def ver_detalhes(self, event):
        # Verificar se há conexão
        if not self.conn or not self.cursor:
            messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
            return
            
        # Obter item selecionado
        item = self.registros_tree.selection()
        if not item:
            return
            
        registro_id = self.registros_tree.item(item[0])['values'][0]
        
        # Buscar dados completos do registro
        self.cursor.execute("""
            SELECT 
                f.id_queimada, 
                f.data_hora, 
                f.latitude, 
                f.longitude, 
                f.potencia_rad,
                m.nome_municipio,
                r.nome_regiao,
                r.bioma,
                r.clima_regiao,
                STRING_AGG(s.nome_satelite, ', ') AS satelites
            FROM focos_de_queimada f
            LEFT JOIN municipios m ON f.id_municipio = m.id_municipio
            LEFT JOIN regioes_imediatas r ON m.codigo_regiao = r.codigo_regiao
            LEFT JOIN satelite_queimada sq ON f.id_queimada = sq.id_queimada
            LEFT JOIN satelites s ON sq.id_satelite = s.id_satelite
            WHERE f.id_queimada = %s
            GROUP BY f.id_queimada, m.nome_municipio, r.nome_regiao, r.bioma, r.clima_regiao
        """, (registro_id,))
        
        registro = self.cursor.fetchone()
        if not registro:
            messagebox.showerror("Erro", "Registro não encontrado!")
            return
        
        # Criar janela de detalhes
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detalhes do Registro #{registro_id}")
        detail_window.geometry("500x500")
        detail_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(detail_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Texto com informações detalhadas
        info_text = tk.Text(frame, wrap=tk.WORD, height=20)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # Adicionar informações
        info_text.insert(tk.END, f"ID: {registro[0]}\n")
        info_text.insert(tk.END, f"Data e Hora: {registro[1]}\n")
        info_text.insert(tk.END, f"Latitude: {registro[2]}\n")
        info_text.insert(tk.END, f"Longitude: {registro[3]}\n")
        info_text.insert(tk.END, f"Potência Radiante: {registro[4]}\n")
        info_text.insert(tk.END, f"Município: {registro[5]}\n")
        info_text.insert(tk.END, f"Região: {registro[6]}\n")
        info_text.insert(tk.END, f"Bioma: {registro[7]}\n")
        info_text.insert(tk.END, f"Clima: {registro[8]}\n")
        info_text.insert(tk.END, f"Satélites: {registro[9] if registro[9] else 'Nenhum'}\n")
        
        # Desabilitar edição
        info_text.config(state=tk.DISABLED)
        
        # Botão de fechar
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Fechar", command=detail_window.destroy).pack()
    
    def show_context_menu(self, event):
        # Verificar se há item selecionado
        item = self.registros_tree.identify_row(event.y)
        if not item:
            return
            
        # Selecionar o item
        self.registros_tree.selection_set(item)
        
        # Criar menu de contexto
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Ver Detalhes", command=self.ver_detalhes)
        menu.add_command(label="Editar", command=self.editar_registro)
        menu.add_command(label="Excluir", command=self.excluir_registro)
        
        # Mostrar menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def exportar_dados(self):
        try:
            if not self.conn or not self.cursor:
                messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
                return
                
            # Obter todos os registros
            self.cursor.execute("""
                SELECT 
                    f.id_queimada, 
                    f.data_hora, 
                    m.nome_municipio, 
                    r.nome_regiao, 
                    r.bioma,
                    f.latitude, 
                    f.longitude, 
                    f.potencia_rad,
                    STRING_AGG(s.nome_satelite, ', ') AS satelites
                FROM focos_de_queimada f
                LEFT JOIN municipios m ON f.id_municipio = m.id_municipio
                LEFT JOIN regioes_imediatas r ON m.codigo_regiao = r.codigo_regiao
                LEFT JOIN satelite_queimada sq ON f.id_queimada = sq.id_queimada
                LEFT JOIN satelites s ON sq.id_satelite = s.id_satelite
                GROUP BY f.id_queimada, m.nome_municipio, r.nome_regiao, r.bioma
                ORDER BY f.data_hora DESC
            """)
            
            registros = self.cursor.fetchall()
            
            if not registros:
                messagebox.showwarning("Aviso", "Nenhum registro encontrado para exportar!")
                return
                
            # Criar DataFrame
            df = pd.DataFrame(registros, columns=[
                'ID', 'Data/Hora', 'Município', 'Região', 'Bioma', 
                'Latitude', 'Longitude', 'Potência Radiante', 'Satélites'
            ])
            
            # Perguntar onde salvar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")],
                title="Salvar como"
            )
            
            if not file_path:
                return
                
            # Exportar conforme extensão
            if file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            else:
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                
            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")
    
    def gerar_estatisticas(self):
        try:
            if not self.conn or not self.cursor:
                messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
                return
                
            # Limpar frame de gráficos
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
                
            # Limpar resumo
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.config(state=tk.DISABLED)
            
            # Obter parâmetros
            periodo = self.periodo_combo.get()
            agrupar_por = self.agrupar_combo.get()
            
            # Construir consulta SQL
            sql = "SELECT "
            
            # Definir agrupamento
            if agrupar_por == "Mês":
                sql += "TO_CHAR(f.data_hora, 'YYYY-MM') AS periodo, "
                group_by = "TO_CHAR(f.data_hora, 'YYYY-MM')"
            elif agrupar_por == "Município":
                sql += "m.nome_municipio AS periodo, "
                group_by = "m.nome_municipio"
            elif agrupar_por == "Região":
                sql += "r.nome_regiao AS periodo, "
                group_by = "r.nome_regiao"
            elif agrupar_por == "Bioma":
                sql += "r.bioma AS periodo, "
                group_by = "r.bioma"
                
            sql += f"COUNT(*) AS total, AVG(f.potencia_rad) AS potencia_media FROM focos_de_queimada f "
            sql += "LEFT JOIN municipios m ON f.id_municipio = m.id_municipio "
            sql += "LEFT JOIN regioes_imediatas r ON m.codigo_regiao = r.codigo_regiao "
            
            # Definir período
            if periodo == "Último mês":
                sql += "WHERE f.data_hora >= CURRENT_DATE - INTERVAL '1 month' "
            elif periodo == "Últimos 3 meses":
                sql += "WHERE f.data_hora >= CURRENT_DATE - INTERVAL '3 months' "
            elif periodo == "Último ano":
                sql += "WHERE f.data_hora >= CURRENT_DATE - INTERVAL '1 year' "
                
            sql += f"GROUP BY {group_by} ORDER BY total DESC"
            
            # Executar consulta
            self.cursor.execute(sql)
            dados = self.cursor.fetchall()
            
            if not dados:
                messagebox.showwarning("Aviso", "Nenhum dado encontrado para os filtros selecionados!")
                return
                
            # Criar DataFrame
            df = pd.DataFrame(dados, columns=['Periodo', 'Total', 'Potencia_Media'])
            
            # Gerar resumo estatístico
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.insert(tk.END, f"Resumo Estatístico ({periodo} - Agrupado por {agrupar_por})\n\n")
            self.summary_text.insert(tk.END, f"Total de focos: {df['Total'].sum()}\n")
            self.summary_text.insert(tk.END, f"Média de potência radiante: {df['Potencia_Media'].mean():.2f}\n\n")
            self.summary_text.insert(tk.END, "Top 5 ocorrências:\n")
            
            for i, row in df.head().iterrows():
                self.summary_text.insert(tk.END, f"- {row['Periodo']}: {row['Total']} focos (potência média: {row['Potencia_Media']:.2f})\n")
                
            self.summary_text.config(state=tk.DISABLED)
            
            # Criar gráfico
            fig = Figure(figsize=(8, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            if agrupar_por == "Mês":
                # Ordenar por data
                df = df.sort_values('Periodo')
                ax.bar(df['Periodo'], df['Total'])
                ax.set_xlabel('Mês')
                ax.set_xticklabels(df['Periodo'], rotation=45)
            else:
                ax.bar(df['Periodo'], df['Total'])
                ax.set_xlabel(agrupar_por)
                
            ax.set_ylabel('Número de Focos')
            ax.set_title(f'Focos de Queimada por {agrupar_por}')
            
            # Adicionar gráfico ao Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar estatísticas: {str(e)}")
    
    def fazer_backup(self):
        try:
            if not self.conn or not self.cursor:
                messagebox.showerror("Erro", "Não há conexão ativa com o banco de dados!")
                return
                
            # Perguntar onde salvar o backup
            file_path = filedialog.asksaveasfilename(
                defaultextension=".sql",
                filetypes=[("SQL", "*.sql")],
                title="Salvar Backup como"
            )
            
            if not file_path:
                return
                
            # Executar pg_dump (requer que o pg_dump esteja no PATH do sistema)
            dbname = self.dbname_entry.get()
            user = self.user_entry.get()
            password = self.password_entry.get()
            host = self.host_entry.get()
            port = self.port_entry.get()
            
            # Comando pg_dump
            cmd = f'pg_dump -h {host} -p {port} -U {user} -F p -b -v -f "{file_path}" {dbname}'
            
            # Definir variável de ambiente para a senha
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            # Executar comando
            result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Sucesso", f"Backup criado com sucesso em:\n{file_path}")
            else:
                messagebox.showerror("Erro", f"Falha ao criar backup:\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaQueimadas(root)
    root.mainloop()
