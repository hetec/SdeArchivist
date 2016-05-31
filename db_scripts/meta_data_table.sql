DROP TABLE sde_meta_data CASCADE CONSTRAINTS PURGE;

-- Create the table for the meta data entries

CREATE TABLE sde_meta_data (
  id NUMBER(19),
  -- required values
  title VARCHAR2(1000 char) NOT NULL,
  topic VARCHAR2(1000 char) NOT NULL,
  description CLOB NOT NULL,
  contact_name VARCHAR2(1000 char) NOT NULL,
  contact_organisation VARCHAR2(1000 char) NOT NULL,
  contact_position VARCHAR2(1000 char) NOT NULL,
  contact_role VARCHAR2(1000 char) NOT NULL,
  creation_date VARCHAR2(1000 char) NOT NULL, -- date is not represented as milliseconds since epoch
  content_lang VARCHAR2(1000 char) NOT NULL,
  bounding_box_west VARCHAR2(1000 char) NOT NULL,
  bounding_box_east VARCHAR2(1000 char) NOT NULL,
  bounding_box_north VARCHAR2(1000 char) NOT NULL,
  bounding_box_south VARCHAR2(1000 char) NOT NULL,
  -- optional values
  special_representation_type VARCHAR2(1000 char),
  special_reference_version VARCHAR2(1000 char),
  special_reference_space VARCHAR2(1000 char),
  special_reference_code VARCHAR2(1000 char),
  maintenance_update_fequency VARCHAR2(1000 char),
  maintenance_note CLOB,
  CONSTRAINT check_pk_range 
    CHECK(id BETWEEN -9223372036854775808 AND 9223372036854775807),
  CONSTRAINT pk_sde_meta_data 
    PRIMARY KEY(id)
);

-- Automatically increment the primary key of the table
-- Create a sequence from 1 to max value

DROP SEQUENCE seq_sde_meta_data;
CREATE SEQUENCE seq_sde_meta_data;

-- Create trigger which updates the id of sde_meta_data to the next value of
-- the created sequence

CREATE OR REPLACE TRIGGER tri_sde_meta_data
BEFORE INSERT ON sde_meta_data
FOR EACH ROW
BEGIN :NEW.id := seq_sde_meta_data.NEXTVAL;
END;
/

INSERT INTO sde_meta_data (
title,
topic,
description,
contact_name,
contact_organisation,
contact_position,
contact_role,
creation_date,
content_lang,
bounding_box_west,
bounding_box_east,
bounding_box_north,
bounding_box_south) VALUES (
'test_title',
'test_desc',
'test_topic1, test_topic2',
'test_name',
'test_orga',
'test_posit',
'test_role',
'22223344',
'de',
'150.1',
'160.3',
'60.112',
'88.56');