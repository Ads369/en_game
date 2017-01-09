#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.html as html
import html_str
import lxml
import threading
import time
from lxml   import etree
from lxml.html.clean import Cleaner

cleaner = Cleaner()
cleaner.javascript = True # This is True because we want to activate the javascript filter
cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter


class en_m_game(object):
    """Класс экземпляра игры
    На данный момент версия программы адаптирована под полную версию сайта
    Но какким то магическим образом работает все вкроме задания.
    """


    def __init__(self, domain = "", game = 0,
                    lvl = 0, pos = 0, time_out = 1,
                    page_path = "", page = ""):
        self.domain = domain
        self.game = game
        self.lvl = lvl
        self.pos = pos
        self.sec = pos
        self.help = pos
        self.time_out = time_out
        self.page_path = page_path
        self.page = cleaner.clean_html(html.parse(page_path))


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


    def clear_string(self, str):
        '''Удаление \t и \n'''
        str = str.replace('\t', '')
        str = str.strip()
        return(str)


    #Начало блока: Поиск сообщений от автора
    def get_auth_mess(self):
        e = self.page.getroot().find_class('globalmess').pop()
        i = e.text_content()
        i = i.replace('\t', '')
        i = i.strip()
        #print("Собщения от авторов:")
        return(i)


    def check_lvl(self):
        '''Возвращает только номер текушего уровня'''
        t = self.page.xpath("//h2/span/text()")[0]
        return(t)

    def check_answer(self):
        '''Возвращает только номер текушего уровня'''
        t = self.page.xpath("//ul[@class='history']/li[1]/text()")[0]
        if t.index("неверный"):
            return("неверный")
        else:
            return(self.page.xpath("//ul[@class='history']/li[2]/span[@class='color_correct']")[0])


    def get_lvl_name(self):
        '''Возвращает номер уровня, сколько всего и название'''
        t = self.page.xpath("//h2")[0]
        str_t = t.text_content().split(' ')
        #print("Уровень:")
        return(str_t[1],str_t[3][0:-1],str_t[4])


    #Начало блока: с автопереходом
    def get_auto_finish(self):
        try:
            t = self.page.xpath("//h3[@class='timer']/span/b/text()")
            while len(t) < 3:
                t.insert(0, 0)
            timer_h = t[0]
            timer_m = t[1]
            timer_s = t[2]
            #print("Автореперход:")
            return(timer_h,timer_m,timer_s)
        except IndexError:
            return(None)


    def count_h3(self):
        e = self.page.xpath("//h3/text()[normalize-space()]")
        print(e)
        for i in e:
            if "Задание" in i:
                #print(i)
                pass
            elif "следующий" in i:
                #print(i)
                pass
            elif "На уровне" in i:
                #print(i)
                pass
        pass


    def get_all(self):
        self.add_url_a()
        self.add_url_img()
        e = self.page.xpath("//div[@class='content']")
        print(self.clear_string(e[0].text_content()))


    #Начало блока: с информацией о секторах
    #На данный момент не рабочий
    def get_sectors(self):
        #Попыткак найти сектроа
        #e = self.page.xpath("//h3[contains(.,'На уровне')]")
        e = self.page.xpath(
                "//p[preceding-sibling::h3[contains(.,'На уровне')]"
                " and following-sibling::h3]]")
        print(e)
        result = ""
        for i in e:
            result += i.text_content()+"\n"
        return(result)
        '''
        try:
            e = self.page.xpath("//div[@class='cols-wrapper']")[0]
            str_t = e.text_content()
            str_t = self.clear_string(str_t)
            #print("Сектора:")
            return(str_t)
        except IndexError:
            return(None)
        '''

    def get_count_sectors(self):
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
            return(1,1)
            self.sec = 0


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


    def get_task(self, current_index):
        '''Берет задание или плдсказки зависит от индекса'''
        e = self.page.xpath('//div[@class="content"]')[0]
        t = e.xpath('//div[@class="spacer"]')
        t1 = e.index(t[current_index])+1
        try:
            t2 = e.index(t[current_index+1])
        except IndexError:
            t2 = len(e)
        result = ""
        for i in e[t1:t2]:
            result += i.text_content()+"\n"
        return(result)


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
        self.pos = 0
        self.lvl,total_lvl,name_lvl = self.get_lvl_name()
        g_hour,g_min,g_sec = self.get_auto_finish()
        if g_sec:
            self.pos += 1
            auto_finish_text = "Автопереход через: %s:%s:%s" %(g_hour,g_min,g_sec)
        else:
            auto_finish_text = ""
        g_total_sec, g_left_sec = self.get_count_sectors()
        if int(g_total_sec) > 1:
            self.pos += 1
            sector_text = "Нужно закрыть: %s из %s" %(g_left_sec,g_total_sec)
        else:
            sector_text = "Нужно закрыть: 1 из 1"
        self.add_url_a()
        self.add_url_img()
        g_task = self.get_task(self.pos)


        g_lvl_text = "Уровень: %s из %s: %s \n" %( self.lvl,total_lvl,name_lvl)
        g_lvl_text += auto_finish_text + '\n'
        g_lvl_text += sector_text + '\n'
        g_lvl_text += '\n' + g_task
        print(g_lvl_text)
        pass

    def game_start(self):
        self.new_lvl()
        check_lvl = threading.Thread(target=self.timer_set, args=(self.lvl,))
        check_lvl.start()
        pass


