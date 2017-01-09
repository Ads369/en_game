#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.html as html
import html_str
import lxml
import threading
import time
import string
import random
from lxml   import etree
from lxml.html.clean import Cleaner

cleaner = Cleaner()
cleaner.javascript = True # This is True because we want to activate the javascript filter
cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter


class en_game(object):
    """Класс экземпляра игры
    На данный момент версия программы адаптирована под полную версию сайта
    Но какким то магическим образом работает все вкроме задания.

    Порядок в полной версии:
        Название уровня
        Сектора
        Задание
        Подсказки
        Штрафные подсказки
        Бонусы
    """


    def __init__(self,
                domain = "",
                game = 0,
                owner = "",
                page_path = "",
                page = ""):

        self.domain = domain
        self.game = game
        self.owner = owner
        self.chat = ""
        self.key = self.key_generator()
        self.time_out = time_out
        self.page_path = page_path
        self.page = cleaner.clean_html(html.parse(page_path))
        self.lvl = 0
        self.pos_timeout = -1
        self.pos_sec = -1
        self.pos_task = -1
        self.pos_sup_help = -1
        self.help_arr = []
        self.bonus_arr = []
        return(self.key)


    def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return(''.join(random.choice(chars) for _ in range(size)))


    def new_game(self):
        return()


    def connect_game(self):



    def to_file(self):
        return(html.tostring(self.page, pretty_print=True, method="html",
            encoding='unicode'))


    def set_domain(self, in_str = ""):
        '''Устанавливает значение domain'''
        self.domain = in_str


    def set_game(self, in_str = ""):
        '''Устанавливает значение game'''
        self.game = in_str


    def set_time_out(self, in_str = ""):
        '''Устанавливает значение time_out'''
        self.time_out = in_str


    def set_page_path(self, in_str = ""):
        '''Устанавливает значение page_path'''
        self.page_path = in_str


    def set_page(self, in_str = ""):
        '''Устанавливает значение page'''
        self.page = in_str


    def reload_page(self):
        '''Обновить данные'''
        self.page = cleaner.clean_html(html.parse(self.page_path))


    def reload_lvl(self):
        self.pos_timeout = -1
        self.pos_sec = -1
        self.pos_task = -1
        self.pos_sup_help = -1
        self.help_arr = []
        self.bonus_arr = []
        pass


    def clear_string(self, str):
        '''Удаление \t и \n'''
        str = str.replace('\t', '')
        str = str.strip()
        return(str)

    # e = self.page.xpath("//h3/text()[normalize-space()]")
    # "/descendant-or-self::*/text()[normalize-space()]")


    def get_position_global(self):
        '''Выясняет какие спейсы к чему относятся на глобальном уровне'''
        e = self.page.xpath('//div[@class="content"]')[0]
        #Позиция автоперехода
        t = e.xpath('//h3[@class="timer"][1]')
        if t:
            self.pos_timeout = e.index(t[0])-1
            print("timeout=",e.index(t[0])-1)
        #Позиция секторов
        t = e.xpath('//div[@class="cols-wrapper"][1]')
        if t:
            self.pos_sec = e.index(t[0])-2
            print("pos_sec=",e.index(t[0])-2)
        #Позиция Задание
        t = e.xpath('//h3[contains(.,"Задание")][1]')
        if t:
            self.pos_task = e.index(t[0])-1
            print("pos_task=",e.index(t[0])-1)
        #Позиция штрафная подскзок
        t = e.xpath('//h3[contains(.,"Штрафная подсказка")][1]')
        if t:
            self.pos_sup_help = e.index(t[0])-1
            print("pos_sup_help=",e.index(t[0])-1)
        #Позиция бонусы
        t = e.xpath('//h3[contains(.,"Бонус")]')
        if t:
            arr = [e.index(x)-1 for x in t]
            self.bonus_arr = arr
            print("bonus_arr=",arr)

        t = self.page.xpath('//div[@class="spacer"]')
        print([e.index(x) for x in t])
        pass


    def get_position(self):
        '''Выясняет какие спейсы к чему относятся'''
        e = self.page.xpath('//div[@class="spacer"]')
        #Позиция автоперехода
        #print(e)
        for i in e:
            s = i.xpath("./following-sibling::*[1]/"
                            "text()[normalize-space()]")
            #print(s)
            if s[0].startswith("на следующий",1):
                self.pos_timeout = e.index(i)
            elif s[0].startswith("На уровне"):
                self.pos_sec = e.index(i)
            elif s[0].startswith("Задание"):
                self.pos_task = e.index(i)
            elif s[0].startswith("Подсказка") or\
                     s[0].startswith("будет через",1):
                self.help_arr.append(e.index(i))
            elif s[0].startswith("Штрафная подсказка"):
                self.pos_sup_help= e.index(i)
            elif s[0].startswith("Бонус",5):
                self.bonus_arr.append(e.index(i))
        pass


    def print_index(self):
        result = ["ТО = ",str(self.pos_timeout),"\n",
        "Сек = ",str(self.pos_sec),"\n",
        "Зад = ",str(self.pos_task),"\n",
        "Под = ",str(self.help_arr),"\n",
        "ШП = ",str(self.pos_sup_help),"\n",
        "Бон = ",str(self.bonus_arr),"\n"]
        return(''.join(result))


    def get_auth_mess(self):
        '''Начало блока: Поиск сообщений от автора'''
        e = self.page.xpath("//*[@class='globalmess']")
        i = [x.text_content() for x in e][0]
        i = [x.strip() for x in i.split("\n")]
        i = "\n".join(i).strip()
        return(i)


    def check_lvl(self):
        '''Возвращает только номер текушего уровня'''
        t = self.page.xpath("//h2/span/text()")[0]
        return(t)


    def check_answer(self):
        '''Проверка на коррекность ответа
        !!!работоспособность не проверяд
        '''
        t = self.page.xpath("//ul[@class='history']/li[1]/text()")[0]
        if t.index("неверный"):
            return("неверный")
        else:
            return(self.page.xpath("//ul[@class='history']/li[2]/span[@class='color_correct']")[0])


    def get_lvl_name(self):
        t = self.page.xpath("//h2[1]/descendant-or-self::*"
                        "/text()[normalize-space()]")
        return("".join(t))


    #Начало блока: с автопереходом
    def get_auto_finish(self):
        t = self.page.xpath("//h3[@class='timer']/span/b/text()")
        if t:
            while len(t) < 4:
                t.insert(0, 0)
            #print("Автореперход:")
            return(int(t[0]),int(t[1]),int(t[2]),int(t[3]))
        else:
            return(None)


    def get_left_sectors(self):
        '''
        Возвращет все названия всех не закрытых секторов
        '''
        try:
            e = self.page.xpath("//div[@class='cols-wrapper']"
                        "/div[1]/p/span[@class='color_dis']/..")
            return([x.text[7:-2] for x in e])
        except IndexError:
            return(None)


    #На данный момент не рабочий
    def get_sectors(self):
        '''Возвращает все сектора и их статусы как на сайте'''
        try:
            e = self.page.xpath("//div[@class='cols-wrapper']")[0]
            str_t = e.text_content()
            str_t = self.clear_string(str_t)
            #print("Сектора:")
            return(str_t)
        except IndexError:
            return(None)


    def get_count_sectors(self):
        '''Возвращает 2 числа всего секторов и осталось'''
        e = self.page.xpath("//h3[contains(.,'На уровне')]/descendant-or-self::*/text()[normalize-space()]")
        if e:
            str_1 = ' '.join(e).split()
            self.sec = str_1[2]
            try:
                #специально стоит 6 для отлова ошибки
                return(str_1[2],str_1[6][0:-1])
            except IndexError:
                return(str_1[2],str_1[2])
        else:
            return(None)


    def print_all_img(self):
        e = self.page.getroot().find_class('content').pop()
        return(e.xpath("//img/@src")[2:])


    def print_all_href(self):
        e = self.page.getroot().find_class('content').pop()
        return(e.xpath("//a/@href")[5:])


    def add_url_img(self):
        '''Заменяет все <img> ссылки на текстовый вариант'''
        e = self.page.getroot().find_class('content').pop()
        for i in e.xpath("//img")[2:]:
            url = i.get('src')
            newtag = etree.Element("a", href=url)
            newtag.text = url
            i.getparent().replace(i,newtag)
            pass


    def add_url_a(self):
        '''Заменяет все <a> ссылки на текстовый вариант'''
        e = self.page.getroot().find_class('content').pop()
        for i in e.xpath("//a")[2:]:
            url = i.get('href')
            if url is not None:
                newtag = etree.Element("a", href=url)
                newtag.text = i.text_content()+ "{%s}" %url
                try:
                    i.getparent().replace(i,newtag)
                except:
                    print(url , i.text_content())
            pass


    def get_block(self,current_index = 1):
        '''Берет всю информацию между двумя блоками
        '''
        e = self.page.xpath('//div[@class="content"]')[0]
        t = e.xpath('//div[@class="spacer"]')
        t1 = e.index(t[current_index])+1
        try:
            #t2 = e.index(t[current_index+1])
            result = [self.clear_string(i.text_content())\
                         for i in e[t1:e.index(t[current_index+1])]]
        except IndexError:
            result = [self.clear_string(i.text_content()) for i in e[t1:]]
        return("\n".join(result))


    def get_block_to(self):
        '''Возвращает все данные по автопереходу '''
        return(self.get_block(self.pos_timeout))


    def get_block_sectors(self):
        '''Возвращает все данные по секторам '''
        return(self.get_block(self.pos_sec))


    def get_block_task(self):
        '''Возвращает блок задания '''
        return(self.get_block(self.pos_task))


    def get_block_help(self):
        '''Возвращает 1 подсказку '''
        return(self.get_block(self.help_arr.pop(0)))


    def get_block_sup_help(self):
        '''Возвращает штрафную подсказку'''
        return(self.get_block(self.pos_sup_help))


    def get_block_bonus(self):
        '''Возвращает 1 бонус'''
        return(self.get_block(self.bonus_arr.pop(0)))


    def get_time_help(self):
        result = []
        for i in self.help_arr:
            e = self.page.xpath('//div[@class="spacer"]')[i]
            t = e.xpath("./following-sibling::*[1]/span/b/"
                            "text()[normalize-space()]")
            if t:
                t = [int(x) for x in t]
                while len(t) < 4:
                    t.insert(0, 0)
                t.insert(0, t.pop(0) * 24 + t.pop(0))
                result.append(t)
        if result:
            return(result)
        else:
            return(None)


    def timer_set(self, global_lvl):
        print("-=-")
        local_lvl = global_lvl
        print(local_lvl,global_lvl)
        while (global_lvl == local_lvl):
            time_out = int(self.time_out)
            time.sleep(time_out)
            self.reload_page()
            local_lvl = self.check_lvl()
            print(local_lvl,global_lvl)
            print(".")
        print(local_lvl,global_lvl)
        self.new_lvl()
        pass


    def new_lvl(self):
        self.reload_lvl()
        #self.add_url_a()
        self.add_url_img()
        self.get_position()

        self.lvl = self.check_lvl()
        timeout = self.get_auto_finish()
        if timeout is not None:
            auto_finish_text = "Автопереход через: %d:%d:%d" %(
                            timeout[0]*24+timeout[1],timeout[2],timeout[3])
        else:
            auto_finish_text = ""

        sectors = self.get_count_sectors()
        if sectors is not None:
            sector_text = "Нужно закрыть: %s из %s" %(sectors[1],sectors[0])
        else:
            sector_text = ""

        help_time_arr = self.get_time_help()
        helps_time = []
        if help_time_arr is not None:
            for i in help_time_arr:
                i = [str(x) for x in i]
                helps_time.append(':'.join(i))
            helps_time_str = "Подсказки: " + ", ".join(helps_time)


        return(self.get_lvl_name() + '\n' + auto_finish_text + '\n' +\
            sector_text + '\n' + helps_time_str +'\n\n' + self.get_block_task())


    def game_start(self):
        self.new_lvl()
        check_lvl = threading.Thread(target=self.timer_set, args=(self.lvl,))
        check_lvl.start()
        pass