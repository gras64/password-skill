from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message


class Password(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings["password"] = self.settings.get('password', None)
        self.settings["uespassword"] = self.settings.get('usepassword', False)
        self.settings["allowskill"] = self.settings.get('allowskill', "")
        if self.settings["password"] is None:
            self.log.info("no Password found")
            self.shutdown()
        self.add_event('recognizer_loop:sleep',
                   self.handler_sleep)
        if self.settings["uespassword"] is True:
            self.bus.emit(Message('recognizer_loop:sleep'))


    def handler_sleep(self):
        self.bus.emit(Message('skillmanager.activate',
                              {'skill': "Password"}))
        self.log.info("handler sleep")



    @intent_file_handler('password.intent')
    def handle_password(self, message):
        password = message.data.get("password")
        self.log.info("found password "+password)
        self.log.info("erwarte password "+self.settings["password"])
        if self.settings["password"] in password:
            enable = True
            self.speak_dialog('password')
        else:
            enable = False
            self.speak_dialog("wrong.password")
        self.disable_enable(enable)

    def disable_enable(self, enable=False):
        if self.settings["uespassword"] is True:
            if enable is True:
                self.log.info("manage login")
                self.bus.emit(Message('mycroft.awoken'))
            else:
                self.log.info("go sleep")
                self.bus.emit(Message('recognizer_loop:sleep'))
        else:
            self.log.info("password deactivated")


    @intent_file_handler('logout.intent')
    def handle_logout(self, message):
        enable = False
        self.disable_enable(enable)

    def shutdown(self):
        super(Password, self).shutdown()


def create_skill():
    return Password()

