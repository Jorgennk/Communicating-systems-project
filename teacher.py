"""
Script contains the teacher class and the corresponding mqtt-client for the teacher class.
Should be executed from teacher_client.ipynb
"""

from threading import Thread
import json
from stmpy import Machine, Driver
import paho.mqtt.client as mqtt
from utils import TOPIC, QUEUE_TOPIC, HELP_TOPIC, JOIN_TOPIC, PROGRESS_TOPIC, UPDATE_TOPIC
from stmpy import Driver, Machine
from threading import Thread
import paho.mqtt.client as mqtt
import ipywidgets as widgets
from IPython.display import display


class MQTT_Teacher_Client:
    def __init__(self, teacher):
        self.teacher: Teacher = teacher
        self.count = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.stm_driver: Driver = None


    def on_connect(self, client, userdata, flags, rc):
        """Called upon connecting"""
        print(f"on_connect(): {mqtt.connack_string(rc)}")


    def on_message(self, client, userdata, msg):
        """Called when receiving a message"""
        # Decode Json-message and ignore non-json formatted messages.
        try:
            message: dict = json.loads(msg.payload.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print(f"=====\nWARNING: Received message with incorrect formating:\n{msg.payload}\nIgnoring message...\n=====")
            return
        if "msg" not in message.keys():
            print(f"=====\nWARNING: Json object does not contain the key 'msg':\n{message}\nIgnoring message...\n=====")
            return
                    
        print(f"on_message(): topic: {msg.topic}, msg: {message['msg']}")

        if msg.topic == f"{TOPIC}/{JOIN_TOPIC}":
            self.join_handler(message)
        elif msg.topic == f"{TOPIC}/{self.teacher.session_id}/{HELP_TOPIC}":
            self.help_handler(message)
        elif msg.topic == f"{TOPIC}/{self.teacher.session_id}/{QUEUE_TOPIC}":
            self.queue_handler(message)
        elif msg.topic == f"{TOPIC}/{self.teacher.session_id}/{PROGRESS_TOPIC}":
            self.progress_handler(message)



    def validate_recipient(self, message: dict) -> bool:
        """Validate that this client is the intended recipient of this message."""
        if "ta_name" in message.keys():
            if message["ta_name"] != self.teacher.ta_name:
                print(f"{message['ta_name']} is not {self.teacher.ta_name}")
                return False
        elif "group_name" in message.keys():
            return False

        return True
        

    def subscribe_session_topics(self) -> None:
        """Subscribe to new topics after successfully joining a session"""
        self.client.unsubscribe(f"{TOPIC}/{JOIN_TOPIC}")

        self.client.subscribe(f"{TOPIC}/{self.teacher.session_id}/{QUEUE_TOPIC}")
        self.client.subscribe(f"{TOPIC}/{self.teacher.session_id}/{HELP_TOPIC}")
        self.client.subscribe(f"{TOPIC}/{self.teacher.session_id}/{PROGRESS_TOPIC}")


    def start(self, broker, port):
        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)
        self.client.subscribe(f"{TOPIC}/{JOIN_TOPIC}")

        try:
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()

    
    def join_handler(self, message: dict):
        """Handle messages in the join-topic"""
        # All messages in the join topic are intended for one recipient, so validate that
        # this particular message is for us:
        if not self.validate_recipient(message):
            return
        
        print(f"Received '{message['msg']}'")
        
        # NOTE: session_created and session_joined are handled the same way.
        if message["msg"] == "session_created" or message["msg"] == "session_joined":            
            self.teacher.session_id = message["session_id"]
            self.teacher.ta_code = message["ta_code"]
            self.teacher.student_code = message["student_code"]

            self.subscribe_session_topics()

            self.stm_driver.send("session_created", "teacher")

        # Handle session_join_failed.
        elif message["msg"] == "session_join_failed":
            self.teacher.error = message["error_message"]
            self.stm_driver.send("session_join_failed", "teacher")

    
    def queue_handler(self, message: dict):
        """Handle messages in the queue-topic"""
        if message["msg"] == "queue_update":
            self.teacher.queue = message["queue"]

            # If the queue-field is being displayed, update it immediately.
            if self.teacher.queue_field:
                self.teacher.queue_field.value = str(message["queue"])


    def progress_handler(self, message: dict):
        """Handle messages in the queue-topic"""
        print(message)
        if message["msg"] == "progress_update":
            self.teacher.progress = message["progress"]

            # If the progress-field is being displayed, update it immediately.
            if self.teacher.progress_field:
                self.teacher.progress_field.value = str(message["progress"])


    def help_handler(self, message: dict):
        """Handle messages in the help-topic"""
        pass
    

