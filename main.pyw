from html.parser import HTMLParser
from urllib.request import urlopen
from tkinter import *

class NewHTMLParser(HTMLParser):
    def __init__(self, site_name, *args, **kwargs):
        # список ссылок
        self.links = []
        # имя сайта
        self.site_name = site_name
        # вызываем __init__ родителя
        super().__init__(*args, **kwargs)
        # при инициализации "скармливаем" парсеру содержимое страницы
        self.feed(self.read_site_content())
        # записываем список ссылок в файл
        self.write_to_file()

    def handle_starttag(self, tag, attrs):
        # проверяем является ли тэг тэгом ссылки
        if tag == 'a':
            # находим аттрибут адреса ссылки
            for attr in attrs:
                if attr[0] == 'href':
                    # проверяем эту ссылку методом validate()
                    if not self.validate(attr[0]):
                    	if self.validate_link(attr[1]):
                        	# вставляем адрес в список ссылок
                        	self.links.append(attr[1])

    def validate(self, link):
        """ Функция проверяет стоит ли добавлять ссылку в список адресов.
        В список адресов стоит добавлять если ссылка:
             1) Еще не в списке ссылок
             2) Не вызывает javascript-код
             3) Не ведет к какой-либо метке. (Не содержит #)
         """
        return link in self.links or '#' in link or 'javascript:' in link

    def read_site_content(self):
        return str(urlopen(self.site_name).read())

    def write_to_file(self):
        # открываем файл
        f = open('links.txt', 'w')
        # записываем отсортированный список ссылок, каждая с новой строки
        f.write('\n'.join(sorted(self.links)))
        # закрываем файл
        f.close()

    def validate_link(self, link):
    	if link[:4]=='http':
    		return True

    def __del__(self):
        pass

def handler():
    link = str(entrylink.get())
    parsing = NewHTMLParser(link)
    #удаляем к хуям объект
    parsing.__del__()

root = Tk()
root.title('Link parser')
root.geometry('350x80')
label1 = Label(root, text="Enter a web-page:")
label1.pack()
entrylink = Entry(root, width=50)
entrylink.pack()
button1 = Button(root, text="Apply", command=handler)
button1.pack()
root.mainloop()