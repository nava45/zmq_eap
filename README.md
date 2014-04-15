zmq_eap
=======

A Sample Enterprise App using zero mq python

Plan:

python controller.py start (To start the computing in distributed way)
python controller.py stop (stop all executing items)

controller:
   It is the intermidiate step between producer and user command
   It pushed the command to master

master:
   It get the command from controller, also it always listen to the master
   It launches several workers and sending the task to all the worker parallely.

   
