import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from querier import querier, answer
from conn import conn
import query_builder
from tqdm import tqdm

EXCLUDES = [
    'simthanglongvn@gmail.com',
    'khosimtructuyen.com@gmail.com',
    'toan85dalat@gmail.com',
    'info@timnhaviet.vn',
    'hotro@sanchinhchu.net',
    'simvina.net@gmail.com',
    'hotro@batdongsan.com',
    'contact@alonhadat.com'
]


def SearchEmail(mobileNum, firstResult=True):
    page = requests.get(
        "https://www.google.com/search?q={}+email".format(mobileNum))
    html = page.content

    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()

    if text.find('solving the above CAPTCHA') > 0:
        print('\n\nRequest bị nhận dạng là auto bot! dừng chương trình và thử lại sau!')
        while(True):
            read = input('')

    match = re.findall(
        r'[\w\.-]+@[\w\.-]+com|[\w\.-]+@[\w\.-]+net|[\w\.-]+@[\w\.-]+vn', text)

    filter_match = [s for s in match if s not in EXCLUDES]
    match = filter_match
    if len(match) < 1:
        return ''

    if firstResult:
        gmailCom = [x for x in match if x.endswith('gmail.com')]
        if len(gmailCom) > 0:
            return gmailCom[0]
        else:
            return match[0]
    else:
        return '|'.join(match)


def find_member_emails():
    fs_members_question = """SELECT id, poster_name, poster_mobile FROM fs_members WHERE (email IS NULL OR email = '') AND (poster_mobile IS NOT NULL AND poster_mobile <> '')"""

    # =========== lay danh sach member. sua lai dinh dang so dien thoai ===============
    print('Đang lấy danh sách members...\n')
    ans = answer(querier(fs_members_question,
                         one_time_answer=True), auto_decode=True)

    members = np.array(ans.get_answer(), dtype=str)

    m_mobiles = np.char.replace(members[:, 2], ' ', '')
    m_mobiles = np.char.replace(m_mobiles, '.', '')
    m_mobiles = np.char.replace(m_mobiles, '+84', '0')
    m_mobiles = np.char.replace(m_mobiles, '/', ',')
    m_mobiles = np.char.replace(m_mobiles, '-', ',')

    members[:, 2] = m_mobiles

    print('Có {} members hợp lệ\n'.format(len(m_mobiles)))
    updated_count = 0
    if members is not None and len(members) > 0:
        for i in tqdm(range(len(members))):
            next_mem = members[i]
            mem_mobile = next_mem[2]
            mem_email = SearchEmail(mem_mobile, False)
            mem_id = next_mem[0]

            if mem_email != '':
                query = query_builder.upsert(
                    'fs_members',
                    id=int(mem_id),
                    emails_auto=mem_email,
                    auto_find_email=1
                )
                querier(query).perform_task()
                updated_count += 1

    print('Tìm được tổng số {} emails'.format(updated_count))


if __name__ == '__main__':
    # print(SearchEmail('0978000831', True))
    find_member_emails()
