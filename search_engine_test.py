# http://aakashjapi.com/fuckin-search-engines-how-do-they-work/
import sys
import numpy as np

sys.path.append('./TextSearchEngine/')
from buildindex import BuildIndex
from querytexts import Query

from conn import conn
from querier import querier, answer


def main(reindex=False):
    fs_local_streets_query = """SELECT id, name, city_id, district_id FROM fs_local_streets"""
    ans = answer(querier(fs_local_streets_query,
                         one_time_answer=True), auto_decode=True)

    streets = ans.get_answer()

    for street in streets:
        fs_lands_question = """SELECT id, title FROM fs_lands WHERE street_id = {}""".format(
            street[0])
        ans = answer(querier(fs_lands_question,
                             one_time_answer=True), auto_decode=True)

        lands = ans.get_answer()

        if lands is None or type(lands[0]) is not tuple:
            continue

        print('street: {}(id: {})\n'.format(street[1], street[0]))

        lands_arr = np.array(lands, dtype=str)
        titles = lands_arr[:, 0:2]
        text_query = Query(titles, True)

        # text = u'Cho thuê nhà đường Trường Chinh'
        text = titles[0][1]
        num_results = 5

        best_results = text_query.free_text_query(text)
        print('Dang liet ke {} ket qua tot nhat: \n'.format(num_results))

        titles = text_query.filenames
        indeces = [i for i, id in enumerate(
            titles[:, 0]) if id in best_results[0:num_results]]

        suba = list(titles[indeces])
        suba.sort(key=lambda x: best_results.index(x[0]))
        sorted_results = np.array(suba)
        for e in sorted_results:
            print('{} - {}'.format(e[0], e[1]))

    return

    if reindex:
        # fs_lands_question = """SELECT id, title, alias, image, category_name, project_name, home_number, city_id, city_name, district_id, district_name, street_id, street_name, ward_id, ward_name, land_lat, land_lng, poster_id, poster_name, poster_mobile, content FROM fs_lands"""

        fs_lands_question = """SELECT id, title FROM fs_lands LIMIT 4000"""

        print('Dang lay danh sach bat dong san...\n')
        ans = answer(querier(fs_lands_question,
                             one_time_answer=True), auto_decode=True)

        lands = ans.get_answer()
        lands_arr = np.array(lands, dtype=str)
        titles = lands_arr[:, 0:2]
        print('Da tai xuong {} bat dong san, dang lap chi muc...\n'.format(len(lands)))
        text_query = Query(titles, True)
        print('Hoan thanh viec lap chi muc! San sang cho viec tim kiem\n')
    else:
        text_query = Query(None, False)
        print('Hoan thanh viec load chi muc! San sang cho viec tim kiem\n')

    text = u'Cho thuê nhà đường Trường Chinh'
    print(u"""Dang tim cac bat dong san gan giong voi '{}'{}""".format(
        text, '\n'))
    num_results = 5

    print('Dang truy van...\n')
    best_results = text_query.free_text_query(text)
    print('Dang liet ke {} ket qua tot nhat: \n'.format(num_results))

    titles = text_query.filenames
    indeces = [i for i, id in enumerate(
        titles[:, 0]) if id in best_results[0:num_results]]
    suba = list(titles[indeces])
    suba.sort(key=lambda x: best_results.index(x[0]))
    sorted_results = np.array(suba)
    for e in sorted_results:
        print('{} - {}'.format(e[0], e[1]))

    print('\n')


if __name__ == '__main__':
    main(True)
