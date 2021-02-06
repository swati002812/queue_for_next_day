
from queue_order.queue_manipulator import QueueManipulator

class Queue:

    filename = None
    baseline = None
    def __init__(self, baseline, filename):
        self.filename = filename
        self.baseline = baseline
        self.queueManipulator = QueueManipulator(self.baseline, self.filename)

    def getNextDayQueue(self):
        self.queueManipulator.processFile()
        self.queueManipulator.setCaseType()
        self.queueManipulator.setTempVariableForPersonOnLeave()
        self.queueManipulator.setBinManagerTempVariable()
        self.queueManipulator.markBoldOrMinusOne()
        self.queueManipulator.printQueue()
        self.queueManipulator.print()
        return self.queueManipulator.member_day_data_list
