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



# Request help: Student -> Server

{"msg": "request_help", "group_name": <group_name>, "question": <question>}

# Provide help: Teacher -> Server

{"msg": "provide_help", "ta_name": <ta_name>, "group_name": <group_name>}

# Provide queue update: Server -> Teacher / Student

{"msg": "queue_update", "queue": <queue>}



# Leave session: Teacher -> Server

{"msg": "leave_session", "ta_name": <ta_name>}

# Leave session: Student -> Server

{"msg": "leave_session", "group_name": <group_name>}


# Finish task: Student -> Server

{"msg": "task_finished", "question": <question>, "group_name": <group_name>}

# Provide progress update: Server -> Teacher

{"msg": "progress_update", "progress": <progress>}

