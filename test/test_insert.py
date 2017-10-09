from querier import querier, answer
from conn import conn
import numpy as np

fs_members_question = query = """
        INSERT INTO fs_members_va_test
        (`poster_mobile`, `poster_name`)
        VALUES
        ('010101', 'name 1'),
        ('020202', 'name 2'),
        ('030303', 'name 3')
        """

querier(fs_members_question).perform_task()
ans = None
conn.db.close()
