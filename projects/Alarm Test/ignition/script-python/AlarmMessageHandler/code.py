import uuid
import time
from java.util.concurrent import LinkedBlockingQueue, TimeUnit
import alarm_state as state

def processQueue():
    
	base_path = "[Alarm Test Tag Provider]Alarm/AlarmRequest/"
	tags = [
        base_path + "UUID",
        base_path + "Sender",
        base_path + "Receiver",
        base_path + "Content",
        base_path + "Important",
        base_path + "Trigger",
    ]

	try:
		while True:
			item = state.alarmQueue.poll()
			if item is None:
				break

			system.tag.writeBlocking(tags, [
                str(uuid.uuid4()),
                item["sender"],
                item["receiver"],
                item["content"],
                item["important"],
                True
            ])

#            system.tag.writeBlocking(tags, ["", "", "", "", False])
			system.tag.writeBlocking([base_path + "Trigger"], [False])
	finally:
		state.processing = False


def alarmMessageHandler(payload):
    state.alarmQueue.put(payload)

    if not state.processing:
    	state.processing = True
        system.util.invokeAsynchronous(processQueue)