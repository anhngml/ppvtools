# fuckin-search-engines-how-do-they-work/
import sys
import numpy as np

sys.path.append('./SearchEngine/')
from buildindex import BuildIndex
from querytexts import Query

from conn import conn
from querier import querier, answer


def main(reindex=False):
    # Ngũ Hành Sơn(id: 1594)
    fs_local_streets_query = """SELECT id, name, city_id, district_id FROM fs_local_streets WHERE id = 1594"""
    ans = answer(querier(fs_local_streets_query,
                         one_time_answer=True), auto_decode=True)

    streets = ans.get_answer()

    for street in streets:
        fs_lands_question = """SELECT id, content, title FROM fs_lands WHERE street_id = {}""".format(
            street[0])
        ans = answer(querier(fs_lands_question,
                             one_time_answer=True), auto_decode=True)

        lands = ans.get_answer()

        if lands is None or type(lands[0]) is not tuple:
            continue

        print('\n=====================> Street: {}(id: {})'.format(
            street[1], street[0]))

        lands_arr = np.array(lands, dtype=str)
        lands_title = lands_arr[:, 0:2]
        text_query = Query(lands_title, True)

        compared_ids = []
        for l in range(lands_title.shape[0]):
            text = lands_title[l, 1]
            cur_id = lands_title[l, 0]
            if cur_id in compared_ids:
                continue

            compared_ids.append(cur_id)
            # titles = lands_title[:, 1]
            # text = titles[0]
            num_results = 10

            # tính khoảng cách giữa text so với các text khác có cùng street_id
            # và sắp xếp giảm dần theo khoảng cách
            best_results, ranks = text_query.free_text_query(text)
            # print('Dang liet ke {} ket qua tot nhat cho: \'{}\''.format(
            #     num_results, text))

            # chọn ra chỉ số của num_results texts có khoảng cách gần nhất
            titles = text_query.filenames
            indeces = [i for i, id in enumerate(
                titles[:, 0]) if id in best_results[0:num_results]]

            # lấy texts từ chỉ số đã chọn đc, sắp xếp tăng dần theo khoảng cách để in ra
            suba = list(titles[indeces])
            suba.sort(key=lambda x: best_results.index(x[0]))
            sorted_results = np.array(suba)

            cap = False
            for e, score in zip(sorted_results, ranks):
                if e[0] in compared_ids:
                    continue
                if e[0] != cur_id and score >= .8:
                    compared_ids.append(e[0])
                    if cap == False:
                        print('\n--> Dang liet ke {} ket qua tot nhat cho:\n{} - \'{}\'\n                       ==========vv=========='.format(
                            num_results, cur_id, text))
                        cap = True
                    print(
                        '{} - \'{}\' ::> score {}'.format(e[0], e[1], round(score, 3)))


if __name__ == '__main__':
    main(True)
