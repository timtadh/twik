DELIMITER $$

USE <%DATABASE%>

DROP PROCEDURE IF EXISTS delete_session $$

CREATE PROCEDURE delete_session(IN sessionID VARCHAR(64))
BEGIN
    DELETE ses
    FROM sessions as ses
    WHERE (ses.session_id = sessionID);
END
$$

DELIMITER ;
