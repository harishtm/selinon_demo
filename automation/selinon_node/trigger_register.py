from settings.singleton import Singleton


class TriggerRegistry(metaclass=Singleton):
    """
        Register the trigger based on store
    """

    def __init__(self, cls, scope=None, intent=None, trigger=None):
        """
        Initialization of new registered trigger
        """
        self.trigger_registry = {}
        self.trigger_registry['trigger'] = []
        self.trigger_registry['trigger'].append({cls: {'scope': scope, 'intent': intent}})

    def update(self, previous_trigger):
        self.trigger_registry['trigger'].append(previous_trigger)