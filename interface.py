import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

grupos = {'1': "Grupo Brabíssimo",
          '2': "Grupo dos Amigos",
}

class TelaGrupo(QWidget):
    def __init__(self,grupo):
        super().__init__()
        self.grupo = grupo

        self.initUI()

    def initUI(self):
        # Widgets
        self.label_grupo = QLabel(f'Bem Vindo ao grupo {self.grupo}')
        self.botao_cancelar = QPushButton('Cancelar')

        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_grupo)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        # Configurar eventos
        self.botao_cancelar.clicked.connect(self.close)

        self.setWindowTitle('Tela de Grupo')
        self.setGeometry(100, 100, 300, 200)


class TelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Widgets
        self.label_usuario = QLabel(f'Qual grupo deseja entrar?')
        self.input_grupo = QLineEdit()
        self.botao_entrar = QPushButton('Entrar')
        self.botao_cancelar = QPushButton('Cancelar')

        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_grupo)
        layout.addWidget(self.botao_entrar)
        layout.addWidget(self.botao_cancelar)
        

        self.setLayout(layout)

        # Configurar eventos
        self.botao_entrar.clicked.connect(self.entrar_grupo)
        self.botao_cancelar.clicked.connect(self.close)

        self.setWindowTitle('Tela Principal')
        self.setGeometry(100, 100, 300, 200)
    
    def entrar_grupo(self):
        grupo = self.input_grupo.text()


        self.abrir_tela_grupo(grupos[f"{grupo}"])

        
    def abrir_tela_grupo(self, grupo):
        self.tela_grupo = TelaGrupo(grupo)
        self.tela_grupo.show()
        self.close()


class TelaLogin(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Widgets
        self.label_usuario = QLabel('Usuário:', self)
        self.label_senha = QLabel('Senha:', self)
        self.input_usuario = QLineEdit(self)
        self.input_senha = QLineEdit(self)
        self.botao_login = QPushButton('Login', self)
        self.botao_cancelar = QPushButton('X', self)

        #Campo input_senha é um campo de senha  
        self.input_senha.setEchoMode(QLineEdit.Password)

        # Posicionar os widgets na tela
        self.label_usuario.setGeometry(300, 200, 100, 30)  # X, Y, Width, Height
        self.input_usuario.setGeometry(300, 230, 200, 30)
        self.label_senha.setGeometry(300, 270, 100, 30)
        self.input_senha.setGeometry(300, 300, 200, 30)
        self.botao_login.setGeometry(350, 350, 100, 30)
        self.botao_cancelar.setGeometry(750, 10, 40, 30)

        # Configurar os eventos dos botões
        self.botao_login.clicked.connect(self.fazer_login)
        self.botao_cancelar.clicked.connect(self.close)

        self.setWindowTitle('Tela de Login')
        self.setGeometry(450, 100, 800, 600)

    def fazer_login(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()

        # Autenticação porca só pra testar
        if usuario == 'usuario' and senha == 'senha':
            print('Login bem-sucedido')
            # Abra a tela principal após o login bem-sucedido
            self.abrir_tela_principal()
        else:
            print('Login falhou')

    def abrir_tela_principal(self):
        self.tela_principal = TelaPrincipal()
        self.tela_principal.show()
        self.close()


if __name__ == '__main__':
    #Cria uma instancia da aplicação PyQt, necessária para configurar a interface gráfica e o loop de eventos
    app = QApplication(sys.argv)
    #Cria uma instância da classe TelaLogin, que representa a tela de login da aplicação
    tela_login = TelaLogin()
    #Mostra a tela de login
    tela_login.show()
    #app.exec inicia o loop de eventos da aplicação, que aguarda por cliques de mouse e pressionamentos de teclas por exemplo
    #sys.exit termina a aplicação quando tem um retorno de 0, ou seja, quando app.exec_() retornar 0, a aplicação será terminada
    sys.exit(app.exec_())