class Teacher:
    def __init__(self):
        # After creating/joining a session, these should be set.
        self.session_id: int = None
        self.ta_code: int = None
        self.student_code: int = None
        self.ta_name: str = None

        self.mqtt_client: mqtt.Client = None
        self.stm: Machine = None
        
        self.error = None
        self.queue: list[str] = []
        self.progress: dict = {}


    def __str__(self) -> str:
        return f"Session: {self.session_id}, TA-code: {self.ta_code}, Student-code: {self.student_code}"


    def create_session(self, b):
        """
        Create session. Send message to server and receive codes indicating the session
        has been created.
        """
        if self.ta_name_field.value == None:
            return
        
        self.ta_name = self.ta_name_field.value
        
        create_session = {"msg": "create_session", "ta_name": self.ta_name_field.value}
        self.mqtt_client.publish(f"{TOPIC}/{JOIN_TOPIC}", json.dumps(create_session, indent=4))
        
        self.stm.send("start_session")

    

    def join_session(self, b):
        """Join an already existing session using a TA code."""
        if not self.ta_code_field.value or not self.ta_name_field.value:
            return
        
        self.ta_name = self.ta_name_field.value
        
        join_session = {"msg": "join_session", "ta_code": self.ta_code_field.value, "ta_name": self.ta_name_field.value}
        self.mqtt_client.publish(f"{TOPIC}/{JOIN_TOPIC}", json.dumps(join_session, indent=4))

        self.stm.send("start_session")
        

    def in_idle(self):
        """Called upon entering idle-state."""
        print(f"In idle-state: {self}")
        self.button_create = widgets.Button(description="Create Session")
        self.button_create.on_click(self.create_session)
        self.button_join = widgets.Button(description="Join Session")
        self.button_join.on_click(self.join_session)
        self.ta_code_field = widgets.Text(value='', placeholder='', description='TA code:', disabled=False)
        self.ta_name_field = widgets.Text(value='', placeholder='', description='Name:', disabled=False)

        error_field = widgets.Text(value=self.error, placeholder='', description='Error code:', disabled=True)

        display(self.ta_name_field, self.button_create, self.ta_code_field, self.button_join, error_field)


    def in_wait(self):
        """Called upon entering wait-state."""
        print(f"In wait-state: {self}")
        return
    

    def in_lab_session_active(self):
        """Called upon entering lab_sesssion_active-state."""
        self.button_help = widgets.Button(description="Help")
        self.button_help.on_click(self.help)
        self.button_end = widgets.Button(description="End lab session")
        self.button_end.on_click(self.end_session)

        self.queue_field = widgets.Text(value=str(self.queue), placeholder="", description='Queue:', disabled=True)
        self.progress_field = widgets.Text(value=str(self.progress), placeholder="", description='Progress:', disabled=True)

        display(self.button_help, self.button_end, self.queue_field, self.progress_field)
        

        print(f"In lab_sesssion_active-state: {self}")


    def in_help(self):
        """Called upon entering help-state."""  
        self.button_help = widgets.Button(description="Finished Helping")
        self.button_help.on_click(self.finish_help)
        display(self.button_help)

        print(f"In help-state: {self}")


    def help(self, b):
        """Called when Help-button is pressed in lab_session_active"""
        # If queue is empty, there is noone to help.
        if not self.queue:
            return

        # Inform server that group is receiving help.
        provide_help = {"msg": "provide_help", "ta_name": self.ta_name, "group_name": self.queue[0]}
        self.mqtt_client.publish(f"{TOPIC}/{self.session_id}/{HELP_TOPIC}", json.dumps(provide_help))
        
        self.stm.send("help_group")


    def finish_help(self, b):
        """Called when Finished Help-button is pressed in help"""
        # Inform server that group has been helped successfully.
        # NOTE: Probably no reason to inform the server about this, I suppose.
        # self.mqtt_client.publish(f"{TOPIC}/{self.session_id}/{HELP_TOPIC}", "finished helping")
        self.stm.send("finish_help")


    def end_session(self, b):
        """Called when End Session-button is pressed in lab_session_active"""
        leave_session = {"msg": "leave_session", "ta_name": self.ta_name}
        self.mqtt_client.publish(f"{TOPIC}/{self.session_id}/{UPDATE_TOPIC}", json.dumps(leave_session))

        self.stm.send("end_lab")
