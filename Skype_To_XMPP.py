#!/usr/bin/env python
from datetime import datetime, timedelta

import sys
import signal
import logging
from time import sleep

from sleekxmpp import ClientXMPP, JID

import sqlite3

jid = "YOUR_USER_JID"
passwd = "PASSWORD"
domain = "DOMAIN"
server = "SERVER"

message_subject = "chatMessage"
plugin_config = {'feature_mechanisms': {'use_mech': 'PLAIN', 'unencrypted_plain': True, 'encrypted_plain': False}}


class HeraldBot(ClientXMPP):
    def __init__(self, jid, password, plugin_config):
        ClientXMPP.__init__(self, jid, password, plugin_config)
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')
        self.actions = ['subscribe', 'unsubscribe']
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler('presence_subscribe', self.presence_subscribe)
        self.add_event_handler('presence_subscribed', self.presence_subscribed)

    def presence_subscribe(self, presence):
        self.last_auth_request = datetime.now()
        self._handle_new_subscription(presence)

    def presence_subscribed(self, presence):
        self.last_auth_request = datetime.now()

    def message_send(self, msgBody):
        self.send_message(mto="any1\\40test.com@adstream", mbody=msgBody, msubject=message_subject)

    def session_start(self, event):
        self.send_presence()


def main(argv):
    # Get command line vars
    
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s <path to skype `main.db` file> <watch interval in seconds>\n" % sys.argv[0])
        sys.exit(1)

    port = 5222

    def int_handler(signum, frame):
        print('Disconnecting!')
	xmpp.disconnect()
        sys.exit(0)
    signal.signal(signal.SIGINT, int_handler)

    dbfilename = sys.argv[1]
    interval = float(sys.argv[2])

    conn = sqlite3.connect(dbfilename, 1)
    c = conn.cursor()
    try:
        c.execute("select id from Messages where id = (select max(id) from Messages);")
    except:
        print("Can't connect to DB")
        sys.exit(1)

    jid_escaped = JID(local = jid, domain = domain)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    xmpp = HeraldBot(jid_escaped, passwd, plugin_config=plugin_config)
    xmpp.auto_authorize = True
    xmpp.auto_subscribe = True
    xmpp.client_jid = jid_escaped
    xmpp.connect((server,port),use_ssl=False, use_tls = False)
    xmpp.process(block=False)
    xmpp.last_auth_request = datetime.now()

    (last_msg_id,) = c.fetchone()
    while True:
        sleep(interval)
        for id, body, name in c.execute("select id, body_xml, from_dispname from Messages where id > ?;", (last_msg_id,)):
            last_msg_id = max(id, last_msg_id)
            msg = name + "::" + body
            xmpp.message_send(msg)


if __name__ == '__main__':
    main(sys.argv[1:])

