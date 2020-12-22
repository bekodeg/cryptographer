import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
import algorithm
import text
import bin_algoritm


class Cryptographer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cryptographer.ui', self)  # Загружаем дизайн

        self.key = None
        self.lib_update()
        self.chip = self.alg_t[0]
        self.info_p.setText(str(self.chip))
        self.id_mem = 0

        self.txt_mode.clicked.connect(self.mode_changed)
        self.bin_mode.clicked.connect(self.mode_changed)
        self.alg_txt.activated.connect(self.move)
        self.alg_bin.activated.connect(self.move)
        self.lib_btn.clicked.connect(self.lib_change)

        self.encrypt.clicked.connect(self.encryption)
        self.decrypt.clicked.connect(self.decryption)

        self.reverse_btn.clicked.connect(self.reverse)
        self.open_btn.clicked.connect(self.open)
        self.save_file_btn.clicked.connect(self.save_txt)

        self.import_key_btn.clicked.connect(self.import_key)
        self.generator_btn.clicked.connect(self.generator)
        self.save_key_btn.clicked.connect(self.save_key)

        self.key_line.editingFinished.connect(self.check_key)

    def move(self, index):
        if self.txt_mode.isChecked():
            self.chip = self.alg_t[index]
        else:
            self.chip = self.alg_b[index]
        self.info_p.setText(str(self.chip))
        self.check_key()

    def mode_changed(self):
        state = self.txt_mode.isChecked()
        self.alg_txt.setEnabled(state)
        self.alg_bin.setEnabled(not state)
        if state:
            self.move(self.alg_txt.currentIndex())
        else:
            self.move(self.alg_bin.currentIndex())

    def lib_change(self):
        self.lib_widget = LibWidget(self.lib_update)
        self.lib_widget.show()

    def lib_update(self):
        self.text = text.Text()
        self.alg_t = [algorithm.Caesar(), algorithm.MonoCipher(), algorithm.TranspositionCipher()]
        self.alg_b = [algorithm.TranspositionCipher(), algorithm.MonoCipherBin()]
        self.check_key()

    def encryption(self):
        if self.key is None:
            self.hint.setText('требуется ключ')
            return
        try:
            if self.txt_mode.isChecked():
                data = self.text.to_string(self.inp.toPlainText())[0]
                print(data, type(data), self.text.l_l())
                data = self.chip.encryption_fun(data, self.text.l_l(), self.key)
                data = self.text.to_string(data)[1]
                self.out.setText(data)

            else:
                data = self.inp.toPlainText()
                data = list(map(lambda x: int(x) % 256, data.split()))
                data = self.chip.encryption_fun(data, 256, self.key)
                self.out.setText(' '.join(map(str, data)))
            self.hint.setText('')

        except OSError as ex:
            self.hint.setText('error: ' + str(ex))

    def decryption(self):
        if self.key is None:
            self.hint.setText('требуется ключ')
            return
        try:
            print(self.txt_mode.isChecked())
            if self.txt_mode.isChecked():
                data = self.text.to_string(self.inp.toPlainText())[0]
                data = self.chip.decryption_fun(data, self.text.l_l(), self.key)
                data = self.text.to_string(data)[1]
                self.out.setText(data)
            else:
                data = self.inp.toPlainText()
                data = list(map(lambda x: int(x) % 256, data.split()))
                data = self.chip.decryption_fun(data, 256, self.key)
                self.out.setText(' '.join(map(str, data)))

        except OSError as ex:
            self.hint.setText('error: ' + str(ex))

    def reverse(self):
        code = self.out.toPlainText()
        self.out.setText(self.inp.toPlainText())
        self.inp.setText(code)

    def open(self):
        try:
            if self.txt_mode.isChecked():
                fname = QFileDialog.getOpenFileName(self, 'выбрать файл', '', 'Текстовый файл (*.txt)')[0]
                with open(fname, mode='rt', encoding='utf8') as f:
                    data = f.read()
                self.inp.setText(data)
            else:
                fname = QFileDialog.getOpenFileName(
                    self, 'выбрать файл', '', "Картинка (*.png *.xpm *.jpg);;"
                                              "Текстовый файл (*.txt);;"
                                              "Все файлы (*)")[0]
                self.inp.setText(' '.join(map(str, bin_algoritm.encoding(fname))))
            self.hint.setText('выгруска успешно завершена')
        except OSError as ex:
            self.hint.setText('error: ' + str(ex))
        except UnicodeDecodeError as ex:
            self.hint.setText('error: ' + str(ex))

    def save_txt(self):
        try:
            if self.txt_mode.isChecked():
                f_name = QFileDialog.getSaveFileName(self, 'выбрать файл', '', 'Текстовый файл (*.txt)')[0]
                with open(f_name, mode='wt', encoding='utf8') as f:
                    f.write(self.out.toPlainText())
            else:
                f_name = QFileDialog.getSaveFileName(
                    self, 'выбрать файл', '', "Картинка (*.png *.xpm *.jpg);;"
                                              "Текстовый файл (*.txt);;"
                                              "Все файлы (*)")[0]
                bin_algoritm.decoding(f_name, self.out.toPlainText())
            self.hint.setText('файл успешно сохранён')
        except OSError as ex:
            self.hint.setText('error: ' + str(ex))

    def check_key(self):
        key = self.key_line.text()
        if not key:
            return
        print('ok1')
        if self.txt_mode.isChecked():
            res = self.chip.key_check(key, self.text.l_l())
        else:
            res = self.chip.key_check(key, 256)
        print('ok2')
        if not res[0]:
            self.hint.setText('неверный ключ')
            self.key = None
            return
        elif self.hint.text() == 'неверный ключ':
            self.hint.setText('')
        self.key = res[1]
        print(self.key)
        print(*self.key)

    def generator(self):
        if self.txt_mode.isChecked():
            key = self.chip.key_generator(self.text.l_l())
            self.key_line.setText(key)
        else:
            self.key_line.setText(self.chip.key_generator(size=256))
        self.check_key()

    def save_key(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'выбрать файл', '', 'Текстовый файл (*.txt)')[0]
            with open(fname, mode='wt', encoding='utf8') as f:
                f.write(self.key_line.text())
        except OSError as ex:
            self.hint.setText('error: ' + str(ex))

    def import_key(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'выбрать файл', '', 'Текстовый файл (*.txt)')[0]
            with open(fname, mode='rt', encoding='utf8') as f:
                self.key_line.setText(f.read())
        except OSError as ex:
            self.hint.setText('error: ' + str(ex))


