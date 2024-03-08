from void_installer import Module, ModuleSettings


def setup(ctx):
    ctx.add_module(MyCoolModule)


class MyCoolModule(Module):
    id = "locale"
    name = "Locale Settings"
    desc = "sets the locale"

    class Settings(ModuleSettings):
        lang: str
        locales: list
