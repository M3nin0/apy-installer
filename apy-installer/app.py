import sys
import subprocess

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication

class Install(object):
    '''
        Classe resposável em realizar as instalações
    '''
    def __init__(self, window):
        self.window = window
        self.password , status = QInputDialog.getText(window, 'Senha', 'Insira sua senha')
        self.commands = {
                'update': 'sudo -S apt-get update -y',

                'Chrome': 'sudo -S apt-get install libxss1 libappindicator1 libindicator7 -f -y \
                && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb\
                && sudo dpkg -i google-chrome*.deb',

                'Opera': 'sudo -S apt-get install apt-transport-https -f -y && \
                wget http://deb.opera.com/opera/pool/non-free/o/opera-stable/opera-stable_43.0.2442.806_amd64.deb -O "opera" && \
	            sudo dpkg -i opera && sudo apt-get install -f -y',

                'Atom': 'sudo -S wget https://atom.io/download/deb -O atom && sudo dpkg -i atom',

                'Vim': 'sudo -S apt-get install vim -f -y ',

                'Spotify': 'sudo -S apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0DF731E45CE24F27EEEB1450EFDC8610341D9410 && \
                echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list && \
                sudo apt-get update && sudo apt-get install spotify-client -f -y',

                'VLC': 'sudo -S apt-get install vlc -f -y',

                'VirtualBox': 'sudo -S wget http://download.virtualbox.org/virtualbox/5.2.4/virtualbox-5.2_5.2.4-119785~Debian~jessie_amd64.deb -O virtualbox \
                sudo dpkg -i virtualbox',

                'Dropbox': 'sudo -S wget https://www.dropbox.com/download?dl=packages/ubuntu/dropbox_2015.10.28_amd64.deb -O dropbox && \
                sudo dpkg -i dropbox',

                'JDK': 'sudo -S apt-get install default-jre && sudo apt-get install default-jdk'
            }
        command = "echo " + "\""+ self.password +"\"" + " | " + self.commands['update']

        QMessageBox.information(window, 'Atualização',
                            'Os pacotes estão sendo atualizados')

        p = subprocess.Popen(command, shell=True)
        # Espera o processo finalizar para continuar o programa
        p.wait()
        QMessageBox.information(window, 'Status', 'Atualização concluída!')

    def install_selected(self):
        '''
            Método para instalar os programas selecionados pelo usuário
        '''
        erros = 0
        for checks in self.window.findChildren(QCheckBox):
            if checks.isChecked():
                command = "echo " + "\""+ self.password +"\"" + " | " + self.commands[checks.text()]
                # Executa o comando criado acima
                try:
                    p = subprocess.Popen(command, shell=True)
                    p.wait()
                except BaseException as e:
                    erros += 1
                    QMessageBox.information(self.window, 'Erro', 'Erro ao tentar instalar ' + checks.text() + '\n' + e)
                    continue

        QMessageBox.information(self.window, 'Sucesso', 'Os programas selecionados foram instalados\nErros: ' + str(erros))

    def install_all(self):
        '''
            Método para instalar todos os programas de uma única vez
        '''
        erros = 0
        for key in self.commands:
            command = "echo " + "\""+ self.password +"\"" + " | " + self.commands[key]
            try:
                p = subprocess.Popen(command, shell=True)
                p.wait()
            except BaseException as e:
                erros += 1

        QMessageBox.information(self.window, 'Sucesso', 'Todos os programas foram instalados\nErros: ' + str(erros))

class App(object):
    def __init__(self):
        '''
            Método que inicializa e configura a interface
        '''
        self.app = QApplication(sys.argv)
        self.window = loadUi('interface/menu.ui')

        self.install = Install(self.window)
        self.__config_buttons()

        self.window.show()
        sys.exit(self.app.exec_())
    def __config_buttons(self):
        '''
            Método para configurar os botões e as funções que serão chamadas
        '''
        self.window.btn_install.clicked.connect(self.install.install_selected)
        self.window.btn_install_all.clicked.connect(self.install.install_all)

if __name__ == '__main__':
    App()
