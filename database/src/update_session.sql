DELIMITER $$

USE <%DATABASE%>

DROP PROCEDURE IF EXISTS update_session $$

CREATE PROCEDURE update_session(IN sessionID VARCHAR(64), IN sigID VARCHAR(64), IN msgSig VARCHAR(64),
                                IN user_id VARCHAR(64))
BEGIN
    UPDATE sessions
    SET sig_id = sigID 
    WHERE session_id = sessionID;
    
    UPDATE sessions
    SET msg_sig = msgSig 
    WHERE session_id = sessionID;
    
    UPDATE sessions
    SET usr_id = user_id 
    WHERE session_id = sessionID;
    
    UPDATE sessions
    SET last_update = NOW() 
    WHERE session_id = sessionID;
    
    SELECT *
    FROM sessions
    WHERE session_id = sessionID;
END
$$

DELIMITER ;
