#basic implementation of the observer model
#used to send messages to plugins

from enum import Enum

class ModuleObserver():
    subscribers = {} #dictionary with subscribers per module type

    def subscribe(self, module_type, func):
        if isinstance(module_type, Enum):
            module_type = module_type.value
        if module_type not in self.subscribers:
            self.subscribers[module_type] = set()
        if (func in self.subscribers[module_type]):
            print("func is already subscribed to module")
        else:
            self.subscribers[module_type].add(func)
    
    def unsubscribe(self, module_type, func):
        if func in self.subscribers[module_type]:
            self.subscribers[module_type].discard(func)
            if len(self.subscribers[module_type]) == 0:
                del self.subscribers[module_type]

    def send_message(self, module_target, data):
        if isinstance(module_target, Enum):
            try:
                module_id = module_target.value
            except ValueError:
                print(f"{module_target} not a valid module ID")
        if module_id in self.subscribers:
            for func in self.subscribers[module_id]:
                func(data)
        else:
            print(f"Call to {module_target} made, but no subscribers")