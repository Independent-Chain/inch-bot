from modules import ModulesManager

GroupModule: ModulesManager = ModulesManager("group")
GroupModule.connect("modules.group", "leaderboard")
GroupModule.connect("modules.group", "listing")
