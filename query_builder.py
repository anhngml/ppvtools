"""
Su dung:
>>> upsert("tbl", LogID=500, LoggedValue=5)
"INSERT INTO tbl (LogID, LoggedValue) VALUES ('500', '5') ON DUPLICATE KEY UPDATE LogID = '500', LoggedValue = '5';"

>>> read("tbl", **{"username": "morten"})
"SELECT * FROM tbl WHERE username = 'morten';"

>>> read("tbl", **{"user_type": 1, "user_group": "admin"})
"SELECT * FROM tbl WHERE user_type = '1' AND user_group = 'admin';"
"""


def read(table, **kwargs):
    """ Generates SQL for a SELECT statement matching the kwargs passed. """
    sql = list()
    sql.append("SELECT * FROM %s " % table)
    if kwargs:
        sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v)
                                           for k, v in kwargs.items()))
    sql.append(";")
    return "".join(sql)


def upsert(table, **kwargs):
    """ update/insert rows into objects table (update if the row already exists)
        given the key-value pairs in kwargs """
    keys = ["%s" % k for k in kwargs]
    values = ["'%s'" % v for v in kwargs.values()]
    sql = list()
    sql.append("INSERT INTO %s (" % table)
    sql.append(", ".join(keys))
    sql.append(") VALUES (")
    sql.append(", ".join(values))
    sql.append(") ON DUPLICATE KEY UPDATE ")
    sql.append(", ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
    sql.append(";")
    return "".join(sql)


def delete(table, **kwargs):
    """ deletes rows from table where **kwargs match """
    sql = list()
    sql.append("DELETE FROM %s " % table)
    sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v)
                                       for k, v in kwargs.items()))
    sql.append(";")
    return "".join(sql)
