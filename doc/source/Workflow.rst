User Workflow
=============

--- manual process ---

1. The user connects to the original sde instance through ArcMap (requires appropriate credentials)
2. The user searches for the 'request' and 'content' table and includes these into ArcMap through drag and drop
3. The user enables the editon of the tables through clicking 'start editing' in the context menu of one of the tables
4. The user opens the 'request' table through the context menu
5. The user enters the name a its data set (USERNAME.dataname). The name is case sensitive.

--- automatic process ---

6. The program fetches the data from the request table
7. The program validates the meta data
8. The program copies the the data to the archive
9. The program exports the meta data to the relevant meta data stores
10. The User will be informed

NOTE: If something unexpected happens the user will be informed through email if possible. Simultaneously the
state of the process will be documented in the 'content' table. In critical situation the admin will be informed.