import sys
import sqlite3
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QDialog
from PyQt5 import uic


con = sqlite3.connect("basa.db")
cur = con.cursor()


# Полный перезапуск игры
def restart_game():
    cur.execute("""update human set hp = 100, gold = 100, maxhp = 100, damage = 10, defense = 0, exp = 0""")
    cur.execute("""update levels set have = 0 where have = 1""")
    cur.execute("""update levels set have = 1 where level = 1""")
    cur.execute("""update armor set have = 0""")
    cur.execute("""update armor set have = 1 where id in (1, 6, 11, 16, 21)""")
    cur.execute("""update armor set damage = dmnormal, hp = hpnormal, defense = dfnormal, gold = goldnormal""")
    cur.execute("""update armor set level = 0""")
    con.commit()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi('main.ui', self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.monster.clicked.connect(self.monstr)
        self.inventary.clicked.connect(self.inven)
        self.smith.clicked.connect(self.sm)
        self.settings.clicked.connect(self.setting)
        self.shaman.clicked.connect(self.shaman_look)

        self.pixmap = QPixmap('heart.png')
        self.heart.setPixmap(self.pixmap)

        self.low_hp.hide()
        self.label.hide()
        self.label_2.hide()

        # выводим на экран всю информцию о персонаже

        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        res = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {res[0]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()[0]
        self.exp.setText(f"exp: {expir}/{maxexp}")

        self.res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {self.res[0]}/{self.res[1]}")

        if self.res[0] < 1:  # проверка, жив ли персонаж
            self.low_hp.show()
            self.label.show()
            self.label_2.show()

    def monstr(self):
        if self.res[0] > 0:  # Если у нас 0 хп, запрещаю все кнопки кроме настроек и шамана, который восстановит hp
            self.monsters_view = Monsters()
            self.monsters_view.show()
            self.hide()

    def setting(self):
        self.setting_view = Setting()
        self.setting_view.show()
        self.hide()

    def inven(self):
        if self.res[0] > 0:
            self.inven_view = Inventory()
            self.inven_view.show()
            self.hide()

    def sm(self):
        if self.res[0] > 0:
            self.smith_view = BlackSmith()
            self.smith_view.show()
            self.hide()

    def shaman_look(self):
        self.shaman_view = Shaman()
        self.shaman_view.show()
        self.hide()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        self.draw_flag(qp)
        qp.end()

    def draw_flag(self, qp):
        qp.setBrush(QColor(48, 8, 8))
        qp.drawRect(80, 270, 258, 320)
        qp.drawRect(80, 70, 250, 100)


class Monsters(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.initUi()
        except Exception as o:
            print(o)

    def initUi(self):
        uic.loadUi('monstr.ui', self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.pixmap = QPixmap('heart.png')
        self.heart.setPixmap(self.pixmap)

        self.back.clicked.connect(self.backing)

        self.spider.clicked.connect(self.spider_run)
        self.wolf.clicked.connect(self.wolf_run)
        self.troll.clicked.connect(self.troll_run)
        self.troll_king.clicked.connect(self.troll_king_run)
        self.grifon.clicked.connect(self.grifon_run)
        self.vasilisk.clicked.connect(self.vasilisk_run)
        self.dragon.clicked.connect(self.dragon_run)

        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {res[0]}/{res[1]}")

        res = cur.execute("""select damage, defense from human""").fetchone()
        self.attack.setText(f"Атака: {res[0]}")
        self.defense.setText(f"Защита: {res[1]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()
        self.exp.setText(f"exp: {expir[0]}/{maxexp}")

    def spider_run(self):
        self.monsteer_view = Monsteer("паук")
        self.monsteer_view.show()
        self.hide()

    def wolf_run(self):
        self.monsteer_view = Monsteer("волк")
        self.monsteer_view.show()
        self.hide()

    def troll_run(self):
        self.monsteer_view = Monsteer("тролль")
        self.monsteer_view.show()
        self.hide()

    def troll_king_run(self):
        self.monsteer_view = Monsteer("король троллей")
        self.monsteer_view.show()
        self.hide()

    def grifon_run(self):
        self.monsteer_view = Monsteer("грифон")
        self.monsteer_view.show()
        self.hide()

    def vasilisk_run(self):
        self.monsteer_view = Monsteer("василиск")
        self.monsteer_view.show()
        self.hide()

    def dragon_run(self):
        self.monsteer_view = Monsteer("дракон")
        self.monsteer_view.show()
        self.hide()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        self.draw_flag(qp)
        qp.end()

    def draw_flag(self, qp):
        qp.setBrush(QColor(48, 8, 8))
        qp.drawRect(70, 10, 300, 70)
        qp.drawRect(70, 85, 300, 90)
        qp.drawRect(70, 180, 300, 440)

    def backing(self):
        self.main_view = Main()
        self.main_view.show()
        self.hide()


class Monsteer(QMainWindow):
    def __init__(self, animal):
        self.animal = animal  # по этой переменной я буду определять против кого сражается персонаж
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi("moonster.ui", self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.pixmap = QPixmap('heart.png')
        self.heart.setPixmap(self.pixmap)

        self.fight()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        self.draw_flag(qp)
        qp.end()

    def draw_flag(self, qp):
        qp.setBrush(QColor(48, 8, 8))
        qp.drawRect(90, 35, 280, 115)
        qp.drawRect(90, 170, 280, 245)
        qp.drawRect(90, 450, 280, 70)

    def closing(self):
        self.close()
        self.monsters_view = Monsters()
        self.monsters_view.show()

    def closing_lose(self):
        self.close()
        self.zerohp_view = ZeroHp()
        self.zerohp_view.show()

    def fight(self):
        # Реализация нанесения урона в битве
        res = cur.execute("""select damage, defense, hp from human""").fetchone()
        player_damage = res[0]  # Мой дамаг
        player_defense = 1 - ((0.06 * res[1]) / (1 + 0.06 * res[1]))  # Броня поглощает некоторый урон
        player_hp = res[2]  # Мои хр
        damage, defense, hp, i = 0, 0, 0, 0
        # У разных врагов разное количество брони, хп и урона
        if self.animal == "паук":
            damage = 15
            defense = 1 - ((0.06 * 0) / (1 + 0.06 * 0))
            hp = 50
        elif self.animal == "волк":
            damage = 30
            defense = 1 - ((0.06 * 4) / (1 + 0.06 * 4))
            hp = 400
        elif self.animal == "тролль":
            damage = 70
            defense = 1 - ((0.06 * 4) / (1 + 0.06 * 4))
            hp = 1000
        elif self.animal == "король троллей":
            damage = 300
            defense = 1 - ((0.06 * 8) / (1 + 0.06 * 8))
            hp = 2000
        elif self.animal == "грифон":
            damage = 600
            defense = 1 - ((0.06 * 15) / (1 + 0.06 * 15))
            hp = 3000
        elif self.animal == "василиск":
            damage = 1000
            defense = 1 - ((0.06 * 30) / (1 + 0.06 * 30))
            hp = 5000
        elif self.animal == "дракон":
            damage = 4000
            defense = 1 - ((0.06 * 50) / (1 + 0.06 * 50))
            hp = 10000
        with open("inf.txt", "w", encoding="utf-8") as f:  # записываю инфу в файл, откуда буду выводить на qt
            while player_hp >= 0 and hp >= 0:
                hp -= int(player_damage * defense)  # нанесение урона врагу
                f.write(f"-Вы наносите противнику {int(player_damage * defense)} урона\n")  # Записб в файл
                if hp > 0:
                    player_hp -= int(damage * player_defense)
                    f.write(f"-Противник наносит вам {int(damage * player_defense)} урона\n")
                else:
                    break
                i += 1
                if i >= 100:  # 100 ходов для ничью
                    break
            f.close()
        with open("inf.txt", encoding="utf-8") as f:
            self.window_file.setText(f.read())
        if hp <= 0:  # если персонаж побели
            self.but_2.hide()
            self.but_3.hide()
            self.but.clicked.connect(self.closing)
            self.win(player_hp)
        elif player_hp <= 0:  # если победил противнки
            self.but.hide()
            self.but_3.hide()
            self.but_2.clicked.connect(self.closing_lose)
            self.lose()
        else:  # ничья
            self.but.hide()
            self.but_2.hide()
            self.but_3.clicked.connect(self.closing)
            self.draw(player_hp)

    def win(self, hpr):
        # реализация победы и получение exp and gold
        cur.execute("""update human set hp = ?""", (hpr,))
        if self.animal == "паук":
            cur.execute("""update human set gold = gold + 200, exp = exp + 100""")
            self.label.setText(f"Вы выиграли бой и получили 200 голды и 100 exp")
        elif self.animal == "волк":
            cur.execute("""update human set gold = gold + 1000, exp = exp + 500""")
            self.label.setText(f"Вы выиграли бой и получили 1000 голды и 500 exp")
        elif self.animal == "тролль":
            cur.execute("""update human set gold = gold + 4000, exp = exp + 600""")
            self.label.setText(f"Вы выиграли бой и получили 4000 голды и 600 exp")
        elif self.animal == "король троллей":
            cur.execute("""update human set gold = gold + 8000, exp = exp + 1000""")
            self.label.setText(f"Вы выиграли бой и получили 8000 голды и 1000 exp")
        elif self.animal == "грифон":
            cur.execute("""update human set gold = gold + 20000, exp = exp + 2000""")
            self.label.setText(f"Вы выиграли бой и получили 20000 голды и 2000 exp")
        elif self.animal == "василиск":
            cur.execute("""update human set gold = gold + 50000, exp = exp + 4000""")
            self.label.setText(f"Вы выиграли бой и получили 50000 голды и 4000 exp")
        elif self.animal == "дракон":
            cur.execute("""update human set gold = gold + 200000, exp = exp + 5000""")
            self.label.setText(f"Вы выиграли бой и получили 200000 голды и 5000 exp")
        con.commit()
        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()[0]
        if expir >= maxexp:  # Проверка на повышение уровня
            self.lvl_up(expir, maxexp)  # Его реаЛизация
        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {res[0]}/{res[1]}")

        res = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {res[0]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()
        self.exp.setText(f"exp: {expir[0]}/{maxexp}")

    def lvl_up(self, expir, maxexp):
        # Повышаем уровень, прибавляем хп
        cur.execute("""update human 
                       set exp = (select exp from human) - (select maxexp from levels where have = 1)""")
        cur.execute("""update human set hp = hp + (select growhp from levels where have = 1)""")
        cur.execute("""update human set maxhp = maxhp + (select growhp from levels where have = 1)""")
        cur.execute("""update levels set have = 1 where level = (select level from levels where have = 1) + 1""")
        cur.execute("""update levels 
                       set have = 0 where level = (select level from levels where have = 1)""").fetchone()
        con.commit()

    def lose(self):
        # Соответственно проигрыш
        cur.execute("""update human set hp = 0""")
        con.commit()
        hpr = cur.execute("""select maxhp from human""").fetchone()[0]
        expiriance = cur.execute("""select exp from human""").fetchone()[0]
        cur.execute("""update human set gold = gold - ?, exp = 0""", (hpr,))
        con.commit()
        self.label.setText(f"Вы проиграли бой и потеряли {hpr} голды и {expiriance} exp")

        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {res[0]}/{res[1]}")

        res = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {res[0]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()
        self.exp.setText(f"exp: {expir[0]}/{maxexp}")

    def draw(self, player_hp):
        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        cur.execute("""update human set hp = ?""", (player_hp,))
        con.commit()

        res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {res[0]}/{res[1]}")

        res = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {res[0]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()
        self.exp.setText(f"exp: {expir[0]}/{maxexp}")

        self.label.setText("Спустя 100 ходов никто никого не победил")


class ZeroHp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi('zero_hp.ui', self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.nomoney.hide()
        self.restart.hide()
        self.yes.hide()

        self.recover.clicked.connect(self.recovering)

    def recovering(self):
        # Будем покупать хп за голду
        hp = cur.execute("""select maxhp from human""").fetchone()[0]
        gold = cur.execute("""select gold from human""").fetchone()[0]
        if hp > gold:  # если хп больше чем денег
            self.nomoney.show()
            self.restart.show()  # Заставляем начать игру заново, так как персонаж умер и мы не можем выкупиться
            self.yes.show()
            self.yes.clicked.connect(self.restarting)
        else:
            cur.execute("""update human set hp = maxhp, gold = gold - maxhp""")
            con.commit()
            self.main_view = Main()
            self.main_view.show()
            self.hide()

    def restarting(self):
        restart_game()
        self.main_view = Main()
        self.main_view.show()
        self.hide()


class Setting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi('settings.ui', self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.restart.clicked.connect(self.res_run)

        self.back.clicked.connect(self.backing)

    def backing(self):
        self.main_view = Main()
        self.main_view.show()
        self.hide()

    def res_run(self):
        confirmation, ok_pressed = QInputDialog.getItem(
                    self, "Вопрос", "Вы уверены?",
                    ("Да", "Нет"), 1, False)
        if confirmation == "Да" and ok_pressed:
            restart_game()
            self.backing()


class Inventory(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi("inv.ui", self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.back.clicked.connect(self.backing)

        self.swap_1.clicked.connect(self.swaping1)
        self.swap_2.clicked.connect(self.swaping2)
        self.swap_3.clicked.connect(self.swaping3)
        self.swap_4.clicked.connect(self.swaping4)
        self.swap_5.clicked.connect(self.swaping5)

        self.put_on.clicked.connect(self.equipment)

        self.pixmap = QPixmap('heart.png')
        self.heart.setPixmap(self.pixmap)

        res = cur.execute("""select name, way from armor where have = 1 and type = 'меч'""").fetchone()
        self.sword_broken = QPixmap(res[1])
        self.sword.setPixmap(self.sword_broken)
        self.sword_name.setText(res[0])

        res = cur.execute("""select name, way from armor where have = 1 and type = 'шлем'""").fetchone()
        self.helmet_mercenary = QPixmap("Броня\Шлема\Шлем_наемника.jpg")
        self.helmet.setPixmap(self.helmet_mercenary)
        self.helmet_name.setText(res[0])

        res = cur.execute("""select name, way from armor where have = 1 and type = 'доспех'""").fetchone()
        self.tshort_mercenary = QPixmap("Броня\Доспехи\Доспех_наемника.jpg")
        self.tshort.setPixmap(self.tshort_mercenary)
        self.tshort_name.setText(res[0])

        res = cur.execute("""select name, way from armor where have = 1 and type = 'наручи'""").fetchone()
        self.bracer_mercenary = QPixmap("Броня\Наручи\Наручи_наемника.jpg")
        self.bracer.setPixmap(self.bracer_mercenary)
        self.bracer_name.setText(res[0])

        res = cur.execute("""select name, way from armor where have = 1 and type = 'поножи'""").fetchone()
        self.leggins_mecenary = QPixmap("Броня\Поножи\Поножи_наемника.jpg")
        self.leggins.setPixmap(self.leggins_mecenary)
        self.leggins_name.setText(res[0])

        self.interface()

        self.inventary = [self.sword, self.helmet, self.tshort, self.bracer, self.leggins]

        res = cur.execute("""select way from armor where have = 1""").fetchall()
        for i in range(5):
            weapons = QPixmap(res[i][0])
            self.inventary[i].setPixmap(weapons)

        self.labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7,
                       self.label_8, self.label_9, self.label_10, self.label_11, self.label_12, self.label_13,
                       self.label_14, self.label_15, self.label_16, self.label_17, self.label_18, self.label_19,
                       self.label_20]

        res = cur.execute("""select way, have from armor where have = 2""").fetchall()
        for i in range(20):
            try:
                nice = QPixmap(res[i][0])
                self.labels[i].setPixmap(nice)
            except IndexError:
                pass

    def swaping1(self):
        res = cur.execute("""select name from armor where type = 'меч' and have = 0""").fetchall()
        if res == []:
            name, ok_pressed = QInputDialog.getItem(
                self, "Утверждение", f"Вы уже купили все мечи",
                ("Ок", "Ок"), 0, False)
        else:
            name, ok_pressed = QInputDialog.getItem(
                    self, "Магазин", "Какой меч хотите купить?",
                    (res[i][0] for i in range(len(res))), 0, False)
        if ok_pressed:
            if name == "Старый":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 2000:
                    conf, okpress = QInputDialog.getItem(
                            self, "Вопрос", "Вы потратие 2000 голды. Вы уверены?",
                            ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 2000""")
                        cur.execute("""update armor set have = 2 where name = ?""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {2000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "Морионовый":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 10000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 10000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 10000""")
                        cur.execute("""update armor set have = 2 where name = ?""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {10000 - res[0]} голды",
                        ("Ок", "Ок"), 0, False)
            elif name == "Священный":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 100000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 100000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 100000""")
                        cur.execute("""update armor set have = 2 where name = ?""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {100000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "Иритильский":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 500000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 500000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 500000""")
                        cur.execute("""update armor set have = 2 where name = ?""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {500000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)

            res = cur.execute("""select way, have from armor where have = 2""").fetchall()
            for i in range(20):
                try:
                    nice = QPixmap(res[i][0])
                    self.labels[i].setPixmap(nice)
                except IndexError:
                    pass
        self.interface()

    def swaping2(self):
        res = cur.execute("""select name from armor where type = 'шлем' and have = 0""").fetchall()
        if res == []:
            name, ok_pressed = QInputDialog.getItem(
                self, "Утверждение", f"Вы уже купили все шлема",
                ("Ок", "Ок"), 0, False)
        else:
            name, ok_pressed = QInputDialog.getItem(
                self, "Магазин", "Какой шлем хотите купить?",
                (res[i][0] for i in range(len(res))), 0, False)
        if ok_pressed:
            if name == "фариса":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 2000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 2000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 2000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'шлем'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {2000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "лаппа":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 10000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 10000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 10000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'шлем'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {10000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "рыцаря":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 100000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 100000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 100000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'шлем'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {100000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "драконоборца":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 500000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 500000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 500000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'шлем'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {500000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)

        res = cur.execute("""select way, have from armor where have = 2""").fetchall()
        for i in range(20):
            try:
                nice = QPixmap(res[i][0])
                self.labels[i].setPixmap(nice)
            except IndexError:
                pass
        self.interface()

    def swaping3(self):
        res = cur.execute("""select name from armor where type = 'доспех' and have = 0""").fetchall()
        if res == []:
            name, ok_pressed = QInputDialog.getItem(
                self, "Утверждение", f"Вы уже купили все доспехи",
                ("Ок", "Ок"), 0, False)
        else:
            name, ok_pressed = QInputDialog.getItem(
                self, "Магазин", "Какой доспех хотите купить?",
                (res[i][0] for i in range(len(res))), 0, False)
        if ok_pressed:
            if name == "фариса":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 2000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 2000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 2000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'доспех'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {2000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "лаппа":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 10000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 10000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 10000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'доспех'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {10000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "рыцаря":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 100000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 100000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 100000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'доспех'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {100000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "драконоборца":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 500000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 500000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 500000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'доспех'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {500000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)

        res = cur.execute("""select way, have from armor where have = 2""").fetchall()
        for i in range(20):
            try:
                nice = QPixmap(res[i][0])
                self.labels[i].setPixmap(nice)
            except IndexError:
                pass
        self.interface()

    def swaping4(self):
        res = cur.execute("""select name from armor where type = 'наручи' and have = 0""").fetchall()
        if res == []:
            name, ok_pressed = QInputDialog.getItem(
                self, "Утверждение", f"Вы уже купили все наручники",
                ("Ок", "Ок"), 0, False)
        else:
            name, ok_pressed = QInputDialog.getItem(
                self, "Магазин", "Какие наручи хотите купить?",
                (res[i][0] for i in range(len(res))), 0, False)
        if ok_pressed:
            if name == "фариса":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 2000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 2000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 2000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'наручи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {2000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "лаппа":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 10000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 10000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 10000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'наручи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {10000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "рыцаря":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 100000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 100000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 100000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'наручи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {100000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "драконоборца":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 500000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 500000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 500000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'наручи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {500000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)

        res = cur.execute("""select way, have from armor where have = 2""").fetchall()
        for i in range(20):
            try:
                nice = QPixmap(res[i][0])
                self.labels[i].setPixmap(nice)
            except IndexError:
                pass
        self.interface()

    def swaping5(self):
        res = cur.execute("""select name from armor where type = 'поножи' and have = 0""").fetchall()
        if res == []:
            name, ok_pressed = QInputDialog.getItem(
                self, "Утверждение", f"Вы уже купили все поножи",
                ("Ок", "Ок"), 0, False)
        else:
            name, ok_pressed = QInputDialog.getItem(
                self, "Магазин", "Какие поножи хотите купить?",
                (res[i][0] for i in range(len(res))), 0, False)
        if ok_pressed:
            if name == "фариса":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 2000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 2000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 2000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'поножи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {2000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "лаппа":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 10000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 10000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 10000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'поножи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {10000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "рыцаря":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 100000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 100000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 100000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'поножи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {100000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)
            elif name == "драконоборца":
                res = cur.execute("""select gold from human""").fetchone()
                if res[0] >= 500000:
                    conf, okpress = QInputDialog.getItem(
                        self, "Вопрос", "Вы потратие 500000 голды. Вы уверены?",
                        ("Да", "Нет"), 0, False)
                    if conf == "Да" and okpress:
                        cur.execute("""update human set gold = gold - 500000""")
                        cur.execute("""update armor set have = 2 where name = ? and type = 'поножи'""", (name,))
                        con.commit()
                else:
                    conf, okpress = QInputDialog.getItem(
                        self, "Утверждение", f"Вам нехватает {500000 - res[0]} голды",
                        ("Ок", "Ок"), 1, False)

        res = cur.execute("""select way, have from armor where have = 2""").fetchall()
        for i in range(20):
            try:
                nice = QPixmap(res[i][0])
                self.labels[i].setPixmap(nice)
            except IndexError:
                pass
        self.interface()

    def equipment(self):
        namenig = cur.execute("""select type from armor where have = 1""").fetchall()
        types, okpressed = QInputDialog.getItem(
            self, "Инвентарь", "Что хотите надеть?",
            (namenig[i][0] for i in range(len(namenig))), 0, False)
        if okpressed:
            res = cur.execute("""select name from armor where type = ? and have = 2""", (types,)).fetchall()
            if res == []:
                name, ok_pressed = QInputDialog.getItem(
                    self, "Утверждение", f"У вас нету этого снаряжения",
                    ("Ок", "Ок"), 0, False)
            else:
                name, ok_pressed = QInputDialog.getItem(
                    self, "Инвентарь", f"Какой хотите надеть {types}?",
                    (res[i][0] for i in range(len(res))), 0, False)
                if ok_pressed:
                    # Снятие снаряжения
                    res = cur.execute("""select damage, hp, defense from armor
                                         where have = 1 and type = ?""", (types,)).fetchone()
                    cur.execute("""update human 
                                   set damage = damage - ?, maxhp = maxhp - ?, hp = hp - ?, defense = defense - ?""",
                                   (res[0], res[1], res[1], res[2]))
                    cur.execute("""update armor set have = 2 where have = 1 and type = ?""", (types,))
                    # Надеваю снаряжение
                    cur.execute("""update armor set have = 1 where type = ? and name = ?""", (types, name))
                    res = cur.execute("""select damage, hp, defense from armor where have = 1 and type = ? and
                                         name = ?""", (types, name)).fetchone()
                    cur.execute("""update human 
                                set damage = damage + ?, maxhp = maxhp + ?, hp = hp + ?, defense = defense + ?""",
                                (res[0], res[1], res[1], res[2]))

                    con.commit()

        res = cur.execute("""select way, have from armor where have = 2""").fetchall()
        for i in range(20):
            try:
                nice = QPixmap(res[i][0])
                self.labels[i].setPixmap(nice)
            except IndexError:
                pass

        res = cur.execute("""select way from armor where have = 1""").fetchall()
        for i in range(5):
            weapons = QPixmap(res[i][0])
            self.inventary[i].setPixmap(weapons)

        self.interface()

    def backing(self):
        self.main_view = Main()
        self.main_view.show()
        self.hide()

    def interface(self):
        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {res[0]}/{res[1]}")

        res = cur.execute("""select damage, defense from human""").fetchone()
        self.attack.setText(f"Атака: {res[0]}")
        self.defense.setText(f"Защита: {res[1]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()
        self.exp.setText(f"exp: {expir[0]}/{maxexp}")

        res = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {res[0]}")


class BlackSmith(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi("blacksm.ui", self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.pixmap = QPixmap('heart.png')
        self.heart.setPixmap(self.pixmap)

        self.back.clicked.connect(self.backing)

        self.type.hide()
        self.name.hide()

        self.choose.clicked.connect(self.choice)
        self.lvlup.clicked.connect(self.updating)

        self.interface()

    def choice(self):
        namenig = cur.execute("""select type from armor where have = 1""").fetchall()
        self.types, ok_pressed = QInputDialog.getItem(
            self, "Кузнец", "Какой предмет хотите улучшить?",
            (namenig[i][0] for i in range(len(namenig))), 0, False)
        if ok_pressed:
            res = cur.execute("""select name from armor where type = ? and have = 2""", (self.types,)).fetchall()
            if res == []:
                name, ok_pressed = QInputDialog.getItem(
                    self, "Утверждение", f"У вас нет других предметов",
                    ("Ок", "Ок"), 0, False)
            else:
                self.names, okpressed = QInputDialog.getItem(
                    self, "Кузнец", "Что хотите улучшить?",
                    (res[i][0] for i in range(len(res))), 0, False)
                if res == []:
                    name, ok_pressed = QInputDialog.getItem(
                        self, "Утверждение", f"У вас нет других предметов",
                        ("Ок", "Ок"), 0, False)
                if okpressed:
                    res = cur.execute("""select gold, damage, hp, defense, level from armor
                        where name = ? and type = ?""", (self.names, self.types)).fetchone()
                    self.type.setText(self.types)
                    self.name.setText(self.names)
                    self.gold_lvlup.setText(str(res[0]))
                    self.damage_lvl.setText(f"Урон: {res[1]}")
                    self.hp_lvl.setText(f"Hp: {res[2]}")
                    self.defense_lvl.setText(f"Защита: {res[3]}")
                    self.levels.setText(f"Уровень предмета {res[4]}")
                    self.type.show()
                    self.name.show()

    def updating(self):
        res = cur.execute("""select gold, damage, hp, defense, level from armor
            where name = ? and type = ?""", (self.names, self.types)).fetchone()
        gold = cur.execute("""select gold from human""").fetchone()[0]
        if res[0] > gold:
            name, ok_pressed = QInputDialog.getItem(
                    self, "Утверждение", f"У вас нехватает золота",
                    ("Ок", "Ок"), 0, False)
        else:
            res = cur.execute("""select gold, damage, hp, defense, level from armor
                        where name = ? and type = ?""", (self.names, self.types)).fetchone()
            cur.execute("""update human set gold = gold - ?""", (res[0],))
            res0 = int(res[0] * 1.1)
            res1 = int(res[1] * 1.1)
            res2 = int(res[2] * 1.1)
            res3 = int(res[3] * 1.1)
            res4 = res[4] + 1
            cur.execute("""update armor set gold = ?, damage = ?, 
                        hp = ?, defense = ?, level = ? where name = ? and type = ?""",
                        (res0, res1, res2, res3, res4, self.names, self.types))
            con.commit()
            self.gold_lvlup.setText(str(res0))
            self.damage_lvl.setText(f"Урон: {res1}")
            self.hp_lvl.setText(f"Hp: {res2}")
            self.defense_lvl.setText(f"Защита: {res3}")
            self.levels.setText(f"Уровень предмета {res4}")
        self.interface()

    def backing(self):
        self.main_view = Main()
        self.main_view.show()
        self.hide()

    def interface(self):
        res = cur.execute("""select level from levels where have = 1""").fetchone()
        self.level.setText(f"Уровень: {res[0]}")

        res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {res[0]}/{res[1]}")

        res = cur.execute("""select damage, defense from human""").fetchone()
        self.attack.setText(f"Атака: {res[0]}")
        self.defense.setText(f"Защита: {res[1]}")

        maxexp = cur.execute("""select maxexp from levels where have = 1""").fetchone()[0]
        expir = cur.execute("""select exp from human""").fetchone()
        self.exp.setText(f"exp: {expir[0]}/{maxexp}")

        res = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {res[0]}")


class Shaman(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi("shaman.ui", self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(61, 34, 34))
        self.setPalette(palette)

        self.back.clicked.connect(self.backing)
        self.heal.clicked.connect(self.healing)

        self.goolds = cur.execute("""select gold from human""").fetchone()
        self.gold.setText(f"Золото: {self.goolds[0]}")

        self.res = cur.execute("""select hp, maxhp from human""").fetchone()
        self.hp.setText(f"HP: {self.res[0]}/{self.res[1]}")

        if self.res[1] - self.res[0] <= self.goolds[0]:
            self.heal.setText(f"{self.res[1] - self.res[0]} gold")
            self.name.setText(f"Вылечить {self.res[1] - self.res[0]} hp")
        else:
            self.heal.setText(f"{self.goolds[0]} gold")
            self.name.setText(f"Вылечить {self.goolds[0]} hp")

    def backing(self):
        self.main_view = Main()
        self.main_view.show()
        self.hide()

    def healing(self):
        if self.res[1] - self.res[0] <= self.goolds[0]:
            golds = self.res[1] - self.res[0]
            cur.execute("""update human set hp = maxhp, gold = gold - ?""", (golds,))
            con.commit()
        else:
            cur.execute("""update human set hp = hp + gold, gold = 0 """)
            con.commit()
        self.backing()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())