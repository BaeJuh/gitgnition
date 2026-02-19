import uuid

def sendAlarmMsg(sender, receiver, content, important):
	system.util.sendMessage(
		project="Alarm Test",  # 실제 프로젝트 이름으로 변경
        messageHandler="alarm-request",
        payload={
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "important": important
        },
        scope="G"
	)

def sendAlarm(sender, receiver, content):
	base_path = "[Alarm Test Tag Provider]Alarm/AlarmRequest/"
	
	# [Alarm Test Tag Provider]Alarm/AlarmRequest/Content
	
	tags = [
		base_path + "UUID",
		base_path + "Sender",
		base_path + "Receiver",
		base_path + "Content",
		base_path + "Trigger",
	]
	
	system.tag.writeBlocking(tags, [str(uuid.uuid4()), sender, receiver, content, True])
	
	system.util.invokeAsynchronous(resetAlarmTag, base_path + "Trigger")

def resetAlarmTag(trigger_path):
#	import time
	
	time.sleep(0.5)
	
	system.tag.writeBlocking([trigger_path], [False])

def getAlarm():
	
	
	return 