from mycroft import MycroftSkill, intent_file_handler


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

    def handle_list_skills(self, message):
        skills = [skill for skill in self.msm.all_skills if not skill.is_local]
        shuffle(skills)
        skills = '. '.join(self.clean_name(skill) for skill in skills[:4])
        skills = skills.replace('skill', '').replace('-', ' ')
        self.speak_dialog('some.available.skills', dict(skills=skills))

    @intent_file_handler('password.intent')
    def handle_password(self, message):
        password = message.data.get("password")
        if password is self.settings["password"]:
            enable = True
            self.speak_dialog('password')
        else:
            enable = False
        self.log.info("skill list") #+mycroft.skills.list)
        self.disable_enable(enable)

    def disable_enable(self, enable=False):
        if self.settings["uespassword"] is True:
            if enable is True:
                self.log.info("manage login")

    def shutdown(self):
        super(Password, self).shutdown()


def create_skill():
    return Password()

