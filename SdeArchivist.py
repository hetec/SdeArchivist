# -*- encoding utf-8 -*-
"""
    Project to enable automatic archiving of geographic data which
    are persisted in an ArcSDE geo-database

    This module defines the main program logic.
"""
import ArchivistLogger
import BufferCleaner
import ExistenceValidator
import LdapService
import MailSender
import MetaData
import MetaDataRenderer
import MetaDataService
import MetaDataValidator
import SdeArchivistProperties
import SdeConnectionGenerator
import XmlWorkspaceImporter
import xmlWorkspaceExporter
import DatasetRenameService
from OracleConnection import OracleConnection
from DataIndexer import DataIndexer

# Do not change this in the rest of the code!
SDE_SOURCE_DB = "sde"
SDE_ARCHIVE_DB = "sdearchive"
BUFFER_DIR = "buffer"
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "archivist_config.json"
XML_EXTENSION = ".xml"

ASCII = '''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ___________ _____    ___           _     _       _     _
/  ___|  _  |  ___|  / _ \         | |   (_)     (_)   | |
\ `--.| | | | |__   / /_\ \_ __ ___| |__  ___   ___ ___| |_
 `--. | | | |  __|  |  _  | '__/ __| '_ \| \ \ / | / __| __|
/\__/ | |/ /| |___  | | | | | | (__| | | | |\ V /| \__ | |_
\____/|___/ \____/  \_| |_|_|  \___|_| |_|_| \_/ |_|___/\__|

~~~~~~~~~~~~~~~~~~~~~ Patrick Hebner ~~~~~~~~~~~~~~~~~~~~~~~

'''

STEP1 = '''

*********************************************
* Initialize objects and load configuration *
*********************************************

'''

STEP2 = '''

****************************************
* Fetch Entries form the request table *
****************************************

'''

STEP3 = '''

***********************************
* Start archiving for all entries *
***********************************

'''

STEP4 = '''

********************************
* Start the validation process *
********************************

'''

STEP5 = '''

*********************************************
* Export the meta data as XML to the buffer *
*********************************************

'''

STEP6 = '''

*************************************************************
* Import the meta data XML from the buffer into the archive *
*************************************************************

'''

STEP7 = '''

**************************************
* Add the meta data to elasticsearch *
**************************************

'''

STEP8 = '''

****************************************************
* Data were successfully imported into the archive *
****************************************************

'''

SUCCESS_MAIL_STATE = "success"
FAILURE_MAIL_STATE = "failure"

def handle_process_failure(cont_id,
                           req_id,
                           error,
                           message,
                           mailSender):
    """
    Handles unexpected situations by updating the request and content tables
    and sending status mails

    :param cont_id: Id of the related row in the content table (Integer)
    :param req_id: Id of the related row in the request table (Integer)
    :param error: The error object (Exception)
    :param message: Custom error message (String)
    :param mailSender: MailSender object (MailSender)
    """
    try:
        meta_data_service.delete_by_id(req_id)
        meta_data_service.update_state(cont_id, message)
        meta_data_service.update_name(cont_id, "Not Set")
        console_logger.error("ERROR during the execution -> " + str(message) + "\n" + str(error))
        file_logger.error("ERROR during the execution -> " + str(message) + "\n" + str(error))
    except Exception as e:
        inform_admin("Handling the exception (element id = " +
                     cont_id +
                     "): \n" +
                     str(error) +
                     " raises also a exception: \n" + str(e) +
                     " \n"
                     "Maybe there is a problem with the database connection or the queried tables.",
                     mailSender)

    mailSender.send("patrick.hebner@ufz.de", str(error), FAILURE_MAIL_STATE)


def inform_admin(message, mailSender):
    """
    Send an email to the configured admin/s

    :param message: content of the email (String)
    :param mailSender: MailSender instance (MailSender)
    """
    mailSender.send_to_admin(str(message))


def check_project_structure(validator):
    """
    Checks if the necessary directories (config, buffer) and the
    config file exist in the right location

    :param validator: validator instance (ExistenceValidator)
    """
    buffer_exists = existenceValidator.directory_exists(BUFFER_DIR)
    config_exists = existenceValidator.directory_exists(CONFIG_DIR)
    config_file_exists = existenceValidator.config_file_exists(CONFIG_FILE_NAME)

    if not buffer_exists or not config_exists or not config_file_exists:
        raise Exception("Invalid project structure!")


