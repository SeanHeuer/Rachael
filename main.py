import socket
from  bots import rachael
from modules import messageHandler
#The following is mostly for testing. We'll want to move it later down the road to a config file.

user = host = server = real = "rachael"
debug = False
network = "192.168.156.64"
port = 6667
chan = "#default"

def _restart(lib):
    print "Restarting!"
    reload(lib)

def _connect(username, hostname, servername, realname, network, port):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((network,port))
    irc.send('NICK ' + username + '\r\n')
    irc.send('USER ' + username + ' ' + hostname + ' ' + servername + ' ' + ':' + realname + ' IRC\r\n')
    return irc

if debug:
    print "Debugging!"

else:
    irc = _connect(user, host, server, real, network, port)
    bot1 = rachael.Rachael(debug, irc, chan)

    sender = None
    message = None

    while True:
        data = irc.recv (4096)
        dataline = data.splitlines()

        for line in dataline:
            print(line)
            datasplit = line.split(' ')

            if((datasplit[1] == "376") or (datasplit[1] == "422")):
                bot1._join(chan)

            elif "PING" == datasplit[0]: #If PING is Found in the Data
                irc.send('PONG ' + line.split()[1] + '\r\n') #Send back a PONG

            elif datasplit[1] == "PRIVMSG":
                message = messageHandler._getPrivmsg(line)
                print message

                if user + ": Restart" in message[2] and (message[0] == "sheuer" or message[0] == "masop"):

                    try:
                        messageHandler._send('Restarting!', chan, irc)
                        _restart(rachael)
                        _restart(messageHandler)
                        bot1 = rachael.Rachael(debug, irc, chan)
                        messageHandler._send('Restarted', chan, irc)

                    except Exception as errormsg:
                        irc.send(("ERROR: " + str(errormsg)), chan, irc)
                        print(traceback.format_exc())

                try:
                    bot1.parse(message[0], message[2])

                except Exception as errormsg:
                    irc.send(("ERROR: " + str(errormsg)), chan, irc)
                    print(traceback.format_exc())
