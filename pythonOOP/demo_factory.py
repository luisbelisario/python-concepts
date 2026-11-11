# mostra por que default_factory existe

from dataclasses import dataclass, field

# SEM default_factory (se o Python permitisse — versoes antigas aceitavam)
# Todas as instancias compartilhariam o MESMO dict
# Isso NAO funciona em Python 3.15, entao vamos simular com classe normal:

class ConfigBugado:
    def __init__(self, host="localhost", metadata=None):
        self.host = host
        if metadata is None:
            self.metadata = {}     # cada um tem o seu — jeito certo

class ConfigBugado2:
    metadata = {}      # UM dict pra TODO mundo!

    def __init__(self, host="localhost"):
        self.host = host

c1 = ConfigBugado2()
c2 = ConfigBugado2()
c1.metadata["env"] = "production"
print("Bugado2 c2.metadata:", c2.metadata)   # {'env': 'production'} — VAZOU!

# COM default_factory — cada instancia ganha seu proprio dict
@dataclass
class Config:
    host: str = "localhost"
    metadata: dict = field(default_factory=dict)

c1 = Config()
c2 = Config()
c1.metadata["env"] = "production"
print("Correto c2.metadata:", c2.metadata)   # {} — isolado

# Resumo:
# field(default_factory=dict) = "toda vez que criar uma instancia,
#                                 execute dict() pra gerar um dict novo"
# Isso eh necessario porque:
#   metadata: dict = {}   # NUNCA faça isso — compartilha o mesmo dict
#   metadata: dict = field(default_factory=dict)  # cada um tem o seu