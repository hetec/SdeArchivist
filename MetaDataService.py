# -*- encoding utf-8 -*-
import cx_Oracle
import OracleConnection
import datetime


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

    def find_all_requests(self):
        """
        Queries all dataset names by the names in the ArcGIS requests table
        :return: Names (List)
        """

        query = "SELECT r.NAME_OF_DATASET FROM SDE.ARCHIVE_REQUESTS r"

        cur = self.con.cursor()
        cur.prepare(query)
        cur.execute(None)
        cur.arraysize = 100
        result = cur.fetchall()
        list = []
        for r in result:
            list.append(r)
        cur.close()
        return list

    def find_meta_data_by_dataset_names(self):
        """
        Queries all xml meta data clobs by the names in the ArcGIS requests table
        :return: Meta data (Dictionary)
        """

        query = "SELECT i.NAME, t.NAME, i.DOCUMENTATION " \
                "FROM SDE.GDB_ITEMS_VW i LEFT JOIN SDE.GDB_ITEMTYPES t " \
                "ON i.Type = t.UUID " \
                "WHERE i.NAME in (SELECT r.NAME_OF_DATASET FROM SDE.ARCHIVE_REQUESTS r)" \
                "AND t.NAME in ('Feature Dataset') " \
                "AND length(i.DOCUMENTATION) > 1 " \
                "AND i.DOCUMENTATION IS NOT NULL "

        cur = self.con.cursor()
        cur.prepare(query)
        cur.execute(None)
        cur.arraysize = 100
        result = cur.fetchall()
        metas = {}
        for r in result:
            metas[r[0]] = r[2].read()
        cur.close()
        return metas

    def add_process(self, dataset_name, remarks, org_name):

        try:

            getId = "SELECT r.OBJECTID FROM SDE.ARCHIVE_REQUESTS r WHERE r.NAME_OF_DATASET = :data_name"

            cur1 = self.con.cursor()
            cur1.prepare(getId)
            cur1.execute(None, {'data_name': dataset_name})
            result = cur1.fetchall()

            for r in result:
                print "ID: " + str(r[0])
                dataset_id = r[0]

            dataset_id = 1

            query = "INSERT INTO " \
                    "SDE.ARCHIVE_CONTENT " \
                    "(OBJECTID, NAME_OF_DATASET, DATE_OF_ARCHIVING, REMARKS, NAME_OF_DATASET_ORIGINAL) " \
                    "VALUES (:data_id, :data_name, :req_date, :remarks, :org)"

            cur2 = self.con.cursor()
            cur_date = datetime.date.today()
            cur2.prepare(query)
            cur2.execute(None, {'data_id': dataset_id, 'data_name': dataset_name, 'req_date': cur_date, 'remarks': remarks, 'org': org_name})
            self.con.commit()
            return dataset_id
        except Exception as e:
            raise Exception(e)
            self.con.rollback()
        finally:
            cur1.close()
            cur2.close()

    def update_state(self, id, state):

        try:
            query = "UPDATE SDE.ARCHIVE_CONTENT c SET c.REMARKS = :state WHERE c.OBJECTID = :data_id"

            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None, {'state':state, 'data_id':id})
            self.con.commit()
        except:
            self.con.rollback()
        finally:
            cur.close()

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

