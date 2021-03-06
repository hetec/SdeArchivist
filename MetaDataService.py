# -*- encoding utf-8 -*-
import datetime
import cx_Oracle
from DataException import DataException


class MetaDataService:
    """
    Service to process several database operations on the
    meta data, request table and content table
    """

    def __init__(self, connection, archive_connection, db_config, arch_config):
        """
        Creates a new MetaDataService instance

        :param connection: A connection object (cx_Oracle connection object)
        :param archive_connection: A connection object for the archive db (cx_Oracle connection object)
        :param db_config: Database configuration values
        :param arch_config: Archive database configuration values
        :return: New MetaDataService
        """
        self.con = connection
        self.a_con = archive_connection
        self.db_config = db_config
        self.arch_config = arch_config

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
            query = "SELECT r.NAME_OF_DATASET FROM SDE." + self.db_config["request_table"] + " r"

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
            raise DataException("Error while fetching all data sets: " + str(e))
        finally:
            if cur is not None:
                cur.close()

    def meta_data_exists(self, dataset_name):
        """
        Checks the existence of meta data by a given dataset name

        :param name: The dataset name (String)

        :return: (Boolean)
        :exception: DataException
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
        Queries all XML meta data CLOBS by the names in the ArcGIS REQUEST table

        :return: Meta data (Dictionary)
        :exception: DataException
        """
        self.__c_logger.info("Find all meta data for all data set names")
        self.__f_logger.info("Find all meta data for all data set names")
        cur = None
        try:
            query = "SELECT i.NAME, t.NAME, i.DOCUMENTATION " \
                    "FROM SDE.GDB_ITEMS_VW i LEFT JOIN SDE.GDB_ITEMTYPES t " \
                    "ON i.Type = t.UUID " \
                    "WHERE i.NAME IN (SELECT r.NAME_OF_DATASET FROM SDE." + self.db_config["request_table"] + " r)" \
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
                self.__c_logger.info("DATASET FOUND ==> " + str(r))
                metas[r[0]] = r[2].read()
            return metas
        except cx_Oracle.DatabaseError as e:
            self.__c_logger.exception("Error while fetching all data sets: " + str(e))
            self.__f_logger.exception("Error while fetching all data sets: " + str(e))
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
            getId = "SELECT MAX(c.OBJECTID) FROM SDE." + self.db_config["content_table"] + " c"
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
            getId = "SELECT r.OBJECTID FROM SDE." + self.db_config["request_table"] + " r WHERE r.NAME_OF_DATASET = :data_name"
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
                    "SDE." + self.db_config["content_table"] + \
                    " (OBJECTID, NAME_OF_DATASET, DATE_OF_ARCHIVING, REMARKS, NAME_OF_DATASET_ORIGINAL) " \
                    "VALUES (:data_id, :data_name, :req_date, :remarks, :org)"
            cur = self.con.cursor()
            cur_date = datetime.datetime.now()#datetime.date.today()
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

        :param data_id: Id of the related data set (Integer)
        :param state: The new value of the state column (String)
        :exception: DataException
        """

        self.__c_logger.info("Update process information to the content table")
        self.__f_logger.info("Update process information to the content table")
        cur = None
        try:
            query = "UPDATE SDE." + self.db_config["content_table"] +\
                    " c SET c.REMARKS = :state WHERE c.OBJECTID = :data_id"
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
            query = "UPDATE SDE." + self.db_config["content_table"] +\
                    " c SET c.NAME_OF_DATASET = :name WHERE c.OBJECTID = :data_id"
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
            query = "DELETE FROM SDE." + self.db_config["request_table"] + " WHERE OBJECTID = :data_id"
            cur = self.con.cursor()
            cur.prepare(query)
            cur.execute(None, {'data_id': data_id})
            self.con.commit()

        except cx_Oracle.DatabaseError as e:
            self.con.rollback()
            self.__c_logger.exception("EXCEPTION WHILE deleting request from the request table: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE deleting request from the request table: " + str(e))
            raise DataException("Exception while deleting the id " +
                                str(data_id) +
                                " column of SDE.ARCHIVE_ORDERS_EVW: \n" + str(e))
        finally:
            if cur is not None:
                cur.close()

    def add_meta_data(self, meta_data, arch_title):
        """
        Add required and optional meta data to the database

        :param meta_data: Meta data object containing validated meta data (MetaData)
        :param arch_title: The title of the data set after it was copied to the archvie
        :exception: DataException
        """
        self.__c_logger.info("Insert meta data into db")
        self.__f_logger.info("Insert meta data into db")
        cur = None

        try:
            query = "INSERT INTO " \
                "SDE." + self.arch_config['meta_data_table'] + " (archive_title, title, topic, description, " \
                "contact_name, contact_organisation, contact_position, contact_role, creation_date, content_lang, " \
                "bounding_box_west, bounding_box_east, bounding_box_north, bounding_box_south, " \
                "spatial_representation_type, spatial_reference_version, spatial_reference_space, " \
                "spatial_reference_code, maintenance_update_frequency, maintenance_note) " \
                "VALUES (:arch_title, :title, :topic, :description, :contact_name, :org, " \
                ":pos, :role, :create_date, :lang, :west, :east, :north, :south, " \
                ":sr_type, :sr_code, :sr_version, :sr_space, :m_freq, :m_note)"
            cur = self.a_con.cursor()
            cur.prepare(query)
            cur.execute(None, {
                'arch_title' : str(arch_title),
                'title': self.__check_meta_data_value(meta_data, 'title'),
                'topic': self.__check_meta_data_value(meta_data, 'topic'),
                'description': self.__check_meta_data_value(meta_data, 'description'),
                'contact_name': self.__check_meta_data_value(meta_data, 'contact_name'),
                'pos': self.__check_meta_data_value(meta_data, 'contact_position'),
                'org': self.__check_meta_data_value(meta_data, 'contact_organisation'),
                'role': self.__check_meta_data_value(meta_data, 'contact_role'),
                'lang': self.__check_meta_data_value(meta_data, 'content_lang'),
                'east': self.__check_meta_data_value(meta_data, 'bounding_box_east'),
                'west': self.__check_meta_data_value(meta_data, 'bounding_box_west'),
                'north': self.__check_meta_data_value(meta_data, 'bounding_box_north'),
                'south': self.__check_meta_data_value(meta_data, 'bounding_box_south'),
                'create_date': self.__check_meta_data_value(meta_data, 'creation_date'),
                'sr_type': self.__check_meta_data_value(meta_data, 'spatial_representation_type'),
                'sr_version': self.__check_meta_data_value(meta_data, 'spatial_reference_version'),
                'sr_space': self.__check_meta_data_value(meta_data, 'spatial_reference_space'),
                'sr_code': self.__check_meta_data_value(meta_data, 'spatial_reference_code'),
                'm_freq': self.__check_meta_data_value(meta_data, 'maintenance_frequency'),
                'm_note': self.__check_meta_data_value(meta_data, 'maintenance_note')
            })
            self.a_con.commit()
        except Exception as e:
            self.__c_logger.exception("EXCEPTION while inserting meta data into db: " + str(e))
            self.__f_logger.exception("EXCEPTION while inserting meta data into db: " + str(e))
            try:
                self.con.rollback()
            except Exception as e:
                raise DataException("Exception while inserting meta data into db: \n" + str(e))
            raise DataException("Exception while inserting meta data into db: \n" + str(e))
        finally:
            if cur is not None:
                cur.close()

    def __check_meta_data_value(self, meta_data, value):
        result_value = None
        if str(value) not in meta_data.meta_data():
            for key in meta_data.meta_data():
                if str(value) == (str(key).split("$"))[0]:
                    value = str(key)
        try:
            result_value = (meta_data.meta_data())[value]
            result_value = (str(result_value).split("$"))[0]
        except Exception as e:
            self.__c_logger.exception("EXCEPTION WHILE setting a meta data value: " + str(value) + ": " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE setting a meta data value: " + str(value) + ": " + str(e))

        return result_value
