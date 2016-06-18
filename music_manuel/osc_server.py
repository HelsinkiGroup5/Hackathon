import OSC, time
#import rtmidi_python as rtmidi
#midi_out = rtmidi.MidiOut()
#midi_out.open_port(0)


def handler(addr, tags, data, client_address):
    txt = "OSCMessage '%s' from %s: " % (addr, client_address)
    txt += str(data)
    print(txt)
    #num = data[0]
    #print num
    #midi_out.send_message([0x90, 192, num]) # Note on
    #time.sleep(0.5)
    #midi_out.send_message([0x80, 192, num]) # Note on
    #print("midi sent")


if __name__ == "__main__":
    s = OSC.OSCServer(('10.100.7.151', 57120))  # listen on localhost, port 57120
    s.addMsgHandler('/startup', handler)     # call handler() for OSC messages received with the /startup address
    s.serve_forever()