if __name__ == "__main__":

    # Get config from config/archivist_config.json
    props = SdeArchivistProperties.SdeArchivistProperties(CONFIG_DIR + "/" + CONFIG_FILE_NAME)

    # Create loggers
    console_logger = ArchivistLogger.ArchivistLogger(props.log_config).get_console_logger()
    file_logger = ArchivistLogger.ArchivistLogger(props.log_config).get_file_logger()

    console_logger.debug(ASCII)
    file_logger.debug(ASCII)

    console_logger.debug(STEP1)
    file_logger.debug(STEP1)

    # Create existence validator
    existenceValidator = ExistenceValidator.ExistenceValidator()
    existenceValidator.set_console_logger(console_logger)
    existenceValidator.set_file_logger(file_logger)

    check_project_structure(existenceValidator)

    # Create mail sender object
    ms = MailSender.MailSender(props.mail_config)
    ms.set_console_logger(console_logger)
    ms.set_file_logger(file_logger)

    # Create directory cleaner
    cleaner = BufferCleaner.BufferCleaner()
    cleaner.set_console_logger(console_logger)
    cleaner.set_file_logger(file_logger)

    # Get oracle database connection
    ora_con = OracleConnection(props.database_config)
    ora_con.set_console_logger(console_logger)
    ora_con.set_file_logger(file_logger)
    connection = ora_con.connection()

    # Establish ldap connection
    ldap = LdapService.LdapService(props.ldap_config)
    ldap.set_file_logger(file_logger)
    ldap.set_console_logger(console_logger)

    # Get the particular config for the sde and sde archive databases
    sdeConf = props.sde_config
    archive_conf = props.sdearchive_config

    # Create connection creator objects for sde and sde archive
    connection_generator_sde = SdeConnectionGenerator.SdeConnectionGenerator(sdeConf, SDE_SOURCE_DB)
    connection_generator_sde.set_console_logger(console_logger)
    connection_generator_sde.set_file_logger(file_logger)
    connection_generator_sdearchive = SdeConnectionGenerator.SdeConnectionGenerator(archive_conf, SDE_ARCHIVE_DB)
    connection_generator_sdearchive.set_file_logger(file_logger)
    connection_generator_sdearchive.set_console_logger(console_logger)

    # Create or reuse sde connections files
    sdeCon = connection_generator_sde.connect()
    archive_con = connection_generator_sdearchive.connect()

    # Get the required tags for the meta data from the conifig file
    required_tags = props.tag_config

    # Create meta data service
    meta_data_service = MetaDataService.MetaDataService(connection)
    meta_data_service.set_console_logger(console_logger)
    meta_data_service.set_file_logger(file_logger)

    # Get the elasticsearch config
    elastic_config = props.elasticsearch_config

    # Initialize the data indexer
    indexer = DataIndexer(elastic_config)
    indexer.set_console_logger(console_logger)
    indexer.set_file_logger(file_logger)

    console_logger.info(STEP2)
    file_logger.info(STEP2)

    # Get the meta data for all entries of the request table if they exist in the database
    # Search is based on the data name
    raw_meta = {}

    try:
        raw_meta = meta_data_service.find_meta_data_by_dataset_names()
    except Exception as e:
        raw_meta = {}
        inform_admin("Exception while fetching the meta data for the registered datasets: \n" +
                     e, ms)

    # If there are at one or more entries in the database table continue for each meta data entry
    if len(raw_meta) > 0:
        console_logger.info(STEP3)
        file_logger.info(STEP3)
        for xml in raw_meta:
            console_logger.debug("Fetch the ID of the current entry")
            file_logger.debug("Fetch the ID of the current entry")
            # Get the id of the row in the request table
            request_table_id = -1
            try:
                request_table_id = meta_data_service.find_id_by_name(str(xml))
            except Exception as e:
                inform_admin(e, ms)
                handle_process_failure(-1, request_table_id, e, "FAILED, INTERNAL ERROR", ms)
                continue

            # Add the current process to the content table and get the assigned id
            content_table_id = -1
            try:
                console_logger.debug("Update state of the entry in the content table")
                file_logger.debug("Update state of the entry in the content table")
                content_table_id = meta_data_service.add_process(xml, "STARTED", xml)
            except Exception as e:
                inform_admin(e, ms)
                handle_process_failure(content_table_id, request_table_id, e, "FAILED, INTERNAL ERROR", ms)
                continue

            # Verify the current meta data against the required tags specified in the config file
            console_logger.info(STEP4)
            file_logger.info(STEP4)
            # Meta data object to hold information about the current meta data
            validated_meta = MetaData.MetaData()
            # Create the meta data validator
            meta_validator = MetaDataValidator.MetaDataValidator(raw_meta[xml], required_tags)
            meta_validator.set_console_logger(console_logger)
            meta_validator.set_file_logger(file_logger)
            # Do the validation and write the results into the meta data container
            meta_validator.validate(validated_meta)
            # Ask the meta data object if there are some issues. If not continue.
            if validated_meta.is_valid():
                console_logger.info(STEP5)
                file_logger.info(STEP5)
                # Try to export the data to a xml workspace document into the buffer directory
                try:
                    # Create the exporter
                    exporter = xmlWorkspaceExporter.XmlWorkspaceExporter(sdeConf, SDE_SOURCE_DB)
                    exporter.set_console_logger(console_logger)
                    exporter.set_file_logger(file_logger)
                    # Do the export
                    exporter.export(xml)
                except Exception as e:
                    handle_process_failure(content_table_id, request_table_id, e, "FAILED, EXPORT ERROR", ms)
                    continue

                # If the data was successfully exported to the buffer try to import the exproted
                # data to the read only database schema
                console_logger.debug("Check the existence of the exported XML")
                file_logger.debug("Check the existence of the exported XML")
                if existenceValidator.buffered_xml_exists(str(xml) + ".xml"):
                    try:
                        console_logger.info(STEP6)
                        file_logger.info(STEP6)
                        # Create the importer
                        importer = XmlWorkspaceImporter.XmlWorkspaceImporter(archive_conf, SDE_ARCHIVE_DB)
                        importer.set_console_logger(console_logger)
                        importer.set_file_logger(file_logger)
                        # Do the import
                        importer.archive(str(xml) + XML_EXTENSION)
                        # After successfully importing the data remove the entry in the request table and update
                        # the state of entry in the content table
                        try:
                            meta_data_service.delete_by_id(request_table_id)
                            meta_data_service.update_state(content_table_id, "FINISHED")
                        except Exception as e:
                            handle_process_failure(content_table_id, request_table_id, e,
                                                   "CORRUPT (NOT ABLE TO SET STATE)",
                                                   ms)
                    except Exception as e:
                        handle_process_failure(content_table_id, request_table_id, e, "FAILED, IMPORT ERROR", ms)
                else:
                    handle_process_failure(content_table_id, request_table_id,
                                           "The workspace xml " + str(xml) + " does not exist!",
                                           "FAILED, EXPORT ERROR", ms)
                    continue

                # Check the existence of the data in the archive database.
                # If the data doesn't exist update the state.
                console_logger.debug("Check the existence of the imported data")
                file_logger.debug("Check the existence of the imported data")
                if not existenceValidator.imported_sde_data_exists(SDE_ARCHIVE_DB,
                                                                   SDE_SOURCE_DB + "." + xml.split(".")[1]):
                    handle_process_failure(content_table_id, request_table_id, "The data: " + str(xml) +
                                           " does not exist in the sde archive after the import!",
                                           "FAILED, IMPORT ERROR", ms)
                    continue
                else:
                    # Rename the persisted dataset in the archive schema
                    try:
                        renameService = DatasetRenameService.DatasetRenameService(archive_conf, existenceValidator)
                        renameService.setConsoleLogger(console_logger)
                        renameService.setFileLogger(file_logger)
                        xml = renameService.rename(xml)

                        # Index the meta data to elasticserach
                        console_logger.info(STEP7)
                        file_logger.info(STEP7)
                        try:
                            indexer.index(str(xml), validated_meta)
                        except Exception as e:
                            inform_admin(e, ms)

                        # Update the name column in the content table to the name after the renaming process
                        try:
                            meta_data_service.update_name(content_table_id, xml)
                            ms.send("patrick.hebner@ufz.de", "SUCCESS", SUCCESS_MAIL_STATE)
                            console_logger.info(STEP8)
                            file_logger.info(STEP8)
                        except Exception as e:
                            handle_process_failure(content_table_id, request_table_id, e,
                                                   "CORRUPT (NOT ABLE TO SET NAME)",
                                                   ms)
                    except Exception as e:
                        inform_admin("The renaming of the persisted dataset: " + xml +
                                     " failed because of an exception. There are maybe" +
                                     " corrupt data with wrong naming in the sde archive schema. Exception: " + str(e),
                                     ms)
                        handle_process_failure(content_table_id, request_table_id, e,
                                               "FAILED, RENAMING ERROR",
                                               ms)
            else:
                # Update state of the content table for invalid metadata
                try:
                    meta_data_service.delete_by_id(request_table_id)
                    meta_data_service.update_state(content_table_id, "INVALID META DATA")
                    meta_data_service.update_name(content_table_id, "Not Set")
                except Exception as e:
                    handle_process_failure(content_table_id, request_table_id, e,
                                           "CORRUPT (NOT ABLE TO SET STATE)",
                                           ms)

                # Send a mail to inform about the invalid metadata
                out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
                # ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out, FAILURE_MAIL_STATE)
                ms.send("patrick.hebner@ufz.de", "FAILED! The meta data of '" + str(xml) + "' are invalid: \n\n" + out, FAILURE_MAIL_STATE)
                #print out

            # Remove the buffered file
            cleaner.clear_file(str(xml) + XML_EXTENSION)

    else:
        console_logger.debug("No meta data found for the entries of the request table")
        file_logger.debug("No meta data found for the entries of the request table")

    # Remove all remaining files from the buffer
    cleaner.clear_all(BUFFER_DIR)
