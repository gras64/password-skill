from mycroft import MycroftSkill, intent_file_handler


class Password(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('password.intent')
    def handle_password(self, message):
        self.speak_dialog('password')


def create_skill():
    return Password()

