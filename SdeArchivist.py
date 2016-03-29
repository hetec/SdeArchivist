# -*- encoding utf-8 -*-
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

# Do not change this in the rest of the code!

SDE_SOURCE_DB = "sde"
SDE_ARCHIVE_DB = "sdearchive"
BUFFER_DIR = "buffer"
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "archivist_config.json"
XML_EXTENSION = ".xml"

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
    :param cont_id: Id of the related row in the content table
    :param req_id: Id of the related row in the request table
    :param error: The error object
    :param message: Custom error message
    :param mailSender: MailSender object
    """
    try:
        meta_data_service.delete_by_id(req_id)
        meta_data_service.update_state(cont_id, message)
        console_logger.error(str(error))
        file_logger.error(str(error))
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

    print str(error)


def inform_admin(message, mailSender):
    """
    Send an email to the configured admin/s
    :param message:
    :param mailSender:
    """
    mailSender.send_to_admin(str(message))


def check_project_structure(validator):
    """
    Checks if the necessary directories (config, buffer) and the
    config file exist in the right location

    :param validator:
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
    # Todo: combine these generators
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

    print "\n1) GET ALL ENTRIES OF THE REQUEST TABLE\n"

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
        for xml in raw_meta:
            print "\n2) ADD TO CONTENTS TABLE: " + xml + "\n"

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
                content_table_id = meta_data_service.add_process(xml, "STARTED", xml)
            except Exception as e:
                inform_admin(e, ms)
                handle_process_failure(content_table_id, request_table_id, e, "FAILED, INTERNAL ERROR", ms)
                continue

            # Verify the current meta data against the required tags specified in the config file
            print "\n3) VALIDATION OF: " + xml + "\n"
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
                print "OK!"
                print "\n4) EXPORT OF: " + xml + "\n"
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
                if existenceValidator.buffered_xml_exists(str(xml) + ".xml"):
                    try:
                        print "\n5) IMPORT OF: " + xml + "\n"
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
                if not existenceValidator.imported_sde_data_exists(SDE_ARCHIVE_DB,
                                                                   SDE_SOURCE_DB + "." + xml.split(".")[1]):
                    handle_process_failure(content_table_id, request_table_id, "The data: " + str(xml) +
                                           " does not exist in the sde archive after the import!",
                                           "FAILED, IMPORT ERROR", ms)
                    continue
                else:
                    try:
                        renameService = DatasetRenameService.DatasetRenameService(archive_conf, existenceValidator)
                        renameService.setConsoleLogger(console_logger)
                        renameService.setFileLogger(file_logger)
                        xml = renameService.rename(xml)
                        ms.send("patrick.hebner@ufz.de", "SUCCESS", SUCCESS_MAIL_STATE)
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
                except Exception as e:
                    handle_process_failure(content_table_id, request_table_id, e,
                                           "CORRUPT (NOT ABLE TO SET STATE)",
                                           ms)

                # Send a mail to inform about the invalid metadata
                out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
                # ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out, FAILURE_MAIL_STATE)
                ms.send("patrick.hebner@ufz.de", "FAILED! Your meta data are invalid: \n\n" + out, FAILURE_MAIL_STATE)
                print out

            # Remove the buffered file
            cleaner.clear_file(str(xml) + XML_EXTENSION)
    else:
        # Handle name mismatches
        print "No meta data available"

    # Remove all remaining files from the buffer
    cleaner.clear_all(BUFFER_DIR)
