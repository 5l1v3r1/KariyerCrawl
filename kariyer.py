# @ykslkrkci tarafından Persona Non Grata için hazırlanmıştır.
# @raifpy Sonsuz teşekkürlerimi sunarım.
from bs4 import BeautifulSoup as bsoup
import requests
import lxml
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AnaPencere(object):
    def setupUi(self, AnaPencere):
        AnaPencere.setObjectName("AnaPencere")
        AnaPencere.resize(504, 353)
        self.centralwidget = QtWidgets.QWidget(AnaPencere)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.adresVer = QtWidgets.QLineEdit(self.centralwidget)
        self.adresVer.setObjectName("adresVer")
        self.adresVer.setPlaceholderText("Kariyer'de aranacak anahtar kelime")
        self.verticalLayout.addWidget(self.adresVer)
        self.veriCek = QtWidgets.QPushButton(self.centralwidget)
        self.veriCek.setObjectName("veriCek")
        self.verticalLayout.addWidget(self.veriCek)
        self.gelenIlanlar = QtWidgets.QTextEdit(self.centralwidget)
        self.gelenIlanlar.setObjectName("gelenIlanlar")
        self.verticalLayout.addWidget(self.gelenIlanlar)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        AnaPencere.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AnaPencere)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 504, 25))
        self.menubar.setObjectName("menubar")
        self.menuAyarlar = QtWidgets.QMenu(self.menubar)
        self.menuAyarlar.setObjectName("menuAyarlar")
        self.menuDil = QtWidgets.QMenu(self.menuAyarlar)
        self.menuDil.setObjectName("menuDil")
        self.menuHakk_m_zda = QtWidgets.QMenu(self.menubar)
        self.menuHakk_m_zda.setObjectName("menuHakk_m_zda")
        AnaPencere.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AnaPencere)
        self.statusbar.setObjectName("statusbar")
        AnaPencere.setStatusBar(self.statusbar)
        self.actionT_rk_e = QtWidgets.QAction(AnaPencere)
        self.actionT_rk_e.setObjectName("actionT_rk_e")
        self.actionEnglish = QtWidgets.QAction(AnaPencere)
        self.actionEnglish.setObjectName("actionEnglish")
        self.menuDil.addAction(self.actionT_rk_e)
        self.menuDil.addAction(self.actionEnglish)
        self.menuAyarlar.addAction(self.menuDil.menuAction())
        self.menubar.addAction(self.menuAyarlar.menuAction())
        self.menubar.addAction(self.menuHakk_m_zda.menuAction())

        self.veriCek.clicked.connect(self.VeriverBabus)

        self.retranslateUi(AnaPencere)
        QtCore.QMetaObject.connectSlotsByName(AnaPencere)

    def VeriverBabus(self):
        if self.adresVer.text() == "":
            self.adresVer.setPlaceholderText("Meslek dalı yazmalısınız..")
        else:
            self.adres = self.adresVer.text()
            if len(self.adres.split()) > 1:
                self.adres = "-".join(self.adres.split())
            print("Aranan : ",self.adres)
            link = "https://www.kariyer.net/is-ilanlari/" + self.adres
            header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
            ilan_listesi = []
            kaynak_isle = requests.get(link, headers=header).text
            kod = bsoup(kaynak_isle, "lxml")

            for a in kod.find_all("a"):
                try:
                    a["href"]
                except KeyError:
                    pass
                else:
                    if a["href"].startswith("/is-ilani/"):
                        # self.gelenIlanlar.append("İş ilanı bulundu: "+ "https://kariyer.net"+ a["href"])
                        print("https://www.kariyer.net" + a["href"])
                        ilan_listesi.append("https://www.kariyer.net" + a["href"])
            if ilan_listesi:
                for link in ilan_listesi:
                    self.gelenIlanlar.append(link)
                    self.gelenIlanlar.append("")
                    kod = bsoup(requests.get(link, headers=header).text, "lxml")
                    for konu in kod.find_all("div", attrs={"class": "genel-nitelikler"}):
                        for i in konu.find_all("li"):
                            self.gelenIlanlar.append(i.text)
                    self.gelenIlanlar.append("")
                    self.gelenIlanlar.append(
                        "*******************************************************************************************************************************************************************************************\n\n")
                    self.gelenIlanlar.repaint()
            else:
                self.gelenIlanlar.append("Bilgi Bulunamadı :(")


    def retranslateUi(self, AnaPencere):
        _translate = QtCore.QCoreApplication.translate
        AnaPencere.setWindowTitle(_translate("AnaPencere", "Kariyer.Net İş İlanı Crawler"))
        self.veriCek.setText(_translate("AnaPencere", "İlanları Ver"))
        self.menuAyarlar.setTitle(_translate("AnaPencere", "Ayarlar "))
        self.menuDil.setTitle(_translate("AnaPencere", "Dil"))
        self.menuHakk_m_zda.setTitle(_translate("AnaPencere", "Hakkımızda"))
        self.actionT_rk_e.setText(_translate("AnaPencere", "Türkçe"))
        self.actionEnglish.setText(_translate("AnaPencere", "English"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AnaPencere = QtWidgets.QMainWindow()
    ui = Ui_AnaPencere()
    ui.setupUi(AnaPencere)
    AnaPencere.show()
    sys.exit(app.exec_())
