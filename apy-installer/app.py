import sys
import subprocess

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication

class Install(object):
    def __init__(self, window):
        self.window = window
        self.password , status = QInputDialog.getText(window, 'Senha', 'Insira sua senha')
        self.commands = {
                'update': 'sudo -S apt-get update',
                'Chrome': 'sudo -S apt-get install libxss1 libappindicator1 libindicator7 \
                && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb\
                && sudo dpkg -i google-chrome*.deb'
            }
    def install_selected(self):
        '''
            Método para instalar os programas selecionados pelo usuário
        '''
        command = "echo " + "\""+ self.password +"\"" + " | " + self.commands['update']
        subprocess.Popen(command, shell=True, stdout=open('/dev/null', 'w'))
        for checks in self.window.findChildren(QCheckBox):
            if checks.isChecked():
                command = "echo " + "\""+ self.password +"\"" + " | " + self.commands[checks.text()]
                subprocess.Popen(command, shell=True, stdout=open('/dev/null/', 'w'))

    def install_all():
        pass

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
