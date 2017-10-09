from querier import querier, answer
from conn import conn
import query_builder
import numpy as np
import datetime


def create_members():
    fs_lands_question = """SELECT id, poster_id, poster_name, poster_avatar, poster_address, poster_phone, poster_email, poster_mobile, poster_avarta, poster_background_color, poster_text_color, poster_facebook FROM fs_lands WHERE poster_mobile IS NOT NULL AND poster_mobile <> '' AND (poster_id IS NULL OR poster_id = 0)"""
    # GROUP BY poster_mobile
    # fs_lands_question = query_builder.read('fs_lands_va_test', )

    fs_members_question = "SELECT id, code, email, poster_name, poster_mobile, poster_address FROM fs_members"

    ans = answer(querier(fs_members_question,
                         one_time_answer=True), auto_decode=True)

    members = np.array(ans.get_answer(), dtype=str)

    mobiles = np.char.replace(members[:, 4], ' ', '')
    mobiles = np.char.replace(mobiles, '.', '')
    mobiles = np.char.replace(mobiles, '+84', '0')

    members[:, 4] = mobiles

    # ============= Duyet qua fs_lands
    print('Đang lấy danh sách lands...\n')
    ans = answer(querier(fs_lands_question,
                         one_time_answer=True), auto_decode=True)

    lands = ans.get_answer()

    if lands is not None and len(lands) > 0:

        if type(lands[0]) != tuple:
            lands = tuple([tuple([el for el in lands])])

        print('Có {} lands hợp lệ\n'.format(len(lands)))
        print('Bắt đầu tạo members...\n')
        for next_land in lands:
            p_mobile = next_land[7].replace(
                '+84', '0').replace('.', '').replace(' ', '').replace('/', ',').replace('-', ',')
            p_mobi_splited = np.array(p_mobile.split(','), dtype=str)
            p_mobi_splited = p_mobi_splited[p_mobi_splited != '']
            joined_mobil = ','.join([str(x) for x in p_mobi_splited])
            mask = np.in1d(mobiles, np.append(p_mobi_splited, joined_mobil))
            match = np.where(mask)[0]

            if len(match) == 0:  # chua ton tai member trong fs_members
                # TODO chen member
                query = query_builder.upsert(
                    'fs_members', id='',
                    email=next_land[6],
                    poster_name=next_land[2],  # .replace("""'""", """\'"""),
                    poster_mobile=joined_mobil,
                    poster_address=next_land[4],
                    created_time=datetime.datetime.now())

                new_id = querier(query).perform_task()
                mobiles = np.append(mobiles, [joined_mobil])
                members = np.concatenate(
                    (members, [[new_id, '', next_land[6], next_land[2], joined_mobil, next_land[4]]]), axis=0)
                query = query_builder.upsert(
                    'fs_lands',
                    id=next_land[0],
                    poster_id=new_id)
                querier(query).perform_task()
                print('Create new member with ID: {}; Email: {}; Mobile: {} @ land_id: {}'.format(
                    new_id, next_land[6], joined_mobil, next_land[0]))
            else:
                # TODO sync member id trong fs_members va fs_lands
                mem = members[match[0]][:]
                query = query_builder.upsert(
                    'fs_lands',
                    id=next_land[0],
                    poster_id=mem[0])
                querier(query).perform_task()

                print('Link land ID: {} with member ID: {}'.format(
                    next_land[0], mem[0]))

            # next_land = ans.get_answer()
        print('\n\nHoàn thành cập nhật!\n')
    else:
        print('Không có member mới! Kết thúc công việc')

    ans = None


if __name__ == '__main__':
    create_members()
    conn.db.close()
