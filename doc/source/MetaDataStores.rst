Meta Data Stores
================

Oracle db table
---------------

If a database is available and the program runs, it will try to story the defined meta data into
a ORACLE database table of the SDE schema of the sdearchive instance.

The sql script to restore or create this table and the associated trigger and sequence is stored in

SdeArchivist/db_scripts/meta_data_table.sql

Just run the script to remove the old table and all its data and create everything newly.

Elastic search
--------------

The program tries to index the meta data in the configured elasticsearch instance. If ES is not available,
a fallback mechanism takes place and writes all meta data records into a cache file under

SdeArchivist/config/failed_indexing.cache

The program will try to reindex all entries of the cache on startup.