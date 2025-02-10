# import sqlite3
#
#
# def create_db()
#     conn = sqlite3.connect('item.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS items(
#             Catalog TEXT PRIMARY KEY,
#             Price INTEGER DEFAULT 0
#         )
#     """)
#     conn.commit()
#     conn.close()
#
# item = ''
# while True:
#
#     conn = sqlite3.connect('item.db')
#     cursor = conn.cursor()
#
#     item = input('Введите название: ')
#     if item == 'stop':
#         break
#     price = int(input('Введите цену: '))
#
#     cursor.execute('INSERT OR REPLACE INTO items (Catalog, Price) VALUES (?, ?)', (item, price))
#     conn.commit()
#     conn.close()