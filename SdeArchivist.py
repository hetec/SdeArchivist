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


def handle_process_failure(identifier, error, message, mailSender):
    meta_data_service.delete_by_id(identifier)
    meta_data_service.update_state(identifier, message)
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
    existenceValidator = ExistenceValidator.ExistenceValidator()

    check_project_structure(existenceValidator)

    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json")
    ms = MailSender.MailSender(props.mail_config)
    connection = OracleConnection(props.database_config).connection()
    ldap = LdapService.LdapService(props.ldap_config)
    sdeConf = props.sde_config
    sdeCon = SdeConnectionGenerator.SdeConnectionGenerator(sdeConf).connect()
    required_tags = props.tag_config
    meta_data_service = MetaDataService.MetaDataService(connection)

    print "\n1) GET ALL ENTRIES OF THE REQUEST TABLE\n"

    try:
        raw_meta = meta_data_service.find_meta_data_by_dataset_names()
    except DataException as e:
        inform_admin("Exception while fetching the meta data for the registered datasets: \n" +
                     e, ms)

    for xml in raw_meta:
        print "\n2) ADD TO CONTENTS TABLE: " + xml + "\n"
        pid = -1
        try:
            pid = meta_data_service.add_process(xml, "STARTED", xml)
        except DataException as e:
            inform_admin(e, ms)
            handle_process_failure(pid, e, "FAILED, INTERNAL ERROR", ms)
            continue

        print "\n3) VALIDATION OF: " + xml + "\n"
        validated_meta = MetaData.MetaData()
        MetaDataValidator.MetaDataValidator(raw_meta[xml], required_tags).validate(validated_meta)
        if validated_meta.is_valid():
            # meta_data_service.update_state(pid, "META DATA VALID")
            print "OK!"
            print "\n4) EXPORT OF: " + xml + "\n"

            try:
                xmlWorkspaceExporter.XmlWorkspaceExporter(sdeConf).export(xml)
            except xmlWorkspaceDocumentExportError as e:
                handle_process_failure(pid, e, "FAILED, EXPORT ERROR", ms)
                continue

            if existenceValidator.buffered_xml_exists(str(xml) + ".xml"):
                try:
                    print "\n5) IMPORT OF: " + xml + "\n"
                    XmlWorkspaceImporter.XmlWorkspaceImporter(props.sde_config).archive(str(xml) + ".xml")
                except XmlImportException as e:
                    handle_process_failure(pid, e, "FAILED, IMPORT ERROR", ms)
                meta_data_service.delete_by_id(pid)
                meta_data_service.update_state(pid, "FINISHED")
            else:
                handle_process_failure(pid, "The workspace xml " + str(xml) + " does not exist!",
                                       "FAILED, EXPORT ERROR", ms)
                continue

            if not existenceValidator.imported_sde_data_exists("SDE." + xml.split(".")[1]):
                handle_process_failure(pid, "The data: " + str(xml) + " does not exist in the sde after the import!",
                                       "FAILED, IMPORT ERROR", ms)
                continue
        else:
            meta_data_service.update_state(id, "INVALID META DATA")

            out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
            # ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out)
            print out
