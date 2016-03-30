The archivist_config.json file
==============================

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


