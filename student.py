from threading import Thread
import json
from stmpy import Machine, Driver
import paho.mqtt.client as mqtt
from utils import TOPIC, JOIN_TOPIC, QUEUE_TOPIC, HELP_TOPIC, UPDATE_TOPIC 
import ipywidgets as widgets
from IPython.display import display


class MQTT_Student_Client:
    def __init__(self, stm):
        self.state_machine = stm
        self.count = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.stm_driver: Driver = None
        self.session_id = ""

    def on_connect(self, client, userdata, flags, rc):
        """Called upon connecting"""
        print(f"on_connect(): {mqtt.connack_string(rc)}")

    def on_message(self, client, userdata, msg):
        """Called when receiving a message"""
        # Decode Json-message and ignore non-json formatted messages.
        try:
            message: dict  = json.loads(msg.payload.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print(f"=====\nWARNING: Received message with incorrect formating:\n{msg.payload}\nIgnoring message...\n=====")
            return
        if "msg" not in message.keys():
            print(f"=====\nWARNING: Json object does not contain the key 'msg':\n{message}\nIgnoring message...\n=====")
            return
                
        if msg.topic == (f"{TOPIC}/{JOIN_TOPIC}"):
            if message['msg'] == "session_joined":
                print("Correct code, session joined")
                self.stm_driver.send("correct_code", "student")

                #Unsubscribe from the JOIN TOPIC so other messages aren't received
                self.client.unsubscribe(f"{TOPIC}/{JOIN_TOPIC}")
                print("Sucsessfully unsubscribed to: "+ (f"{TOPIC}/{JOIN_TOPIC}"))
                self.session_id = message['session_id']
                
                # Send the session_id to the student object
                self.state_machine.session_id = message["session_id"]
                
                #Subscribe to the session and the following topics:
                #team02/session_id/HELP_TOPIC
                #team02/session_id/UPDATE_TOPIC
                self.client.subscribe(f"{TOPIC}/{message['session_id']}/{HELP_TOPIC}")
                print("Sucsessfully subscribed to: "+ (f"{TOPIC}/{message['session_id']}/{HELP_TOPIC}"))
                
                self.client.subscribe(f"{TOPIC}/{message['session_id']}/{UPDATE_TOPIC}")
                print("Sucsessfully subscribed to: "+ (f"{TOPIC}/{message['session_id']}/{UPDATE_TOPIC}"))
                self.client.subscribe(f"{TOPIC}/{self.session_id}/{QUEUE_TOPIC}")
                
            if message['msg'] == "session_join_failed":
                print("Incorrect code, try again")
                self.stm_driver.send("wrong_code", "student")
                
                
        if msg.topic == f"{TOPIC}/{self.session_id}/{QUEUE_TOPIC}":
            print("Receiving queue, passing on to state machine")
            self.state_machine.queue_message = message['queue']
            self.stm_driver.send("queue_request", "student")
            print("queue sent sucsessfully to state machine")
                    

    def start(self, broker, port):
        print("Connectin to {}:{}".format(broker, port))
        self.client.connect(broker, port)
        self.client.subscribe(f"{TOPIC}/{JOIN_TOPIC}")

        try:
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()



class Student:
    def __init__(self):
        self.button_create = widgets.Button(description="Join Session")
        self.button_create.on_click(self.on_button_join)
        self.queue_message = []
        self.session_id = ""
        self.mqtt_client: mqtt.Client = None
        self.stm: Machine = None
        self.question = 1
        # Hard coded number of questions.
        self.total_questions = 5
        
        # text field
        self.stu_code = widgets.Text(value='', placeholder='', description='student code:', disabled=False)
        self.code = self.stu_code.value
        display(self.button_create, self.stu_code)
        
        self.group_name_widget = widgets.Text(value='', placeholder='', description='Group name:', disabled=False)
        self.group_name = self.group_name_widget.value

        display(self.button_create, self.group_name_widget)

      
    def ask_help(self):
        dictMessage = { "msg": "request_help", "group_name": self.group_name_widget.value, "question": self.question}
        jsonMessage = json.dumps(dictMessage)
        print("Asking for help")
        self.mqtt_client.publish(f"{TOPIC}/{self.session_id}/{HELP_TOPIC}", jsonMessage)
        self.number_queue.value = "Queuing"


    def finish_task(self):
        print(f"Finished with task {self.question}")
        dictMessage = {"msg": "task_finished", "question": self.question, "group_name": self.group_name_widget.value}
        jsonMessage = json.dumps(dictMessage)
        self.mqtt_client.publish(f"{TOPIC}/{self.session_id}/{UPDATE_TOPIC}", jsonMessage)

        if self.question == self.total_questions:
            self.button_finish_task.disable = True
        else: 
            self.question += 1
            self.progress_bar.value += 1 
            self.button_task.value = self.question
            
            
    def update_queue(self):
        self.place = 1
        if self.group_name_widget.value not in self.queue_message:
            self.number_queue.value = "Not in queue"
        #ENABLE HELP
        else:
            for i in self.queue_message:
                if i == self.group_name_widget.value:
                    break
                else:
                    self.place += 1  

            Sondre_idiot_confirmed = str(self.place)             
            self.number_queue.value = Sondre_idiot_confirmed
            

    def restart(self):
        self.mqtt_client.subscribe(f"{TOPIC}/{JOIN_TOPIC}")
        self.button_create = widgets.Button(description="Join Session")
        self.button_create.on_click(self.on_button_join)
        self.queue_message = []
        self.session_id = ""
        self.question = 1
        # Hard coded number of questions.
        self.total_questions = 5

        # text field
        self.stu_code = widgets.Text(value='', placeholder='', description='student code:', disabled=False)
        self.code = self.stu_code.value
        display(self.button_create, self.stu_code)

        self.group_name_widget = widgets.Text(value='', placeholder='', description='Group name:', disabled=False)

        self.group_name = self.group_name_widget.value

        display(self.button_create, self.group_name_widget)


    def publish(self):
        dictMessage = {"msg": "join_session","student_code": self.stu_code.value, "group_name": self.group_name_widget.value}
        jsonMessage = json.dumps(dictMessage)

        self.mqtt_client.publish(f"{TOPIC}/{JOIN_TOPIC}" ,jsonMessage)
        self.stu_code.value = "Loading"


    def setup_lab(self):
        print("Setting up lab...")
        self.button_task = widgets.IntText(value= self.question, placeholder='', description='Task', disabled=True)
        display(self.button_task)
        self.button_help = widgets.Button(description="Get help")
        self.button_help.on_click(self.on_button_ask_help)
        display(self.button_help)
        self.button_finish_task = widgets.Button(description="Finish task")
        self.button_finish_task.on_click(self.on_button_finish_task)
        display(self.button_finish_task)
        self.progress_bar = widgets.IntProgress(min = 1, max = self.total_questions, description = "Progress")
        display(self.progress_bar)
        self.button_leave = widgets.Button(description="Leave Session")
        self.button_leave.on_click(self.on_button_leave)
        display(self.button_leave)
        self.number_queue = widgets.Text(value="Not in queue", placeholder='', description='Queue nr.', disabled=True)
        display(self.number_queue)
        print("Lab set up")


    def save_text(self):
        self.code = self.stu_code.value
           

    def on_button_join(self, session_code_stu):
        self.stm.send('join')
  

    def on_button_finish_task(self, session_code_stu):
        self.stm.send('finish_task')
      

    def on_button_ask_help(self, session_code_stu):
        self.stm.send('ask_help')


    def on_button_leave(self, session_code_stu):
        self.stm.send('leave_lab')
        leave_message = {"msg": "leave_session", "group_name": self.group_name_widget.value}
        json_message = json.dumps(leave_message)
        self.mqtt_client.publish(f"{TOPIC}/{self.session_id}/{UPDATE_TOPIC}", json_message)
    