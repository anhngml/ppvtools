from querier import querier, answer
from conn import conn
import query_builder
import numpy as np

# fs_members_question = query = """
#         UPDATE fs_members_va_test
#         SET poster_phone='{}', poster_facebook='{}'
#         WHERE id=46
#         """.format('0000', 'facebook facebook')

fs_members_question = query_builder.upsert(
    'fs_members_va_test', id=46, poster_phone='123', poster_facebook='facebook facebook facebook')

print(querier(fs_members_question).perform_task())

ans = None
conn.db.close()
