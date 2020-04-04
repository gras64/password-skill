from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message


class Password(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings["password"] = self.settings.get('password', None)
        self.settings["uespassword"] = self.settings.get('usepassword', False)
        self.add_event('mycroft.awoken', self.handle_password)
        if self.settings["password"] is None:
            self.log.info("no Password found")
            self.shutdown()
        self.add_event('recognizer_loop:sleep',
                   self.handler_sleep)
        if self.settings["uespassword"] is True:
            self.bus.emit(Message('recognizer_loop:sleep'))
            self.enable = False


    def handler_sleep(self):
        self.bus.emit(Message('skillmanager.activate',
                              {'skill': "Password"}))
        self.log.info("handler sleep")



    @intent_file_handler('password.intent')
    def handle_password(self, message):
        password = message.data.get("password")
        self.log.info(self.enable)
        if password is None and self.enable is True:
            self.speak_dialog("say.password")
            self.bus.emit(Message('recognizer_loop:sleep'))
            return
        elif password is None:
            self.log.info("no password found")
            return
        if self.settings["password"] in password:
            self.enable = True
            self.speak_dialog('password')
        else:
            self.enable = False
            self.speak_dialog("wrong.password")
        self.disable_enable()

    def disable_enable(self):
        if self.settings["uespassword"] is True:
            if self.enable is True:
                self.log.info("manage login")
                self.bus.emit(Message('mycroft.awoken'))
                self.enable = False
            else:
                self.log.info("go sleep")
                self.bus.emit(Message('recognizer_loop:sleep'))
        else:
            self.log.info("password deactivated")


    @intent_file_handler('logout.intent')
    def handle_logout(self, message):
        self.enable = False
        self.disable_enable()

    def test(self):
        self.log.info("test")

    def shutdown(self):
        super(Password, self).shutdown()


def create_skill():
    return Password()

