# -*- encoding utf-8 -*-
import datetime
import cx_Oracle
from DataException import DataException


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

    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger


    def find_all_requests(self):
        """
        Queries all dataset names by the names in the ArcGIS requests table
        :return: Names (List)
        """

        query = "SELECT r.NAME_OF_DATASET FROM SDE.ARCHIVE_ORDERS_EVW r"

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
        self.__c_logger.info("Find meta data by dataset name")
        self.__f_logger.info("Find meta data by dataset name")
        try:
            query = "SELECT i.NAME, t.NAME, i.DOCUMENTATION " \
                    "FROM SDE.GDB_ITEMS_VW i LEFT JOIN SDE.GDB_ITEMTYPES t " \
                    "ON i.Type = t.UUID " \
                    "WHERE i.NAME IN (SELECT r.NAME_OF_DATASET FROM SDE.ARCHIVE_ORDERS_EVW r)" \
                    "AND t.NAME IN ('Feature Dataset', 'Raster Dataset', 'Table', 'Raster Catalog', 'Mosaic Dataset') " \
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
            return metas
        except cx_Oracle.DatabaseError as e:
            self.__c_logger.exception("EXCEPTION WHILE finding meta data by dataset name: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE finding meta data by dataset name: " + str(e))
            raise DataException("Error while fetching all datasets: " + str(e))
        finally:
            cur.close()

    def find_max_id(self):
        self.__c_logger.info("Find max id in content table")
        self.__f_logger.info("Find max id in content table")
        try:
            #getId = "SELECT r.OBJECTID FROM SDE.ARCHIVE_ORDERS_EVW r WHERE r.NAME_OF_DATASET = :data_name"
            getId = "SELECT MAX(c.OBJECTID) FROM ARCHIVE_CONTENT_EVW c"
            cur = self.con.cursor()
            cur.prepare(getId)
            cur.execute(None)
            result = cur.fetchall()
            if len(result) <= 0:
                dataset_id = -1
            else:
                for r in result:
                    dataset_id = r[0]
                    break

            return (dataset_id + 1)

        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE finding max id in content table: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE finding max id in content table: " + str(e))
            raise DataException("Exception while fetching max id in "
                                + "SDE.ARCHIVE_ORDERS_EVW:  \n" + str(e))
        finally:
            cur.close()

    def find_id_by_name(self, dataset_name):
        self.__c_logger.info("Find id by name")
        self.__f_logger.info("Find id by name")
        try:
            getId = "SELECT r.OBJECTID FROM SDE.ARCHIVE_ORDERS_EVW r WHERE r.NAME_OF_DATASET = :data_name"
            cur = self.con.cursor()
            cur.prepare(getId)
            cur.execute(None, {"data_name": dataset_name})
            result = cur.fetchall()
            if len(result) <= 0:
                dataset_id = -1
            else:
                for r in result:
                    dataset_id = r[0]
                    break

            return dataset_id

        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE finding id by name: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE finding id by name: " + str(e))
            raise DataException("Exception while fetching id for "
                                + dataset_name
                                + " from SDE.ARCHIVE_ORDERS_EVW:  \n" + str(e))
        finally:
            cur.close()

    def add_process(self, dataset_name, remarks, org_name):
        self.__c_logger.info("Add process information to the content table")
        self.__f_logger.info("Add process information to the content table")
        did = self.find_max_id()

        try:
            query = "INSERT INTO " \
                    "SDE.ARCHIVE_CONTENT_EVW " \
                    "(OBJECTID, NAME_OF_DATASET, DATE_OF_ARCHIVING, REMARKS, NAME_OF_DATASET_ORIGINAL) " \
                    "VALUES (:data_id, :data_name, :req_date, :remarks, :org)"
            cur = self.con.cursor()
            cur_date = datetime.date.today()
            cur.prepare(query)
            cur.execute(None, {'data_id': did, 'data_name': dataset_name, 'req_date': cur_date, 'remarks': remarks,
                               'org': org_name})
            self.con.commit()
            return did
        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE adding process information to the content table: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE adding process information to the content table: " + str(e))
            raise DataException("Exception while adding a process to SDE.ARCHIVE_CONTENT_EVW: \n" + str(e))
        finally:
            cur.close()

    def update_state(self, data_id, state):
        self.__c_logger.info("Update process information to the content table")
        self.__f_logger.info("Update process information to the content table")
        try:
            query = "UPDATE SDE.ARCHIVE_CONTENT_EVW c SET c.REMARKS = :state WHERE c.OBJECTID = :data_id"
            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None, {'state': state, 'data_id': data_id})
            self.con.commit()
        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE updating process information to the content table: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE updating process information to the content table: " + str(e))
            raise DataException("Exception while updating the state column of SDE.ARCHIVE_CONTENT_EVW: \n" + str(e))
        finally:
            cur.close()

    def delete_by_id(self, data_id):
        self.__c_logger.info("Delete request from the request table")
        self.__f_logger.info("Delete request from the request table")
        try:
            query = "DELETE FROM SDE.ARCHIVE_ORDERS_EVW WHERE OBJECTID = :data_id"
            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None, {'data_id': data_id})
            self.con.commit()

        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE deleting request from the request table: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE deleting request from the request table: " + str(e))
            raise DataException("Exception while deleteing the id "
                                + str(data_id)
                                + " column of SDE.ARCHIVE_ORDERS_EVW: \n" + e)
        finally:
            cur.close()

    def find_flagged_meta_data(self):
        """
        Finds alle meta data in the defined oracle database which are marked by a flag

        :return: Meta data as dictionary {name : meta data xml string}
        """
        query = "SELECT i.NAME, t.NAME, i.DOCUMENTATION FROM SDE.GDB_ITEMS_VW i LEFT JOIN SDE.GDB_ITEMTYPES t " \
                "ON i.Type = t.UUID " \
                "WHERE DBMS_LOB.instr(i.DOCUMENTATION, :flag) > 0 " \
                "AND t.NAME = :name " \
                "AND length(i.DOCUMENTATION) > 1 " \
                "AND i.DOCUMENTATION IS NOT NULL"

        cur = self.con.cursor()
        cur.prepare(query)
        cur.execute(None, {'name': 'Feature Dataset', 'flag': 'DRP=true'})
        cur.arraysize = 100
        result = cur.fetchall()
        metas = {}
        for r in result:
            metas[r[0]] = r[2].read()
        cur.close()
        return metas
