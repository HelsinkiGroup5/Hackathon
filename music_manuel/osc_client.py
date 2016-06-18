import OSC, random, time

c = OSC.OSCClient()
c.connect((' 10.100.7.151', 57120))   # localhost, port 57120
oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/startup")
while True:
    numr = random.randrange(0, 50)
    #numr = numr*0.01
    oscmsg.append(numr)
    print numr
    c.send(oscmsg)
    oscmsg.clearData()
    time.sleep(5)
