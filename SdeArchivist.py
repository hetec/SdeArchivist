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

if __name__ == "__main__":

    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json")
    connection = OracleConnection(props.database_config).connection()
    ldap = LdapService.LdapService(props.ldap_config)
    meta_data_service = MetaDataService.MetaDataService(connection)
    raw_meta = meta_data_service.find_flagged_meta_data()

    sdeConf = props.sde_config
    print sdeConf
    sdeCon = SdeConnectionGenerator.SdeConnectionGenerator(sdeConf).connect()
    required_tags = props.tag_config
    print required_tags
    print required_tags

    for xml in raw_meta:
        validated_meta = MetaData.MetaData()
        MetaDataValidator.MetaDataValidator(raw_meta[xml], required_tags).validate(validated_meta)
        if validated_meta.is_valid():
            print "OK!"
            print xml
            xmlWorkspaceExporter.XmlWorkspaceExporter(sdeConf).export(xml)
        else:
            ms = MailSender.MailSender(props.mail_config)
            out = MetaDataRenderer.MetaDataRenderer(validated_meta).render_txt_table()
            #ms.send(ldap.get_email_by_uid(xml.split(".")[0]), out)
            print out


