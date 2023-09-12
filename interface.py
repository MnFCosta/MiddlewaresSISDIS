import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from confluent_kafka import Producer, Consumer, KafkaError
import uuid

grupos = {'1': "mensagens_topic",
}

usuarios = {
    '1': ['manoel', 'senha123'],
    '2': ['pedro', 'senha456'],
}


# Configurações do produtor Kafka
config = {
    'bootstrap.servers': 'localhost:9092',  # Endereço do servidor Kafka
}

id_grupo_kafka = f'teste-{str(uuid.uuid4())}'

# Configurações do consumidor Kafka
config_consumidor = {
    'bootstrap.servers': 'localhost:9092',  # Kafka Broker
    'group.id': id_grupo_kafka,  # Unique Consumer Group ID for each run
    'auto.offset.reset': 'earliest',  # Start from the beginning of the topic
    'isolation.level': 'read_committed',
}


class TelaGrupo(QWidget):
    def __init__(self, grupo, usuario_logado):
        super().__init__()
        self.grupo = grupo
        self.usuario_logado = usuario_logado
        self.historico_mensagens = [] 

        self.historico_mensagens = self.msgs()

        self.initUI()

    
    def msgs(self):
        mensagens = []

        id_grupo_kafka = f'teste-{str(uuid.uuid4())}'
        # Configurações do consumidor Kafka
        config_consumidor = {
            'bootstrap.servers': 'localhost:9092',  # Kafka Broker
            'group.id': id_grupo_kafka,  # Id de grupo do consumidor
            'auto.offset.reset': 'earliest',  # Inicie a consumir mensagens do inicio do topico
            'isolation.level': 'read_committed',
        }

        consumer = Consumer(config_consumidor)
        consumer.subscribe([self.grupo])
        try:
            while True:
                msg = consumer.poll(1.0)  

                if msg is None:
                    # Se não houver mais mensagens sendo consumidas, encerre o loop
                    break

                if msg.error():
                    print(f'Erro ao buscar por mensagens: {msg.error()}')
                else:
                    mensagem = msg.value().decode("utf-8")
                    mensagens.append(mensagem)

        except KeyboardInterrupt:
            pass
        finally:
            return mensagens

    def initUI(self):
        # Widgets
        self.label_grupo = QLabel(f'Bem Vindo ao grupo {self.grupo} {self.usuario_logado}!')
        self.mensagens = QLabel('Mensagens:', self)
        self.mensagens_grupo = QLabel(self, text='\n'.join(self.historico_mensagens))
        self.mensagem = QLineEdit()
        self.botao_mandar = QPushButton('Enviar')
        self.botao_cancelar = QPushButton('Cancelar')

        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_grupo)
        layout.addWidget(self.mensagens)
        layout.addWidget(self.mensagens_grupo)
        layout.addWidget(self.mensagem)
        layout.addWidget(self.botao_mandar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        # Configurar eventos
        self.botao_cancelar.clicked.connect(self.close)
        self.botao_mandar.clicked.connect(self.mandar_mensagem)

        self.setWindowTitle('Tela de Grupo')
        self.setGeometry(100, 100, 300, 200)

        # Configurar o consumidor Kafka em uma thread separada
        self.consumer_thread = KafkaConsumerThread(grupo=self.grupo)
        self.consumer_thread.start()

        self.consumer_thread.message_received.connect(self.atualizar_mensagens)
    
    def atualizar_mensagens(self, mensagem):

        texto = self.mensagens_grupo.text()
        novo_texto = f"{texto}\n{mensagem}"
        self.mensagens_grupo.setText(novo_texto)

    def mandar_mensagem(self):
        topico = self.grupo
        mensagem = f'{self.usuario_logado}: {self.mensagem.text()}'

        producer = Producer(config)
        producer.produce(topico, key=None, value=mensagem)
        producer.flush()

        self.mensagem.clear()


class KafkaConsumerThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, grupo, parent=None,):
        super().__init__(parent)
        self.grupo = grupo

    def run(self):
        consumer = Consumer(config_consumidor)
        consumer.subscribe([self.grupo])

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print('Erro no Kafka: {}'.format(msg.error()))

            message = msg.value().decode('utf-8')  # Decodifica os bytes para uma string
            self.message_received.emit(message)


class TelaPrincipal(QWidget):
    def __init__(self, usuario_logado):
        super().__init__()
        self.usuario_logado = usuario_logado

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
        self.tela_grupo = TelaGrupo(grupo, self.usuario_logado)
        self.tela_grupo.show()
        self.close()


class TelaLogin(QWidget):
    def __init__(self,):
        super().__init__()
        self.usuario_logado = ''

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

        for key, values in usuarios.items():

            if usuario == values[0] and senha == values[1]:
                self.usuario_logado = values[0]
                print(f'Login bem-sucedido, seja bem vindo {self.usuario_logado}!')
                self.abrir_tela_principal()
            else:
                print('Login falhou')

    def abrir_tela_principal(self):
        self.tela_principal = TelaPrincipal(self.usuario_logado)
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
