#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import sys
sys.path.append("/home/nao/studiotoolkit/python")

import qi
import argparse
import time
import signal
import subprocess
import stk.runner
import os

class CPEAppLauncher(object):

    subprocess = None

    def terminate_previous_app(self):
        if self.subprocess is not None and self.subprocess.returncode is None:
            print "Terminating app"
            self.subprocess.terminate()
            self.subprocess.wait()


    def __init__(self, qiapplication):
        self.qiapplication = qiapplication

    def home(self):
        self.launchWebApp(os.path.basename(os.path.dirname(os.path.realpath(__file__))))

    def launch(self, app):
        self.terminate_previous_app()
        print "Creating subprocess for", app
        self.subprocess = subprocess.Popen("/home/nao/projects/" + app + "/app.py")

    def launchWebApp(self, webapp):
        self.terminate_previous_app()
        print "Showing webview of", webapp
        try:
            tabletService = session.service("ALTabletService")
            tabletService.loadApplication(webapp)
            tabletService.showWebview()
        except Exception, e:
            print "Error was: ", e

    def stop(self):
        self.qiapplication.stop()

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
    stk.runner.run_service(CPEAppLauncher)
