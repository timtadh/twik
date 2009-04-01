DELIMITER $$

USE <%DATABASE%>

DROP PROCEDURE IF EXISTS session_data $$

CREATE PROCEDURE session_data(IN session_id VARCHAR(64))
BEGIN
    SELECT *
    FROM sessions AS ses
    WHERE ses.session_id = session_id;
END
$$

DELIMITER ;
