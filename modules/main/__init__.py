from modules import ModulesManager

MainModule: ModulesManager = ModulesManager("main")
MainModule.connect("modules.main", "start")
MainModule.connect("modules.main", "profile")
MainModule.connect("modules.main", "codes")
MainModule.connect("modules.main", "events")
MainModule.connect("modules.main", "mining")
MainModule.connect("modules.main", "upgrades")
MainModule.connect("modules.main", "support")
MainModule.connect("modules.main", "wallet")
