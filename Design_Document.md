Pychatroom3 Design Document
===========================

Introduction
-----

This project, I choose the python to be the language because it can make an connection very easily
use the socket library. And as a interpreted, dynamic programming language, python can run on any 
operating system without compile.
 
I build an ipv4-TCP connection between the server and client. As a chatroom, tcp always is better 
than the udp in security and reliability. 

In the server and client, I both use an endless while loop to be the thread. (At first, I want to
import the thread, use it to control the process but i failed because I am not good at it) In the
thread I also use the A-Sync I/O to confirm the thread can control mult-socket at same time.


Server Design
-----

Firstly, bind the host and port to build the connect. In the thread, server will keep listen the connect
required from the port. After connect, the server will append the user's sock, name, log in three 
different lists. Then for every message from any port, the message will be boardcast to all online client
via their socks. And in this process, the server still watch this message, if it find the message match 
to the command, server will goto the command method to do the right job.  

Client Design
-----

The client will try to connect to the specified address. The thread stdin and stdout will always watch
user's type-in and the boardcast from the server and put/get the data to/from the I/O stream.

Pros and Cons
----
 
 Pros
 > * TCP is stable and secure
 > * Server and client is light-weighting, cross-platform, easy to use.
 > * A-sync I/O ensure the mult-user chat is possible.
 
 Cons
 > * Can't build private chat now. (functional weakness)
 > * Can't use to world-wide chat, that need NAT.
 > * After server restart, every users' status will disappear. (functional weakness) *(I really should store the log in a file.)*
 > * GUI not support now. (I'm not good at PyQt)
   
   
   
   
   
 *&copy;Samuel Sui is the owner/builder of everything in this project.*