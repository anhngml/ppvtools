import sys
from conn import conn
from create_unique_members import create_members
from collect_mem_info import collect_members_inf
from update_poster_info import update_poster_inf


def main():
    print('\nChọn tác vụ:\n')
    print('=' * 60)
    print('1: Tạo member (fs_members) từ số ĐT (poster_mobile) \n   trong thông tin dự án (fs_lands)\n')
    print('2: Cập nhật thông tin member từ thông tin dự án (fs_lands)\n')
    print('3: Cập nhật thông tin người đăng cho dự án (fs_lands)\n')
    print('4: Chạy toàn bộ các tác vụ\n')
    print('0: Thoát\n')

    sel = -1
    while sel not in (0, 1, 2, 3, 4):
        if sel != -1:
            print('Lựa chọn không hợp lệ! Mời chọn lại.\n')
        try:
            sel = int(input('Chọn: '))
        except:
            sel = 999

    if sel == 1:
        create_members()
    elif sel == 2:
        collect_members_inf()
    elif sel == 3:
        update_poster_inf()
    elif sel == 4:
        print('1. Tạo members: ' + '=' * 44)
        create_members()
        print('2. Cập nhật thông tin members: ' + '=' * 29)
        collect_members_inf()
        print('3. Cập nhật thông tin posters: ' + '=' * 29)
        update_poster_inf()
    elif sel == 0:
        conn.db.close()
        sys.exit()
    print('*' * 60)


if __name__ == '__main__':
    cont = True
    while cont:
        main()
        cont = input('Bạn có muốn tiếp tục không?(y/n): ') == 'y'
    conn.db.close()
