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

if __name__ == "__main__":

    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json")
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
            xmlWorkspaceExporter.XmlWorkspaceExporter(sdeConf).export(xml)
            print "\n5) IMPORT OF: " + xml + "\n"
            XmlWorkspaceImporter.XmlWorkspaceImporter(props.sde_config).archive(str(xml) + ".xml")
            meta_data_service.delete_by_id(pid)
            meta_data_service.update_state(pid, "FINISHED")
        else:
            meta_data_service.update_state(id, "INVALID META DATA")
            ms = MailSender.MailSender(props.mail_config)
            out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
            #ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out)
            print out


