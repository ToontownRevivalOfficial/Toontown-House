from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.task import Task
from toontown.toonbase.AprilToonsGlobals import *

class DistributedAprilToonsMgrAI(DistributedObjectAI):  
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        # Define the default events we want for this year
        self.events = [EventRandomDialogue,
                       EventRandomEffects,
                       EventEstateGravity,
                       EventGlobalGravity,
                       EventSirMaxBirthday]
    
    def getEvents(self):
        return self.events
    
    def isEventActive(self, eventId):
        if not self.air.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False
        return eventId in self.events
    
    def requestEventsList(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'requestEventsListResp', [self.getEvents()])
    
    def toggleEvent(self, eventId):
        if eventId in self.getEvents():
            del self.getEvents()[eventId]
            self.sendUpdate('setEventActive', [eventId, False])
        else:
            self.getEvents().append(eventId)
            self.sendUpdate('setEventActive', [eventId, True])


@magicWord(category=CATEGORY_HEAD, types=[str, str])
def apriltoons(event, active):
    activebool = True if active=='on' else False
    if hasattr(simbase.air, 'aprilToonsMgr') and event in simbase.air.aprilToonsMgr.getEvents():
        simbase.air.aprilToonsMgr.setEventActive(event, activebool)
        return 'April Toons event %s set to %s.' % (event, active)
    return 'Unable to set April Toons event %s to %s.' % (event, active)