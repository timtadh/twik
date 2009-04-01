
-- Tim Henderson
-- Table Creation for <%DATABASE%>

START TRANSACTION;

-- DROP DATABASE IF EXISTS diplomacy;
-- CREATE DATABASE diplomacy DEFAULT CHARACTER SET ascii COLLATE ascii_general_ci;
USE <%DATABASE%>
----------------------------------------  Schema  -------------------------------------
--  users (usr_id : varchar(64), name : varchar(256), email : varchar(256), 
--         screen_name : varchar(128), pass_hash : varchar(64), salt : varchar(64),
--         last_login : datetime, creation : datetime, status : varchar(500))
--
--  session (session_id : varchar(64), sig_id : varchar(64), msg_sig : varchar(64),
--           usr_id : varchar(64), last_update : datetime)
----------------------------------------  Schema  -------------------------------------

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    usr_id varchar(64) NOT NULL,
    name varchar(256) NOT NULL,
    email varchar(256) NOT NULL,
    screen_name varchar(128) NOT NULL,
    pass_hash varchar(64) NOT NULL,
    salt varchar(64) NOT NULL,
    last_login datetime NOT NULL,
    creation datetime NOT NULL,
    status varchar(500),
    CONSTRAINT pk_users PRIMARY KEY (usr_id),
    CONSTRAINT uq_email UNIQUE (email),
    CONSTRAINT uq_screen_name UNIQUE (screen_name)
);

DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions
(
    session_id varchar(64) NOT NULL,
    sig_id varchar(64) NOT NULL,
    msg_sig varchar(64) NOT NULL,
    usr_id varchar(64) NOT NULL,
    last_update datetime NOT NULL,
    CONSTRAINT pk_session PRIMARY KEY (session_id),
    CONSTRAINT fk_usr_id FOREIGN KEY (usr_id)
        REFERENCES users(usr_id) ON DELETE RESTRICT 
);

COMMIT;