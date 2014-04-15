zmq_eap
=======

A Sample Enterprise App using zero mq python

<b>executing plan:</b>

<i>python controller.py start</i> (To start the computing in distributed way)

<i>python controller.py stop</i> (stop all executing items)


<b>controller:</b>

   It is the intermidiate step between producer and user command
   
   It pushed the command to master

<b>master:</b>

   It get the command from controller, also it always listen to the master
   
   It launches several workers and sending the task to all the worker parallely.

   
