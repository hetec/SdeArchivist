# -*- encoding utf-8 -*-


class MetaDataRenderer:
    """
    MetaDateRenderer to produce formatted meta data representations
    """

    def __init__(self, meta_data):
        """
        Creates an MetaDateRenderer
        :param meta_data: Meta data to format
        :return: New MetaDataRenderer object
        """
        self.__meta_data = meta_data

    def render_txt_table(self):
        """
        Creates a simple text table of the key value pairs
        :return: Meta data as table (String)
        """
        meta_data_dict = self.__meta_data.meta_data();
        rendered_meta = ""
        for key in meta_data_dict:
            rendered_meta += "{:>30} | {}\n".format(key, meta_data_dict[key])
        return rendered_meta
