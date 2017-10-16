import sys
import numpy as np
from querier import querier, answer
from conn import conn
import query_builder

sys.path.append('./post_classification/')

from bernoulliNB_classifier import Classifier


def main():
    fs_lands_question = """SELECT id, title, content FROM fs_lands WHERE (source_type='facebookcom' AND tin_rac=-1 AND published=0) LIMIT 5000"""
    ans = answer(querier(fs_lands_question,
                         one_time_answer=True), auto_decode=True)

    lands = np.array(ans.get_answer(), dtype=str)
    # texts = np.array(['{} | {}'.format(
    #     a, b) for a, b in zip(lands[:, 1], lands[:, 2])])

    if lands is None:
        return False

    if len(lands.shape) < 1 or lands.shape[0] < 1:
        return False

    texts = np.array([a for a in lands[:, 1]])

    clf = Classifier()
    pred = clf.classify_proba(texts)
    clses = clf.classify(texts)

    # for id, text, proba, cls in zip(lands[:, 0], lands[:, 1], pred, clses):
    for id, proba in zip(lands[:, 0], pred):
        rac = proba[1]
        pub = 2 if rac >= 50 else -1
        if pub == 2:
            query = query_builder.upsert(
                'fs_lands',
                id=int(id),
                tin_rac=proba[1],
                published=2
            )
            querier(query).perform_task()
        else:
            query = query_builder.upsert(
                'fs_lands',
                id=int(id),
                tin_rac=proba[1],
            )
            querier(query).perform_task()

    l_clses = list(clses)
    print('So tin rac: {}\n'.format(l_clses.count(1)))

    return True


if __name__ == '__main__':
    cont = True
    episode_index = 0
    print('\n')
    while cont:
        episode_index += 1
        print('episode {}...\n'.format(episode_index))
        cont = main()

    conn.db.close()
