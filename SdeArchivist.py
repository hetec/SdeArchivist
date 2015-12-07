# -*- encoding utf-8 -*-

from OracleConnection import OracleConnection
import MetaDataService
import MetaDataValidator
import MetaData
import SdeArchivistProperties


if __name__ == "__main__":

    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json")
    connection = OracleConnection(props.database_config).connection()
    meta_data_service = MetaDataService.MetaDataService(connection)
    metadata = meta_data_service.find_flagged_meta_data()

    tags = props.tag_config
    print tags

    meta = MetaData.MetaData()
    for xml in metadata:
        out = "{0:>40} :: {1}".format(xml, metadata[xml])
        print out
        MetaDataValidator.MetaDataValidator(metadata[xml], tags).validate(meta)

    for m in meta.meta_data():
        print m + "::" + meta.meta_data()[m]

    print meta.is_valid()
