Skype_To_Xmpp
=============

Python bot which listening Skype's DB and if got new message then send it to XMPP user

Thanks to 
----------
Vladislav Yarmak
https://github.com/Snawoot
and thanks to his skype-watch script
https://github.com/Snawoot/skype-watch

Script usage
------------

Add to the Skype_To_Xmpp.py your parameters
jid = "YOUR_USER_JID"
passwd = "PASSWORD"
domain = "DOMAIN"
server = "SERVER"

Then launch as

python Skype_To_Xmpp.py <path to skype `main.db` file> <watch interval in seconds>

Dependencies
------------
sleekxmpp (pip install sleekxmpp)

Notice
------
On Linux (tried under CentOS) all works fine
On MacOS can't connect to Skype DB because can't create more then one connection to DB (If anyone will find decision please let me know, I will be grateful)
On Windows - works well
