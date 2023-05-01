"""Student states and transitions for state machine."""

# initial transition
t0 = {'source': 'initial',
      'target': 'idle'}

# transitions
t1 = {'trigger':'join', 
      'source':'idle', 
      'target':'wait'}

t2 = {'trigger':'wrong_code', 
      'source':'wait', 
      'target':'idle'}

t3 = {'trigger':'correct_code', 
      'source':'wait', 
      'target':'lab_session_active',
      'effect': 'setup_lab'}

t4 = {'trigger':'ask_help', 
      'source':'lab_session_active', 
      'target':'lab_session_active',
      'effect': 'ask_help' }

t5 = {'trigger':'leave_queue', 
      'source':'lab_session_active', 
      'target':'lab_session_active',
      'effect': 'leave_queue'}

t6 = {'trigger':'finish_task', 
      'source':'lab_session_active', 
      'target':'lab_session_active',
      'effect': 'finish_task'}

#Trengs ikke siden det skjer automatisk når man ber om hjelp
t7 = {'trigger':'queue_request', 
       'source':'lab_session_active', 
       'target':'lab_session_active',
       'effect': 'update_queue'}

t8 = {'trigger':'leave_lab', 
      'source':'lab_session_active', 
      'target':'exit',
      'effect': '__init__'}


# the states:
idle = {'name': 'idle'}

wait = {'name': 'wait',
        'entry': 'publish'}

lab_session_active = {'name': 'lab_session_active'}


STUDENT_TRANSITIONS = [t0, t1, t2, t3, t4, t5, t6, t7, t8]
STUDENT_STATES = [idle, wait, lab_session_active]