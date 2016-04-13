General Information
===================

The archivist_config.json file
------------------------------

.. code-block:: javascript

    {
      "database_config" : {
        "url" : "The database url",
        "port" :  "Port of the database",
        "service" :  "Name of the service running on the database",
        "username" : "John Doe",
        "password" : "*********",
        "request_table" : "Table name for the requests",
        "content_table" : "Table name for the content"
      },
      "sde_config" : {
        "project_root" : "Local path to the SdeArchivist directory",
        "database_type" : "ORACLE",
        "instance_name" : "The quick connection string",
        "auth_method" : "DATABASE_AUTH",
        "username" : "Sde super user name",
        "password" : "***********"
      },
      "sdearchivist_config" : {
        "project_root" : "",
        "database_type" : "",
        "instance_name" : "",
        "auth_method" : "",
        "username" : "Sdearchive super user name (almost always the same as Sde user)",
        "password" : "*********"
      },
      "elasticsearch_config": {
        "host": "The elasitcsearch server url",
        "index": "index name",
        "type": "type name"
      },
      "ldap_config" : {
        "server" : "ldap server url",
        "dn" : "ou=people,dc=company,dc=de"
      },
      "mail_config" : {
        "smtp_server" : "server url",
        "port" : "Port of the mail server",
        "from" : "Mail address to send the emails",
        "username" : "Username for the mail account",
        "password" : "***********",
        "get_user_process_info" : false,
        "admin_recipients" : [Comma separated list of admins],
        "failure_subject" : "Subject in the case of failure",
        "success_subject" : "Subject in the case of success",
        "default_message" : "Default message. Displayed before the main content"
      },
      "log_config" : {
        "level" : "Log level",
        "file" : "path to the logfile including logfile name",
        "log_file_size" : 4000 in bytes,
        "log_file_count" : 3 number of files which are retained
      },
      "tag_config" : {
        "required" : [
          {
            "tag_name" : "keyword "
            "mapped_name" : "New name for keyword"
          },
          {
            "tag_name" : "CharSetCd",
            "is_empty" : true,
            "attributes" : ["value"]
          },
          {
             "tag_name" : "dataIdInfo/dataLang/languageCode",
             "is_empty" : true,
             "attributes" : ["value"]
          }

        ]
      }
    }




Define required tags
--------------------

**Tag resolution**

It is possible to specify tags in the config file by name and by xml path.

1. By name: only 'tagname'
2. By XML path: <parentTag><oneChildTag><DesiredTag>?§$%-*"!?</...></...></...>

1.
    If you use the tagname version you should be aware of behavior since this method checks
    all existing tags regardless of their positions in the XML tree. So if there are multiple tags
    with the same name they all need to pass the test to get positive validation result.

2.
    If you use a path to specify you would only target all tags which match to the given path. The path is relative
    to the root element of the meta data XML (In the case of SDE meta data this is the <metadata> tag). Thus this tag
    may not be part of your path

**Rules**

Default tags::

    <tag>Here comes some content</tag>

    "tag_config" : {
        "required" : [
          {
            "tag_name" : "tag",
            "mapped_name" : "desiredName in emails",
          }
        ]
      }

This means for the validation:

- Tag with the defined name must exist in the XML
- Tag is automatically not_empty --> content between tags necessary <tag>content</tag>
-
    Attributes can be defined additionally. If a configuration for attributes exist the tag
    must contain them and the attributes must be populated with values

Empty tags::

    <tag attributeName="attributeValue"/>

    "tag_config" : {
        "required" : [
          {
            "tag_name" : "parentTag/childTag/tag",
            "is_empty" : true,
            "attributes" : ["attriubteName", ... ]
            "mapped_name" : "desiredName in emails",
          }
        ]
      }

This means for the validation:

- Tag name must exists

-
    Is_empty specifies that an empty tag <tag /> is allowed. It is mandatory to mark empty tags with
    is_empty since without this marker the tag would be treated as not empty tag and must have content.
    Thus the validation would fail.

-
    If attributes are defined <tag attr="value" /> they must exist else
    the tag is also valid without attributes <tag/>

-
    It is recommended to use qualified paths to identify tags
    else undesired behavior is possible because of equally named tags in the XML (See tag resolution)