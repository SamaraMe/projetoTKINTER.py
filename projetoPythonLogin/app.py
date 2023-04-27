'''importação do tkinter/recursos para a interface gráfica'''
from tkinter import END, PhotoImage
import customtkinter as ctk
import sqlite3
from tkinter import messagebox

'''Criação da classe backend responsavel pela lógica dos dados e o processamento de dados - será também instanciada na classe App abaixo, esta classe herda os componentes da classe App as funções dessa classse está abaixo do frontend'''
class BackEnd():
    '''Função para afzer a conexão com o banco de dados'''
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema de Login.db")
        self.cursor = self.conn.cursor() # é um ponto de entrada - ajuda a percorrer
        print("Banco de dados conectado.")

    '''Função que desconecta o banco de dados'''
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado.")

    '''Criação das tabelas'''
    def cria_tabela(self):
        self.conecta_db()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMAY KEY AUTO_INCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso")
        self.desconecta_db()
    
    '''Criação da função cadastrar usuário'''
    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        self.conecta_db()

        self.cursor.execute('''
            INSERT INTO Usuarios (Username, Email, Senha, Confirma_senha)
            VALUES (?, ?, ?, ?)''', (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))

        '''Verificção de dados'''
        try:
            if (self.username_cadastro =="" or self.email_cadastro =="" or self.senha_cadastro =="" or self.confirma_senha_cadastro ==""):
                 messagebox.showerror(title="Sistema de Login", message="ERRO!\nPor favor preeencha todos os campos")

            elif (len(self.username_cadastro) < 4):
                 messagebox.showwarning(title="Sistema de Login", message="O nome de usuário de ter pelo menos 4 caracteres.")

            elif (len(self.senha_cadastro) < 4):
                 messagebox.showwarning(title="Sistema de Login", message="A senha deve ter pelo menos 4 caracteres.")

            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de Login", message="ERRO!\nAs senhas não estão corretas,coloque-as iguais")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistemas de Login", message=f"Parabéns {self.username_cadastro}\nOs seus dados foram cadastrados.")
                self.desconecta_db()
                #self.limpa_entry_cadastro() #<-- essa função não está retornando por isso os dados na tela de cadastro não somem.
        except:
            messagebox.showerror(title="Sistema de Login", message="Erro no processamento do seu cadastro\nPor favor tente novamente!")
            self.desconecta_db()

    '''Função verificação de Login'''
    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.conecta_db()
        
        '''verificação do usuário no banco - selecionar dentro da tabela usuarios onde username é igual a username e senha é igual a senha'''
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha=?)""", (self.username_login, self.senha_login))

        '''percorrer na tabela para ver se realmente têm os dados'''
        self.verifica_dados = self.cursor.fetchone() # percorrendo na tabela usuarios - fetchone

        try:
            if (self.username_login=="" or self.senha_login==""):
                messagebox.showwarning(title="Sistema de Login", message="Por favor preencha todos os campos") 
                
            elif (self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistema de login", message=f"Parabéns { self.username_login}\nLogin feito com sucesso!")
                self.desconecta_db()
                #self.limpa_entry_login() <-- infelizmente essa função não está retornando, por isso 
                # está comentada e não some os dados na tela de login.

        except:
            messagebox.showerror(title="Sistema de Login", message="ERRO!\nDados não encontrados no sistema.\nPor favor verifique os seus dados ou cadastre-se no nosso sistema.")
            self.desconecta_db()
        

# FRONTEND  
'''classe App que chama a tela tkinter/ o super quer dizer que esse init é a função mais pesada na classe'''
class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.config_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()
        

    '''Configuracao da janela principal'''
    def config_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False)

    '''Funcao tela de login e trabalahndo com imagens'''
    def tela_de_login(self):
        '''Removendo a tela de cadastro'''

        self.img= PhotoImage (file="img2.1png.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        '''Título da plataforma, aqui está sendo criado o titulo da tela de login'''
        self.title =ctk.CTkLabel(self, text="Faça o seu Login ou Cadastre-se\nna nossa plataforma para acessar\nos nossos serviços.",font=("Dosis bold", 15))
        self.title.grid(row=0, column=0, pady=0, padx=10)

        '''Criação do Frame formulário de login, aqui esta sendo criado o frame para a tela de login(divisao da tela)'''
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        '''Criação de widgets dentro do frame - formulario de login'''
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Dosis bold", 23))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        '''Criação do nome do usuario'''
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuário...", font=("Dosis", 16))
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)

        '''Criação da senha'''
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha do usuário...", font=("Dosis", 16),show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)


        '''Criação do checkbox ver senha(opção)'''
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", font=("Dosis bold", 13),corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        '''Criação do botão'''
        self.btn_login = ctk.CTkButton(self.frame_login, width=300,text="Fazer Login...".upper(), font=("Roboto", 15),corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        '''Criação do span'''
        self.span = ctk.CTkLabel(self.frame_login, text="Se não tem uma conta, clique no botão abaixo para poder se\ncadastrar no nosso sistema.", font=("Dosis ", 12))
        self.span.grid(row=5, column=0, padx=10, pady=10)

        '''Criação do botão cadastro, o atributo command=tela_de_cadastro chama a função "tela de cadastro"
           pois quando clicado o botão de cadastrar a tela de cadastro aparecerá
        '''
        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green",hover_color="#050",text="Fazer Cadastro...".upper(), font=("Roboto", 15),corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, padx=10, pady=10)

    '''Criação da função tela de cadastro '''
    def tela_de_cadastro(self):
        '''Remoção do formulário de Login para poder chamar a tela de cadastro
           o place serve para poder posicionar
        '''
        self.frame_login.place_forget()
        '''Criação da frame de formulário de cadastro'''

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

        '''Criando o título'''
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu Login", font=("Dosis bold", 23))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)


        '''Criar os widgets da tela de cadastro - widgets é um elemento gráfico que é exibido em uma janela de aplicativo, eles são os blocos de construção básicos de uma interface gráfica do usuário
        '''
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário...", font=("Dosis", 16))
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="E-mail do usuário...", font=("Dosis", 16))
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha do usuário...", font=("Dosis", 16),show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirma senha do usuário...", font=("Dosis", 16), show="*")
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=5)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Dosis bold", 13),corner_radius=20)
        self.ver_senha.grid(row=5, column=0, padx=10)

        '''Criação dos botões de cadastrar usuario e voltar'''
        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green",hover_color="#050",text="Fazer Cadastro...".upper(), font=("Roboto", 15),corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, padx=10, pady=5)

        '''Criação dos botões'''
        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300,text="Voltar ao Login".upper(), font=("Roboto", 15),corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, padx=10, pady=10)

'''Função que limpa os elementos-dados'''
def limpa_entry_cadastro(self):
    self.username_cadastro_entry.delete(0, END)
    self.email_cadastro_entry.delete(0, END)
    self.senha_cadastro_entry.delete(0, END)
    self.confirma_senha_entry.delete(0, END)

'''END é uma função do TKinter'''
def limpa_entry_login(self):
    self.username_login_entry.delete(0,END)
    self.senha_login_entry.delete(0,END)




        



'''chamar a classe App, ou seja os elemento que serão executados serão dessa classe
   o mainloop serve para executar a janela
'''
if __name__ == "__main__":
    app = App()
    app.mainloop()