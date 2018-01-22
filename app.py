#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import qi
import argparse
import sys
import time
import signal

def signal_handler(signal, frame):
        print('Bye!')
        sys.exit(0)

def main(session):
    # Get the service ALTabletService.

    try:
        tabletService = session.service("ALTabletService")

        tabletService.loadApplication("project_launcher")
        tabletService.showWebview()

        # Don't forget to disconnect the signal at the end
        signalID = 0

        def callback(event):
            execfile("/home/nao/projects/" + event + "/app.py")
            tabletService.onJSEvent.disconnect(signalID)


        # attach the callback function to onJSEvent signal
        signalID = tabletService.onJSEvent.connect(callback)

        print("Waiting for Ctrl+C to disconnect")
        signal.pause()

    except Exception, e:
        print "Error was: ", e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)

