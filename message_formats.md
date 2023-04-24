# Create session: Teacher -> Server

{"msg": "create_session", "ta_name": <ta_name>}

# Join session: Teacher -> Server

{"msg": "join_session", "ta_code": <ta_code>, "ta_name": <ta_name>}

# Join session: Students -> Server

{"msg": "join_session", "ta_code": <ta_code>, "group_name": <group_name>}

# Session created: Teacher -> Server

{"msg": "session_created", "session_id": <session_id>, "ta_code": <ta_code>, "student_code": <student_code>, "ta_name": <ta_name>}

# Session joined: Server -> Teacher

{"msg": "session_joined", "session_id": <session_id>, "ta_code": <ta_code>, "student_code": <student_code>, "ta_name": <ta_name>}

# Session joined: Server -> Student

{"msg": "session_joined", "session_id": <session_id>, "group_name": <group_name>}

# Session join failed: Server -> Teacher

{"msg": "session_join_failed", "error_message": <error_message>, "ta_name": <ta_name>}

# Session join failed: Server -> Student

{"msg": "session_join_failed", "error_message": <error_message>, "group_name": <group_name>}