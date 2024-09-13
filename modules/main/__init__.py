from modules import ModulesManager

MainModule: ModulesManager = ModulesManager("main")
MainModule.connect("modules.main", "start")

