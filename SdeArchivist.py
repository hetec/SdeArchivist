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

def handle_failure(identifier, error, message, mailSender):
    meta_data_service.delete_by_id(identifier)
    meta_data_service.update_state(identifier, message)
    mailSender.send("patrick.hebner@ufz.de", str(error))
    print str(error)

if __name__ == "__main__":
    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json")
    ms = MailSender.MailSender(props.mail_config)
    existenceValidator = ExistenceValidator.ExistenceValidator()
    connection = OracleConnection(props.database_config).connection()
    ldap = LdapService.LdapService(props.ldap_config)
    sdeConf = props.sde_config
    sdeCon = SdeConnectionGenerator.SdeConnectionGenerator(sdeConf).connect()
    required_tags = props.tag_config
    meta_data_service = MetaDataService.MetaDataService(connection)

    meta_data_service.find_meta_data_by_dataset_names()
    print "\n1) GET ALL ENTRIES OF THE REQUEST TABLE\n"
    requests = meta_data_service.find_all_requests()
    raw_meta = meta_data_service.find_meta_data_by_dataset_names()
    for d in raw_meta:
        print d

    for xml in raw_meta:
        print "\n2) ADD TO CONTENTS TABLE: " + xml + "\n"
        pid = meta_data_service.add_process(xml, "STARTED", xml)
        print("TYPE of pid: " + str(type(pid)))
        print "\n3) VALIDATION OF: " + xml + "\n"
        validated_meta = MetaData.MetaData()
        MetaDataValidator.MetaDataValidator(raw_meta[xml], required_tags).validate(validated_meta)
        if validated_meta.is_valid():
            #meta_data_service.update_state(pid, "META DATA VALID")
            print "OK!"
            print "\n4) EXPORT OF: " + xml + "\n"

            try:
                xmlWorkspaceExporter.XmlWorkspaceExporter(sdeConf).export(xml)
            except xmlWorkspaceDocumentExportError as e:
                handle_failure(pid, e, "FAILED, EXPORT ERROR", ms)
                continue

            if existenceValidator.buffered_xml_exists(str(xml) + ".xml"):
                try:
                    print "\n5) IMPORT OF: " + xml + "\n"
                    XmlWorkspaceImporter.XmlWorkspaceImporter(props.sde_config).archive(str(xml) + ".xml")
                except XmlImportException as e:
                    handle_failure(pid, e, "FAILED, IMPORT ERROR", ms)
                meta_data_service.delete_by_id(pid)
                meta_data_service.update_state(pid, "FINISHED")
            else:
                handle_failure(pid, "The workspace xml " + str(xml) + " does not exist!", "FAILED, EXPORT ERROR", ms)
                continue

            if not existenceValidator.imported_sde_data_exists("SDE." + xml.split(".")[1]):
                handle_failure(pid, "The data: " + str(xml) + " does not exist in the sde after the import!",
                               "FAILED, IMPORT ERROR", ms)
                continue
        else:
            meta_data_service.update_state(id, "INVALID META DATA")

            out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
            #ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out)
            print out


