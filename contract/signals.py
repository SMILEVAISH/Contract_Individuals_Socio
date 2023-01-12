from django.dispatch import Signal

Request_sent = Signal()
Request_viewed = Signal()
Request_canceled = Signal()
Request_rejected = Signal()
Request_accepted = Signal()