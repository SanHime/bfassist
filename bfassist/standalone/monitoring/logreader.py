#############################################################################
#
#
# Module of BFA that reads the event log of the server
#
#
#############################################################################
""" This module implements thread-utilization for reading the event log and processing it.

    Dependencies:

        bfassist <- standalone <- monitoring <- logreader
            |
            \-> standalone  @LogReader.run
             -> bfa_logging

        note::  Author(s): Mitch last-check: 08.07.2021 """

from threading import Thread
from subprocess import Popen

from bfassist.standalone.monitoring import RealTimeRound, RealTimeEvent
from bfassist.standalone import Server
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


round_starts = '<bf:round'
log_ends = '</bf:log>'

server_starts = '<bf:server'
server_ends = '</bf:server'

event_starts = '<bf:event'
event_ends = '</bf:event'

roundstats_start = '<bf:roundstats'
roundstats_end = '</bf:roundstats'


class LogReader(Thread):
    """ Thread for reading the event log fed to us. We do some preliminary parsing here so bfxml only has to parse the
    important bits. Builds paragraph chunks and sends them for parsing to bfxml.

        :param server:          Server Object the Log-Reader attaches to.
        :param eventLogFeed:    The event log feed to read from for better readability.
        :param paragraph:       The entire content of the paragraph/xml-tag currently being prepared for parsing.
        :param currentLine:     The line that's currently being examined.

            note::  Author(s): Mitch """

    tagList = {}
    hooks = {}

    def __init__(self, server: Server, eventLogFeed: Popen = None, paragraph: str = "", currentLine: str = ""):
        Thread.__init__(self)
        self.server = server
        self.eventLogFeed = eventLogFeed

        self.paragraph = paragraph
        self.currentLine = currentLine

    def parse(self, inXML: str):
        """ Main parsing function of this class that delegates parsing using the tag list.

            :param inXML:       The xml to be processed.

                note::  Author(s): Mitch """

        try:
            log("Parsing inXML for server.", 0)
            for tag in self.tagList:
                if tag in inXML:
                    self.tagList[tag](inXML)
        except AttributeError:
            self.server.StatsInterface.realTimeRound = RealTimeRound(self.server)
            self.parse(inXML)

    def continueUntil(self, paragraphEnds: str):
        """ Simple function to continue the parsing-pre-process until the currently prepared paragraph ends.

            :param paragraphEnds:   The ending tag at which we'll stop.

                note::  Author(s): Mitch """

        self.paragraph = self.currentLine
        while (paragraphEnds not in self.currentLine) and self.server.monitoringIsActive():
            if log_ends in self.currentLine:
                self.server.MonitoringInterface.renewEventFeed()
            else:
                self.paragraph += self.currentLine
                self.currentLine = self.getNextLine()
        self.paragraph += self.currentLine
        self.parse(self.paragraph)

    def getNextLine(self):
        """ Simple function to get the next line from the feed.

            :return:    The next line from the feed.

                note::  Author(s): Mitch """

        try:
            return self.eventLogFeed.stdout.readline()
        except ValueError as error:
            log("Trying to read from event log caused a value error. " + str(error), 3)
            self.server.MonitoringInterface.renewEventFeed()

    def run(self):
        from bfassist.standalone import KERN

        log("Starting the log reader for a server.")
        self.currentLine = self.eventLogFeed.stdout.readline()
        while self.server.monitoringIsActive():
            if log_ends in self.currentLine:
                self.server.MonitoringInterface.renewEventFeed()
            elif round_starts in self.currentLine:
                self.paragraph = self.currentLine
                self.parse(self.paragraph)
            elif server_starts in self.currentLine:
                self.continueUntil(server_ends)
            elif event_starts in self.currentLine:
                self.continueUntil(event_ends)
            elif roundstats_start in self.currentLine:
                self.continueUntil(roundstats_end)
            self.currentLine = self.getNextLine()
        log("Stopping the log reader for a server.")
