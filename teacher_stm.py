"""Teacher states and transitions for state machine."""

# initial transition
t0 = {'source': 'initial',
      'target': 'idle'}

# transitions
t1 = {'trigger':'create_session', 
      'source':'idle', 
      'target':'wait'}
t2 = {'trigger':'join_session', 
      'source':'idle', 
      'target':'wait'}
t3 = {'trigger':'session_created', 
      'source':'wait', 
      'target':'lab_session_active'}
t4 = {'trigger':'session_join_failed', 
      'source':'wait', 
      'target':'idle'}

t5 = {'trigger':'help_group', 
      'source':'lab_session_active', 
      'target':'help'}
t6 = {'trigger':'finish_help', 
      'source':'help', 
      'target':'lab_session_active'}

t7 = {'trigger':'end_lab', 
      'source':'lab_session_active', 
      'target':'exit'}
 
# the states:
idle = {'name': 'idle',
        'entry': 'in_idle'}

wait = {'name': 'wait',
        'entry': 'in_wait'}

lab_session_active = {'name': 'lab_session_active',
        'entry': 'in_lab_session_active'}

help = {'name': 'help',
        'entry': 'in_help'}


TEACHER_TRANSITIONS = [t0, t1, t2, t3, t4, t5, t6, t7]
TEACHER_STATES = [idle, wait, lab_session_active, help]