class LibWidget(QWidget):
    def __init__(self, l_b):
        super().__init__()
        uic.loadUi('алфавит.ui', self)  # Загружаем дизайн

        self.l_b = l_b

        self.import_txt.clicked.connect(self.imp)
        self.export_txt.clicked.connect(self.export)
        self.undo.clicked.connect(self.open)
        self.save_lib.clicked.connect(self.save)

        self.open()

    def save(self):
        with open('library.txt', mode='wt', encoding='utf8') as f:
            f.write(self.line.toPlainText())
        self.l_b()
        self.destroy()

    def open(self):
        with open('library.txt', mode='rt', encoding='utf8') as f:
            self.line.setText(f.read())

    def export(self):
        try:
            f_name = QFileDialog.getOpenFileName(self, 'выбрать файл', '', 'Текстовый файл (*.txt)')[0]
            with open(f_name, mode='wt', encoding='utf8') as f:
                f.write(self.line.toPlainText())
        finally:
            pass

    def imp(self):
        try:
            f_name = QFileDialog.getOpenFileName(self, 'выбрать файл', '', 'Текстовый файл (*.txt)')[0]
            with open(f_name, mode='rt', encoding='utf8') as f:
                self.line.setText(f.read())
        finally:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cryptographer()
    ex.show()
    sys.exit(app.exec_())