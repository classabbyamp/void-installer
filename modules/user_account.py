from void_installer.module import Module, ModuleSettings


def setup(ctx):
    ctx.add_module(MyCoolModule)


class MyCoolModule(Module):
    id = "user_account"
    name = "User Account"
    desc = "sets up a non-root user"

    class Settings(ModuleSettings):
        username: str
        displayname: str
        password: str
        groups: list[str]
