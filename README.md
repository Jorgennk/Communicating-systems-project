# Communicating-systems-project

This is the project for [TTM4115](https://www.ntnu.edu/studies/courses/TTM4115).

## Motivation

We want a grade and it is the semester project given for the course innit?

## Contents

It is a system built using the MQTT protocol to make it easier for teachers and teaching assistants to help and organize computer labs here at NTNU.

It creates a queueing system for people asking for help and stores information about how long people spend in the queue in simple .txt files which can be used to analyze the labs later.

The same is done when the students mark a task as finihsed. Thta way, the course coordinator can analyze the contents and adapt the labs or lecture so that the students get a more optimized learning experience.

There was plans to create a proper forntend that could serve the contents more visually pleasing, but we dropped it since it was not a part of the core of this subject/project.

## How to run

Firstly you need to be on NTNU's local wifi or use a vpn to access the MQTT broker.

Start up by running the [server.ipynb](/server.ipynb), this keeps control of the states, queues and progress.

Then you can run [teacher_client.ipynb](teacher_client.ipynb) and [student_client.ipynb](student_client.ipynb). Note: server must be running for any of those to have a meaningful function. Else it spams messages to nothing.

From here it should be pretty self explanatory to run stuff. Just be sure to create a session as a teacher and join it as a student first! 😌🤙
