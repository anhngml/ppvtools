from conn import conn


class querier:
    def __init__(self, question, one_time_answer=False):
        self.question = question
        self.one_time_answer = one_time_answer

    def get_answer(self):
        db = conn.get_db()
        db.query(self.question)
        if self.one_time_answer:
            while True:
                rows = db.store_result()
                if rows is None:
                    return None
                while True:
                    yield rows.fetch_row(how=1, maxrows=0)
        else:
            rows = db.use_result()
            if rows is None:
                return None
            while True:
                yield rows.fetch_row()

    def perform_task(self):
        db = conn.get_db()
        db.query(self.question)
        return db.insert_id()


class answer:
    ans = None

    @property
    def isEmpty(self):
        return self.empty

    empty = False

    def __init__(self, the_querier, auto_decode=False):
        self.the_querier = the_querier
        self.auto_decode = auto_decode

    def get_answer(self):
        if self.the_querier is None:
            return None
        else:
            if self.ans is None:
                self.ans = self.the_querier.get_answer()
        if self.ans is None:
            return None

        try:
            rows = next(self.ans)
            if self.auto_decode:
                if len(rows) < 1:
                    return None
                if type(rows[0]) is tuple:
                    try:
                        result = tuple([tuple([el.decode('utf-8') if el is not None and type(el)
                                               is bytes else el for el in row]) for row in rows])
                    except UnicodeDecodeError:
                        result = tuple([tuple([str(el).replace('b\'', '')[:-1] if el is not None and type(el)
                                               is bytes else el for el in row]) for row in rows])
                elif type(rows[0]) is dict:
                    try:
                        result = tuple([tuple([el.decode('utf-8') if el is not None and type(el)
                                               is bytes else el for el in row.values()]) for row in rows])
                    except UnicodeDecodeError:
                        result = tuple([tuple([str(el).replace('b\'', '')[:-1] if el is not None and type(el)
                                               is bytes else el for el in row.values()]) for row in rows])
            else:
                result = rows
            # if len(result) == 1:
            #     result = result[0]
            return result
        except StopIteration:
            self.empty = True
            self.the_querier = None
            return self.isEmpty
        except:
            self.the_querier = None
            raise
