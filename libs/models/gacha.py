class EventMission:
    def __init__(self, message, progressFrom, progressTo, condition):
        self.message = message
        self.progressFrom = progressFrom
        self.progressTo = progressTo
        self.condition = condition


class gachaInfoServant:
    def __init__(self, isNew, objectId, sellMana, sellQp):
        self.isNew = isNew
        self.objectId = objectId
        self.sellMana = sellMana
        self.sellQp = sellQp
