zmq_eap
=======

A Sample Enterprise App using zeromq in python

<b>executing plan:</b>

<i>python controller.py start</i> (To start the computing in distributed way)

<i>python controller.py stop</i> (stop all executing items)


<b>controller:</b>

   It is the application launcher
   
   It pushes the user command to master

<b>master:</b>

   It gets the command from controller, also it always listen to the controller
   
   It launches several workers in distributed way and distributing the tasks to all the worker.

   
