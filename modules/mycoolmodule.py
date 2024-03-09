from void_installer.module import Module, ModuleSettings


def setup(ctx):
    ctx.add_module(MyCoolModule)


class MyCoolModule(Module):
    id = "mycoolmodule"
    name = "My Cool Module"
    desc = "sets some cool things"
    order = 20

    class Settings(ModuleSettings):
        foo: str
