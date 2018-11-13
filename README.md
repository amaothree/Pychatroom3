Pychatroom3
============

A chatroom demo written by python3

Introduction
------------

This is an chatroom demo written by python3, there are two different file to use on the server and client.
It still is demo because it come from my *Distributed System* assignment project homework. It seem be I will never improve it ever.

这是用python3写的一个聊天室demo，有两个不同的文件分别针对客户端和服务端。之所以只是个简单的demo是因为这是我的分布式系统的作业，做了要求的就没继续完善了，估计以后也不会再更新了。

System Required
-----------------

Install python3

Linux (work)  
Windows (not test, I don't know)  
Mac/OSX (not test)

How to use
----------

Open Server
>python server.py  
**(The default host and port is localhost:14588, you can change it in the code directly)**

* After you boot server, you can forget it.

Open Client
>python client.py [host] [port]  
**(The default is also localhost:14588)**

* Everytime client connect to the server, a nickname is needed. The nickname just can use chinese or alphabet letters.
* Client can use command after connect to server 
  > \<You\> */command [parameter]*

Basic User Command
------------------

* /exit  
  >**(important!!!!) Please use this command to disconnet safety**
* /list
  >List the online user.
* /status [username]
  >Show a list(log) of all commands and message used by the user.
* /kick [username]
  >**Admin account ONLY**, closes the connection between the server and the user.

Admin Account
-------------

I set a admin account default, you can use it to kick someone (the only special function now), you need to type "Admin" as the nickname. The default password is "123", it is unsafe, you can change it in the code of server, and restart server.