from querier import querier, answer
from conn import conn
import query_builder
import numpy as np
from tqdm import tqdm
from search_email import SearchEmail


def collect_members_inf():
    fs_lands_question = """SELECT id, poster_id, poster_name, poster_avatar, poster_address, poster_phone, poster_email, poster_mobile, poster_avarta, poster_background_color, poster_text_color, poster_facebook FROM fs_lands WHERE poster_mobile IS NOT NULL AND poster_mobile <> ''"""  # AND (poster_id IS NOT NULL AND poster_id <> 0)"""

    fs_members_question = """SELECT id, code, email, poster_avatar, poster_name, poster_mobile, poster_phone, poster_address, poster_facebook, background_color, text_color FROM fs_members"""

    # =========== lay danh sach member. sua lai dinh dang so dien thoai ===============
    print('Đang lấy danh sách members...\n')
    ans = answer(querier(fs_members_question,
                         one_time_answer=True), auto_decode=True)

    members = np.array(ans.get_answer(), dtype=str)

    m_mobiles = np.char.replace(members[:, 5], ' ', '')
    m_mobiles = np.char.replace(m_mobiles, '.', '')
    m_mobiles = np.char.replace(m_mobiles, '+84', '0')
    m_mobiles = np.char.replace(m_mobiles, '/', ',')
    m_mobiles = np.char.replace(m_mobiles, '-', ',')

    members[:, 5] = m_mobiles

    print('Có {} members hợp lệ\n'.format(len(m_mobiles)))

    # char_m_mobils = np.chararray(m_mobiles.shape, 50)
    # char_m_mobils[:] = m_mobiles[:]
    # char_m_mobils = char_m_mobils.astype(str)

    # split = lambda t: np.array(t.split(','))
    # m_mobils = split(char_m_mobils)

    # members = np.array(members)
    # members[:, 4] = np.array(m_mobils)

    # =========== lay danh sach land. sua lai dinh dang so dien thoai ===============
    print('Đang lấy danh sách lands...\n')
    ans = answer(querier(fs_lands_question,
                         one_time_answer=True), auto_decode=True)

    lands = np.array(ans.get_answer(), dtype=str)

    l_mobiles = np.char.replace(lands[:, 7], ' ', '')
    l_mobiles = np.char.replace(l_mobiles, '.', '')
    l_mobiles = np.char.replace(l_mobiles, '+84', '0')
    l_mobiles = np.char.replace(l_mobiles, '/', ',')
    l_mobiles = np.char.replace(l_mobiles, '-', ',')

    lands[:, 7] = l_mobiles
    print('Có {} lands hợp lệ\n'.format(len(l_mobiles)))

    def f(x): return '' if (x == 'None') else x

    f = np.vectorize(f)

    lands = f(lands)
    # =========== cap nhat thuoc tinh members ===============
    print('Bắt đầu cập nhật thông tin members...\n')
    if members is not None and len(members) > 0:
        for i in tqdm(range(len(members))):
            next_mem = members[i]
            # for next_mem in members:
            m_mobil = next_mem[5]
            m_mobil_splited = np.array(m_mobil.split(','), dtype=str)
            m_mobil_splited = m_mobil_splited[m_mobil_splited != '']
            joined_mobil = ','.join([str(x) for x in m_mobil_splited])
            mask = np.in1d(l_mobiles, np.append(m_mobil_splited, joined_mobil))
            match = np.where(mask)[0]
            if len(match) > 0:
                # print(match)
                # if len(match) > 1:
                match_lands = lands[match][:]

                poster_id = next_mem[0]
                poster_email = '' if next_mem[2] == 'None' else next_mem[2]
                poster_avatar = '' if next_mem[3] == 'None' else next_mem[3]
                poster_name = '' if next_mem[4] == 'None' else next_mem[4]
                # poster_mobile = ''
                poster_phone = '' if next_mem[6] == 'None' else next_mem[6]
                poster_address = '' if next_mem[7] == 'None' else next_mem[7]
                poster_facebook = '' if next_mem[8] == 'None' else next_mem[8]
                background_color = '' if next_mem[9] == 'None' else next_mem[9]
                text_color = '' if next_mem[10] == 'None' else next_mem[10]

                for m_land in match_lands:
                    poster_email = m_land[6] if poster_email == '' else poster_email
                    poster_avatar = m_land[3] if poster_avatar == '' else poster_avatar
                    poster_name = m_land[2] if poster_name == '' else poster_name
                    poster_phone = m_land[5] if poster_phone == '' else poster_phone
                    poster_address = m_land[4] if poster_address == '' else poster_address
                    poster_facebook = m_land[11] if poster_facebook == '' else poster_facebook
                    background_color = m_land[9] if background_color == '' else background_color
                    text_color = m_land[10] if text_color == '' else text_color

                if poster_email == '':
                    poster_email = SearchEmail(m_mobil)

                query = query_builder.upsert(
                    'fs_members',
                    id=int(poster_id),
                    email=poster_email,
                    poster_avatar=poster_avatar,
                    poster_name=poster_name,
                    poster_phone=poster_phone,
                    poster_address=poster_address,
                    poster_facebook=poster_facebook,
                    background_color=background_color,
                    text_color=text_color
                )
                # print(query)
                querier(query).perform_task()

    ans = None
    print('\n\nHoàn thành cập nhật!\n')


if __name__ == '__main__':
    collect_members_inf()
    conn.db.close()
