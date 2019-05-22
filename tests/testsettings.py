class TestSettings():
    def __init__(self, settings):
        self._settings = settings.copy()

    def isLoaded(self):
        return True

    def addSetting(self, settingKey, settingVal):
    	self._settings[settingKey] = settingVal

    def getSetting(self, settingKey):
        setting = self._settings.get(settingKey)
        return setting if setting else ""

    def getSettingAsBool(self, settingKey): 
        return self.getSetting(settingKey).lower() == "true"