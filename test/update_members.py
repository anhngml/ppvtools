import _mysql
from MySQLdb.constants import FIELD_TYPE

my_conv = {FIELD_TYPE.LONG: int,
           FIELD_TYPE.VARCHAR: str}
# my_conv = {}

db = _mysql.connect(host="timnhaviet.vn", user="timnhaviet",
                    passwd="vNUH7dfk", db="timnhaviet", conv=my_conv)

db.query("""SELECT poster_id, 
				poster_name,
				poster_avatar,
				poster_address,
				poster_phone,
				poster_email,
				poster_mobile,
				poster_avarta,
				poster_background_color,	
				poster_text_color,
				poster_facebook 
                FROM fs_lands_va_test 
                WHERE poster_mobile IS NOT NULL AND poster_mobile <> \'\'""")

# r = db.store_result()
# ...or...
rows = db.use_result()

first_row = rows.fetch_row()[0]

type_fixed_row = tuple([el.decode('utf-8') if type(el)
                        is bytes else el for el in first_row])

# print(first_row)
print(type_fixed_row)

db.close()
