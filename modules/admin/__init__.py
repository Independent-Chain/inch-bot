from modules import ModulesManager

AdminModule: ModulesManager = ModulesManager("group")
AdminModule.connect("modules.admin", "panel")
AdminModule.connect("modules.admin", "statistics")
AdminModule.connect("modules.admin", "mailing")
AdminModule.connect("modules.admin", "constants")
AdminModule.connect("modules.admin", "generate_codes")
AdminModule.connect("modules.admin", "get_codes")