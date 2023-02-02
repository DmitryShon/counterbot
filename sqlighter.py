import sqlite3
class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def check_user_in_db(self, tg_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `user` WHERE `tg_id` = ?', (tg_id,)).fetchall()
            return bool(len(result))

    def add_user(self, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `user` (`tg_id`) VALUES(?)", (tg_id,))

    def add_account(self,account,tg_id):
        with self.connection:
            user_id = self.cursor.execute('SELECT `id` FROM `user` WHERE `tg_id` = ?', (tg_id,)).fetchone()[0]
            if account not in self.show_accounts(tg_id):
                self.cursor.execute("INSERT INTO `account` (`account`, `user_id`) VALUES(?,?)", (account, user_id))
                return True
            else:
                return False

    def del_account(self,account,tg_id):
        with self.connection:
            user_id = self.cursor.execute('SELECT `id` FROM `user` WHERE `tg_id` = ?', (tg_id,)).fetchone()[0]
            return self.cursor.execute("DELETE FROM `account` WHERE account = ? and user_id = ?", (account,user_id))

    def all_users(self):
        with self.connection:
            return self.cursor.execute('select * from user').fetchall()

    def show_accounts(self,tg_id):
        accounts = []
        with self.connection:
            user_id = self.cursor.execute('SELECT `id` FROM `user` WHERE `tg_id` = ?', (tg_id,)).fetchone()[0]
            try:
                accounts_raw = self.cursor.execute('SELECT `account` FROM `account` WHERE `user_id`=?',(user_id,)).fetchall()
                accounts = [i[0] for i in accounts_raw]
            except:
                pass
            return accounts
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

db = SQLighter('db.db')
db.del_account('test','554157175')