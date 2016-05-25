# -*- encoding utf-8 -*-
import datetime
import cx_Oracle
from DataException import DataException


class MetaDataService:
    """
    Service to process several database operations on the
    meta data, request table and content table
    """

    def __init__(self, connection):
        """
        Creates a new MetaDataService instance

        :param connection: A connection object (cx_Oracle connection object)
        :return: New MetaDataService
        """
        self.con = connection

    def set_console_logger(self, console_logger):
        """
        Set the console logger

        :param console_logger: logger instance
        """
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        """
        Set the file logger

        :param file_logger: logger instance
        """
        self.__f_logger = file_logger

    def find_all_requests(self):
        """
        Queries all dataset names by the names in the ArcGIS requests table

        :return: Names (List)
        :exception: DataException
        """
        cur = None
        try:
            query = "SELECT r.NAME_OF_DATASET FROM SDE.ARCHIVE_ORDERS_EVW r"

            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None)
            cur.arraysize = 100
            result = cur.fetchall()
            list = []
            for r in result:
                list.append(r[0])
            return list
        except cx_Oracle.DatabaseError as e:
            self.__c_logger.exception("EXCEPTION WHILE finding meta data: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE finding meta data: " + str(e))
            raise DataException("Error while fetching all datasets: " + str(e))
        finally:
            if cur is not None:
                cur.close()

    def meta_data_exists(self, dataset_name):
        """
        Checks the existence of meta data by a given dataset name

        :param name: The dataset name (String)
        :return: (Boolean)
        """
        self.__c_logger.info("Check if in DB: " + str(dataset_name))
        self.__f_logger.info("Check if in DB: " + str(dataset_name))
        cur = None
        try:
            query = "SELECT i.NAME " \
                    "FROM SDE.GDB_ITEMS_VW i LEFT JOIN SDE.GDB_ITEMTYPES t " \
                    "ON i.Type = t.UUID " \
                    "WHERE i.NAME = :data_name " \
                    "AND t.NAME IN ('Feature Dataset', 'Raster Dataset', 'Table', 'Raster Catalog', 'Mosaic Dataset') " \
                    "AND length(i.DOCUMENTATION) > 1 " \
                    "AND i.DOCUMENTATION IS NOT NULL "

            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None, {"data_name": str(dataset_name)})
            result = cur.fetchall()
            if len(result) > 0:
                return True
            return False
        except Exception as e:
            self.__c_logger.exception("EXCEPTION WHILE checking the existence of meta data: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE checking the existence of meta data: " + str(e))
            raise DataException("Error while fetching all datasets: " + str(e))
        finally:
            if cur is not None:
                cur.close()

    def find_meta_data_by_dataset_names(self):
        """
        Queries all xml meta data clobs by the names in the ArcGIS requests table

        :return: Meta data (Dictionary)
        :exception: DataException
        """
        self.__c_logger.info("Find all meta data by dataset name")
        self.__f_logger.info("Find all meta data by dataset name")
        cur = None
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
                self.__c_logger.exception("DATASET FOUND ==> " + str(r))
                metas[r[0]] = r[2].read()
            return metas
        except cx_Oracle.DatabaseError as e:
            self.__c_logger.exception("EXCEPTION WHILE finding meta data by dataset name: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE finding meta data by dataset name: " + str(e))
            raise DataException("Error while fetching all datasets: " + str(e))
        finally:
            if cur is not None:
                cur.close()

    def find_max_id(self):
        """
        Queries the maximum id value in the content table. If no entries are
        available the id will be set to 1

        :return: ID (Integer)
        :exception: DataException
        """
        self.__c_logger.info("Find max id in content table")
        self.__f_logger.info("Find max id in content table")
        cur = None
        dataset_id = -1
        try:
            getId = "SELECT MAX(c.OBJECTID) FROM ARCHIVE_CONTENT_EVW c"
            cur = self.con.cursor()
            cur.prepare(getId)
            cur.execute(None)
            result = cur.fetchall()
            if len(result) > 0:
                for r in result:
                    dataset_id = r[0]
                    break
            self.__c_logger.debug("MAX dataset ID in the content table = " + str(dataset_id))
            if (dataset_id == None):
                self.__c_logger.debug("No entries in content table -> Set id to 0: ID = " + str(dataset_id))
                dataset_id = 0
            return (dataset_id + 1)

        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE finding max id in content table: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE finding max id in content table: " + str(e))
            raise DataException("Exception while fetching max id in " +
                                "SDE.ARCHIVE_ORDERS_EVW:  \n" + str(e))
        finally:
            if cur is not None:
                cur.close()

    def find_id_by_name(self, dataset_name):
        self.__c_logger.info("Find id by name")
        self.__f_logger.info("Find id by name")
        cur = None
        dataset_id = -1
        try:
            getId = "SELECT r.OBJECTID FROM SDE.ARCHIVE_ORDERS_EVW r WHERE r.NAME_OF_DATASET = :data_name"
            cur = self.con.cursor()
            cur.prepare(getId)
            cur.execute(None, {"data_name": dataset_name})
            result = cur.fetchall()
            if len(result) > 0:
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
            if cur is not None:
                cur.close()

    def add_process(self, dataset_name, remarks, org_name):
        """
        Add a new process entry to the content table

        :param dataset_name: Name of the archived dataset (String)
        :param remarks: Notes about the current process state or failure (String)
        :param org_name: The original dataset name (String)
        :return: ID of the entry (Integer)
        :exception: DataException
        """
        self.__c_logger.info("Add process information to the content table")
        self.__f_logger.info("Add process information to the content table")
        cur = None
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
            if cur is not None:
                cur.close()

    def update_state(self, data_id, state):
        """
        Set the state of a row in the content table. The row is found by dataset ID

        :param data_id: Id of the related dataset (Integer)
        :param state: The new value of the state column (String)
        :exception: DataException
        """

        self.__c_logger.info("Update process information to the content table")
        self.__f_logger.info("Update process information to the content table")
        cur = None
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
            if cur is not None:
                cur.close()

    def update_name(self, data_id, name):
        """
        Set the name of a row in the content table. The row is found by dataset ID

        :param data_id: Id of the related dataset (Integer)
        :param name: The new value of the state column (String)
        :exception: DataException
        """

        self.__c_logger.info("Update process information (name) to the content table")
        self.__f_logger.info("Update process information (name) to the content table")
        cur = None
        try:
            query = "UPDATE SDE.ARCHIVE_CONTENT_EVW c SET c.NAME_OF_DATASET = :name WHERE c.OBJECTID = :data_id"
            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None, {'name': name, 'data_id': data_id})
            self.con.commit()
        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE updating process information (name) to the content table: "
                                      + str(e))
            self.__f_logger.exception("EXCEPTION WHILE updating process information (name) to the content table: "
                                      + str(e))
            raise DataException("Exception while updating the name column of SDE.ARCHIVE_CONTENT_EVW: \n" + str(e))
        finally:
            if cur is not None:
                cur.close()

    def delete_by_id(self, data_id):
        """
        Delete a row of the request table by id

        :param data_id: Dataset ID (Integer)
        """
        self.__c_logger.info("Delete request from the request table")
        self.__f_logger.info("Delete request from the request table")

        cur = None
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
            if cur is not None:
                cur.close()
