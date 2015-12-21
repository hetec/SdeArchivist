# -*- encoding utf-8 -*-
from OracleConnection import OracleConnection
import MetaDataService
import MetaDataValidator
import MetaData
import SdeArchivistProperties
import LdapService
import MetaDataRenderer
import MailSender
import SdeConnectionGenerator
import xmlWorkspaceExporter
import XmlWorkspaceImporter
import xmlWorkspaceDocumentExportError
import XmlImportException
import ExistenceValidator
import DataException
import ArchivistLogger
import BufferCleaner

def handle_process_failure(cont_id, req_id, error, message, mailSender):
    try:
        meta_data_service.delete_by_id(req_id)
        meta_data_service.update_state(cont_id, message)
    except Exception as e:
        inform_admin("Handling the exception (element id = " +
                     cont_id +
                     "): \n" +
                     str(error) +
                     " raises also a exception: \n" + str(e) +
                     " \n"
                     "Maybe there is a problem with the database connection or the queried tables.")

    mailSender.send("patrick.hebner@ufz.de", str(error))

    print str(error)


def inform_admin(message, mailSender):
    mailSender.send_to_admin(str(message))


def check_project_structure(validator):
    buffer_exists = existenceValidator.directory_exists("buffer")
    config_exists = existenceValidator.directory_exists("config")
    config_file_exists = existenceValidator.config_file_exists("archivist_config.json")

    if not buffer_exists or not config_exists or not config_file_exists:
        raise Exception("Invalid project structure!")


if __name__ == "__main__":
    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json")

    console_logger = ArchivistLogger.ArchivistLogger(props.log_config).get_console_logger()
    file_logger = ArchivistLogger.ArchivistLogger(props.log_config).get_file_logger()

    existenceValidator = ExistenceValidator.ExistenceValidator()
    existenceValidator.set_console_logger(console_logger)
    existenceValidator.set_file_logger(file_logger)

    check_project_structure(existenceValidator)



    ms = MailSender.MailSender(props.mail_config)
    ms.set_console_logger(console_logger)
    ms.set_file_logger(file_logger)

    cleaner = BufferCleaner.BufferCleaner()
    cleaner.set_console_logger(console_logger)
    cleaner.set_file_logger(file_logger)

    ora_con = OracleConnection(props.database_config)
    ora_con.set_console_logger(console_logger)
    ora_con.set_file_logger(file_logger)
    connection = ora_con.connection()

    ldap = LdapService.LdapService(props.ldap_config)
    ldap.set_file_logger(file_logger)
    ldap.set_console_logger(console_logger)

    sdeConf = props.sde_config
    archive_conf = props.sdearchive_config

    #Todo: combine these generators
    connection_generator_sde = SdeConnectionGenerator.SdeConnectionGenerator(sdeConf, "sde")
    connection_generator_sde.set_console_logger(console_logger)
    connection_generator_sde.set_file_logger(file_logger)
    connection_generator_sdearchive = SdeConnectionGenerator.SdeConnectionGenerator(sdeConf, "sde")
    connection_generator_sdearchive.set_file_logger(file_logger)
    connection_generator_sdearchive.set_console_logger(console_logger)

    sdeCon = connection_generator_sde.connect()
    archive_con = connection_generator_sdearchive.connect()

    required_tags = props.tag_config
    meta_data_service = MetaDataService.MetaDataService(connection)
    meta_data_service.set_console_logger(console_logger)
    meta_data_service.set_file_logger(file_logger)

    print "\n1) GET ALL ENTRIES OF THE REQUEST TABLE\n"

    raw_meta = {}

    try:
        raw_meta = meta_data_service.find_meta_data_by_dataset_names()
    except Exception as e:
        raw_meta = {}
        inform_admin("Exception while fetching the meta data for the registered datasets: \n" +
                     e, ms)

    if len(raw_meta) > 0:
        for xml in raw_meta:
            print "\n2) ADD TO CONTENTS TABLE: " + xml + "\n"

            request_table_id = -1
            try:
                request_table_id = meta_data_service.find_id_by_name(str(xml))
            except Exception as e:
                inform_admin(e, ms)
                handle_process_failure(-1, request_table_id, e, "FAILED, INTERNAL ERROR", ms)
                continue

            content_table_id = -1
            try:
                content_table_id = meta_data_service.add_process(xml, "STARTED", xml)
            except Exception as e:
                inform_admin(e, ms)
                handle_process_failure(content_table_id, request_table_id, e, "FAILED, INTERNAL ERROR", ms)
                continue

            print "\n3) VALIDATION OF: " + xml + "\n"
            validated_meta = MetaData.MetaData()
            meta_validator = MetaDataValidator.MetaDataValidator(raw_meta[xml], required_tags)
            meta_validator.set_console_logger(console_logger)
            meta_validator.set_file_logger(file_logger)
            meta_validator.validate(validated_meta)
            if validated_meta.is_valid():
                print "OK!"
                print "\n4) EXPORT OF: " + xml + "\n"

                try:
                    exporter = xmlWorkspaceExporter.XmlWorkspaceExporter(sdeConf, "sde")
                    exporter.set_console_logger(console_logger)
                    exporter.set_file_logger(file_logger)
                    exporter.export(xml)
                except Exception as e:
                    handle_process_failure(content_table_id, request_table_id, e, "FAILED, EXPORT ERROR", ms)
                    continue

                if existenceValidator.buffered_xml_exists(str(xml) + ".xml"):
                    try:
                        print "\n5) IMPORT OF: " + xml + "\n"
                        importer = XmlWorkspaceImporter.XmlWorkspaceImporter(archive_conf, "sdearchive")
                        importer.set_console_logger(console_logger)
                        importer.set_file_logger(file_logger)
                        importer.archive(str(xml) + ".xml")
                    except XmlImportException as e:
                        handle_process_failure(content_table_id, request_table_id, e, "FAILED, IMPORT ERROR", ms)
                    try:
                        meta_data_service.delete_by_id(request_table_id)
                        meta_data_service.update_state(content_table_id, "FINISHED")
                    except Exception as e:
                        handle_process_failure(content_table_id, request_table_id, e, "CORRUPT (NOT ABLE TO SET STATE)")
                else:
                    handle_process_failure(content_table_id, request_table_id, "The workspace xml " + str(xml) + " does not exist!",
                                           "FAILED, EXPORT ERROR", ms)
                    continue

                if not existenceValidator.imported_sde_data_exists("sdearchive", "SDE." + xml.split(".")[1]):
                    handle_process_failure(content_table_id, request_table_id, "The data: " + str(xml) +
                                           " does not exist in the sdearchive after the import!",
                                           "FAILED, IMPORT ERROR", ms)
                    continue
                else:
                    ms.send_to_admin("Success")
            else:
                try:
                    meta_data_service.delete_by_id(request_table_id)
                    meta_data_service.update_state(content_table_id, "INVALID META DATA")
                except Exception as e:
                    handle_process_failure(content_table_id, request_table_id, e, "CORRUPT (NOT ABLE TO SET STATE)")
                out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
                # ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out)
                ms.send_to_admin(out)
                print out

            cleaner.clear_file(str(xml) + ".xml")
    else:
        # Logging
        print "No meta data available"

    cleaner.clear_all("buffer")