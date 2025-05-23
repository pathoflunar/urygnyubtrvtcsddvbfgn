from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QRadioButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QLineEdit, QInputDialog
import json

def show_notes():
    key = Zametki_Box.selectedItems()[0].text()
    Zametka.setText(notes[key]['Text'])
    Tag_Box.clear()
    Tag_Box.addItems(notes[key]['Tag'])

def add_note():
    notes_name, ok = QInputDialog.getText(window, 'Добавить заметку', "Название заметки:")
    if ok:
        notes[notes_name] = {
            'Text' : "",
            'Tag' : []
        }
    Zametki_Box.clear()
    Zametki_Box.addItems(notes)
    with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def del_note():
    if Zametki_Box.selectedItems():
        key = Zametki_Box.selectedItems()[0].text()
        del notes[key]
        Zametka.clear()
        Zametki_Box.clear()
        Tag_Box.clear()
        Zametki_Box.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def save_note():
    if Zametki_Box.selectedItems():
        key = Zametki_Box.selectedItems()[0].text()
        notes[key]['Text'] = Zametka.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def add_tag():
    if Zametki_Box.selectedItems():
        key = Zametki_Box.selectedItems()[0].text()
        tag = Tag_Vvod.text()
        if tag != '' and not tag in notes[key]['Tag']:
            notes[key]['Tag'].append(tag)
            Tag_Box.addItem(tag)
            Tag_Vvod.clear()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def del_tag():
    if Zametki_Box.selectedItems():
        key = Zametki_Box.selectedItems()[0].text()
        keyTag = Tag_Box.selectedItems()[0].text()
        notes[key]['Tag'].remove(keyTag)
        Tag_Box.clear()
        Tag_Box.addItems(notes[key]['Tag'])
        with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def search_tag():
    tag = Tag_Vvod.text()
    if tag != '' and Search_Zamet.text() == "Искать заметку по тегу":
        notes_filtered = dict()
        for key in notes:
            if tag in notes[key]['Tag']:
                notes_filtered[key] = notes[key]
        Search_Zamet.setText("Сбросить поиск")
        Zametki_Box.clear()
        Tag_Vvod.clear()
        Zametka.clear()
        Zametki_Box.addItems(notes_filtered)
    else:
        Zametki_Box.clear()
        Zametki_Box.addItems(notes)
        Tag_Vvod.clear()
        Search_Zamet.setText("Искать заметку по тегу")

app = QApplication([]) # приложение
window = QWidget() # окно
window.setWindowTitle('TheZameto4ka ¡')
window.resize(900, 600)

# ----------------------------------------------------------

Zametka = QTextEdit() # Вводим заметку сюда
Zametki_Box = QListWidget() # Здесь список заметок
Zametki_Box_Label = QLabel("Список заметок") # Название бокса
Tag_Box = QListWidget() # Список #Тегов
Tag_Box_Label = QLabel("Список тегов") # Название наших тегов
Tag_Vvod = QLineEdit() # Вводим тег
Tag_Vvod.setPlaceholderText("Введите тег") # это текст в боксе выше 
Create_Zamet = QPushButton("Создать заметку") # Создаём заметку
Delete_Zamet = QPushButton("Удалить заметку") # Удаляем заметку
Save_Zamet = QPushButton("Сохранить заметку") # Сохраняём заметку
Lock_Tag = QPushButton("Закрепить к заметке") # Крепим тег к заметке
Unlock_Tag = QPushButton("Открепить от заметки") # откреплчем тег
Search_Zamet = QPushButton("Искать заметку по тегу") #Ищем заметку по следам

LeadHLine = QHBoxLayout()
VLine_1 = QVBoxLayout()
VLine_2 = QVBoxLayout()
Dop_HLine_1 = QHBoxLayout()
Dop_HLine_2 = QHBoxLayout()
LeadHLine.addLayout(VLine_1)
LeadHLine.addLayout(VLine_2)
VLine_1.addWidget(Zametka)
VLine_2.addWidget(Zametki_Box_Label)
VLine_2.addWidget(Zametki_Box)
VLine_2.addLayout(Dop_HLine_1)
Dop_HLine_1.addWidget(Create_Zamet)
Dop_HLine_1.addWidget(Delete_Zamet)
VLine_2.addWidget(Save_Zamet)
VLine_2.addWidget(Tag_Box_Label)
VLine_2.addWidget(Tag_Box)
VLine_2.addWidget(Tag_Vvod)
VLine_2.addLayout(Dop_HLine_2)
Dop_HLine_2.addWidget(Lock_Tag)
Dop_HLine_2.addWidget(Unlock_Tag)
VLine_2.addWidget(Search_Zamet)

window.setLayout(LeadHLine)

# ----------------------------------------------------------

with open('notes_data.json', 'r') as file:
    notes = json.load(file)

Zametki_Box.addItems(notes)
Zametki_Box.itemClicked.connect(show_notes)
Create_Zamet.clicked.connect(add_note)
Delete_Zamet.clicked.connect(del_note)
Save_Zamet.clicked.connect(save_note)
Lock_Tag.clicked.connect(add_tag)
Unlock_Tag.clicked.connect(del_tag)
Search_Zamet.clicked.connect(search_tag)

# ----------------------------------------------------------

window.show() #показать окно
app.exec() #открыть окно