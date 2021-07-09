#############################################################################
#
#
# Module of BFA that reads and manages bf-xml 1.1
#
#
#############################################################################
""" This module does process parsing for bf events in the event log.

    Dependencies:

        monitoring <- bfxmlevent
            \
             -> logreader

        note::  Author(s): Mitch, henk last-check: 08.07.2021 """

from bfassist.standalone.monitoring.logreader import *
from bfassist.standalone.monitoring import BfRounds


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class LogReaderEventProcessing(LogReader):
    """ Extension of the log reader that parses bf events.

        :param to_greet:    A set of players that were not on the server last round and therefore should be greeted.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, to_greet: set = None):

        super().__init__(server)
        if to_greet:
            self.to_greet = to_greet
        else:
            self.to_greet = set()

    def onBeginMedPack(self, inEvent: RealTimeEvent):
        """ Function that's called when a begin med pack event occurred.

            :param inEvent:     The begin med pack event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        medpack_status = inEvent.parameters['medpack_status']
        healed_player = inEvent.parameters['healed_player']

        self.realTimeRound.beginMedPack(player_id, player_location, medpack_status, healed_player)
    super().hooks['beginMedPack'] = onBeginMedPack

    def onBeginRepair(self, inEvent: RealTimeEvent):
        """ Function that's called when a begin repair event occurred.

            :param inEvent:     The begin repair event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        repair_status = inEvent.parameters['repair_status']
        vehicle_type = inEvent.parameters['vehicle_type']

        self.realTimeRound.beginRepair(player_id, player_location, repair_status, vehicle_type)
    super().hooks['beginRepair'] = onBeginRepair

    def onChangePlayerName(self, inEvent: RealTimeEvent):
        """ Function that's called when a change player name event occurred.

            :param inEvent:     The change player name event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        name = inEvent.parameters['name']

        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            player = self.server.PlayerInterface.onlinePlayerWithId[player_id]
            if name not in player.getAliases():
                player.addAlias(name)
        self.realTimeRound.changePlayerName(player_id, player_location, name)
    super().hooks['changePlayerName'] = onChangePlayerName

    def onChat(self, inEvent: RealTimeEvent):
        """ Function that's called when a chat event occurred.

            :param inEvent:     The chat event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        team = inEvent.parameters['team']
        text = inEvent.parameters['text']

        self.server.InGameAdministration.listenToChat(text, player_id, player_location)
        self.realTimeRound.chat(player_id, player_location, team, text)
    super().hooks['chat'] = onChat

    # noinspection PyMethodMayBeStatic
    def onConnectPlayer(self, inEvent: RealTimeEvent):
        """ Function that's called when a connect player event occurred. Though we believe this event to be dead.

            :param inEvent:     The connect player event.

                note::  Author(s): Mitch """

        log("A connect player event occurred? " + inEvent.eventType, 4)
        pass
    super().hooks['connectPlayer'] = onConnectPlayer

    def onCreatePlayer(self, inEvent: RealTimeEvent):
        """ Function that's called when a player creation event occurred.

            :param inEvent:     The create player event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        name = inEvent.parameters['name']
        is_ai = inEvent.parameters['is_ai']
        team = inEvent.parameters['team']

        new_player = self.realTimeRound.createPlayer(player_id, player_location, name, is_ai, team)
        self.server.PlayerInterface.addPlayer(new_player)
        # Do this to get the IP of the new player
        self.server.MonitoringInterface.bootPlayers()
    super().hooks['createPlayer'] = onCreatePlayer

    def onDestroyPlayer(self, inEvent: RealTimeEvent):
        """ Function that's called when a destroy player event occurred.

            :param inEvent:     The destroy player event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']  # this is None here

        self.realTimeRound.destroyPlayer(player_id, player_location)
        self.server.PlayerInterface.onlinePlayerWithId.pop(player_id)
    super().hooks['destroyPlayer'] = onDestroyPlayer

    def onDestroyVehicle(self, inEvent: RealTimeEvent):
        """ Function that's called when a destroy vehicle event occurred.

            :param inEvent:     The destroy vehicle event.

                note::  Author(s): Mitch """

        if 'player_id' in inEvent.parameters:
            player_id = inEvent.parameters['player_id']
            player_location = inEvent.parameters['player_location']
        else:
            player_id = None
            player_location = None

        vehicle = inEvent.parameters['vehicle']
        vehicle_pos = inEvent.parameters['vehicle_pos']

        self.realTimeRound.destroyVehicle(player_id, player_location, vehicle, vehicle_pos)
    super().hooks['destroyVehicle'] = onDestroyVehicle

    def onDisconnectPlayer(self, inEvent: RealTimeEvent):
        """ Function that's called when a disconnect player event occurred.

            :param inEvent:     The disconnect player event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']

        self.realTimeRound.disconnectPlayer(player_id, player_location)
    super().hooks['disconnectPlayer'] = onDisconnectPlayer

    def onEndMedPack(self, inEvent: RealTimeEvent):
        """ Function that's called when an end med pack event occurred.

            :param inEvent:     The end med pack event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        medpack_status = inEvent.parameters['medpack_status']

        self.realTimeRound.endMedPack(player_id, player_location, medpack_status)
    super().hooks['endMedPack'] = onEndMedPack

    def onEndRepair(self, inEvent: RealTimeEvent):
        """ Function that's called when an end repair event occurred.

            :param inEvent:     The end repair event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        repair_status = inEvent.parameters['repair_status']

        self.realTimeRound.endRepair(player_id, player_location, repair_status)
    super().hooks['endRepair'] = onEndRepair

    def onEnterVehicle(self, inEvent: RealTimeEvent):
        """ Function that's called when an enter vehicle event occurred.

            :param inEvent:     The enter vehicle event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        vehicle_name = inEvent.parameters['vehicle']
        player_seat = inEvent.parameters['pco_id']
        is_default = inEvent.parameters['is_default']
        is_fake = inEvent.parameters['is_fake']

        self.realTimeRound.enterVehicle(player_id, player_location, vehicle_name, player_seat, is_default, is_fake)
    super().hooks['enterVehicle'] = onEnterVehicle

    def onExitVehicle(self, inEvent: RealTimeEvent):
        """ Function that's called when an exit vehicle event occurred.

            :param inEvent:     The exit vehicle event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        vehicle_name = inEvent.parameters['vehicle']
        is_fake = inEvent.parameters['is_fake']

        self.realTimeRound.exitVehicle(player_id, player_location, vehicle_name, is_fake)
    super().hooks['exitVehicle'] = onExitVehicle

    def onPickupFlag(self, inEvent: RealTimeEvent):
        """ Function that's called when a pickup flag event occurred.

            :param inEvent:     The pickup flag event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']

        self.realTimeRound.pickupFlag(player_id, player_location)
    super().hooks['pickupFlag'] = onPickupFlag

    def onPickupKit(self, inEvent: RealTimeEvent):
        """ Function that's called when a pickup kit event occurred.

            :param inEvent:     The pickup kit event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        kit = inEvent.parameters['kit']

        self.realTimeRound.pickupKit(player_id, player_location, kit)
    super().hooks['pickupKit'] = onPickupKit

    def onPlayerKeyHash(self, inEvent: RealTimeEvent):
        """ Function that's called when a player keyhash event occurred.

            :param inEvent:     The player keyhash event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_keyhash = inEvent.parameters['keyhash']

        if self.server.MonitoringInterface.greeting:
            player = self.server.PlayerInterface.onlinePlayerWithId[player_id]
            if BfRounds.getLastInsertedItem().playedThisRound(player):
                self.to_greet.add(player_id)
        self.realTimeRound.playerKeyHash(player_id, player_keyhash)
    super().hooks['playerKeyHash'] = onPlayerKeyHash

    def onRadioMessage(self, inEvent: RealTimeEvent):
        """ Function that's called when a radio message event occurred.

            :param inEvent:     The radio message event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        message = inEvent.parameters['message']
        broadcast = inEvent.parameters['broadcast']

        self.realTimeRound.radioMessage(player_id, player_location, message, broadcast)
    super().hooks['radioMessage'] = onRadioMessage

    def onReSpawnEvent(self, inEvent: RealTimeEvent):
        """ Function that's called when a respawn event occurred.

            :param inEvent:     The respawn event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']

        if player_id in self.to_greet:
            self.server.ConsoleInterface.writeToServer('Welcome ' +
                                                       self.server.PlayerInterface.onlinePlayerWithId[player_id].name +
                                                       ' enjoy your stay')
            self.to_greet.remove(player_id)

        self.realTimeRound.reSpawnEvent(player_id, player_location)
    super().hooks['reSpawnEvent'] = onReSpawnEvent

    def onRestartMap(self, inEvent: RealTimeEvent):
        """ Function that's called when a restart map event occurred.

            :param inEvent:     The restart map event.

                note::  Author(s): Mitch """

        tickets_team1 = inEvent.parameters['tickets_team1']
        tickets_team2 = inEvent.parameters['tickets_team2']

        self.realTimeRound.restartMap(tickets_team1, tickets_team2)
    super().hooks['restartMap'] = onRestartMap

    def onRoundInit(self, inEvent: RealTimeEvent):
        """ Function that's called when a round init event occurred.

            :param inEvent:     The round init event.

                note::  Author(s): Mitch """

        tickets_team1 = inEvent.parameters['tickets_team1']
        tickets_team2 = inEvent.parameters['tickets_team2']

        self.realTimeRound.roundInit(tickets_team1, tickets_team2)
    super().hooks['roundInit'] = onRoundInit

    def onScoreEvent(self, inEvent: RealTimeEvent):
        """ Function that's called when a score event occurred.

            :param inEvent:     The score event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        score_type = inEvent.parameters['score_type']

        if 'victim_id' in inEvent.parameters:
            victim_id = inEvent.parameters['victim_id']
        else:
            victim_id = None

        weapon = inEvent.parameters['weapon']

        self.realTimeRound.scoreEvent(player_id, player_location, score_type, victim_id, weapon)
    super().hooks['scoreEvent'] = onScoreEvent

    def onSetTeam(self, inEvent: RealTimeEvent):
        """ Function that's called when a set team event occurred.

            :param inEvent:     The set team event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']
        team = inEvent.parameters['team']

        self.realTimeRound.setTeam(player_id, player_location, team)
    super().hooks['setTeam'] = onSetTeam

    def onSpawnEvent(self, inEvent: RealTimeEvent):
        """ Function that's called when a spawn event occurred.

            :param inEvent:     The spawn event.

                note::  Author(s): Mitch """

        player_id = inEvent.parameters['player_id']
        player_location = inEvent.parameters['player_location']

        if player_id in self.to_greet:
            self.server.ConsoleInterface.writeToServer('Welcome ' +
                                                       self.server.PlayerInterface.onlinePlayerWithId[player_id].name +
                                                       ' enjoy your stay')
            self.to_greet.remove(player_id)

        self.realTimeRound.spawnEvent(player_id, player_location)
    super().hooks['spawnEvent'] = onSpawnEvent
