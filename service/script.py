from core.persist import Base, session

class ScriptService(Base):
    def check_valid_name(self, name):
        pass

    def create_or_update_script(self, name, data):
        if name.startswith("#"):
            script = self.session.query(Script).filter_by(id=int(name[1:])).first()

            if script == None:
                raise ClientEx("Invalid id for script: {}".format(name[1:]))
            else:
                self.update_script(script, name, data)
        else:
            self.create_script(name, data)


    def update_script(self, name, data):
        pass

    def create_script(self, name, data):
        pass

script_service= ScriptService()
