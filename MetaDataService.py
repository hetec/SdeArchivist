# -*- encoding utf-8 -*-
import cx_Oracle
import OracleConnection


class MetaDataService:
    """
    A service to get the metadata of flagged sde data from the oracle database
    """

    def __init__(self, connection):
        """
        Creates a new MetaDataService

        :param connection: A connection object (cx_Oracle connection object)
        :return: New MetaDataService
        """
        self.con = connection

    def find_flagged_meta_data(self):
        """
        Finds alle meta data in the defined oracle database which are marked by a flag

        :return: Meta data as dictionary {name : meta data xml string}
        """
        query = "select i.NAME, t.NAME, i.DOCUMENTATION from SDE.GDB_ITEMS_VW i left join SDE.GDB_ITEMTYPES t " \
                "on i.Type = t.UUID " \
                "where DBMS_LOB.instr(i.DOCUMENTATION, :flag) > 0 " \
                "and t.NAME = :name " \
                "and length(i.DOCUMENTATION) > 1 " \
                "and i.DOCUMENTATION is not null"

        cur = self.con.cursor()
        cur.prepare(query)
        cur.execute(None, {'name':'Feature Dataset','flag':'DRP=true'})
        cur.arraysize = 100
        result = cur.fetchall()
        metas = {}
        for r in result:
            metas[r[0]] = r[2].read()
        cur.close()
        return metas

