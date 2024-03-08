from abc import ABC


class Element(ABC):
    def __init__(self, label: str, **kwargs) -> None:
        self.label = label


class TextInput(Element):
    def __init__(self, label: str, default: str = "", hidden: bool = False, **kwargs) -> None:
        super().__init__(label, **kwargs)
        self.default = default
        self.hidden = hidden


class RadioSelect(Element):
    def __init__(self, label: str, default: int = 0, choices: list[str] = [], **kwargs) -> None:
        super().__init__(label, **kwargs)
        self.choices = choices


class MultiSelect(Element):
    def __init__(self, label: str, default: list[int] = [], choices: list[str] = [], **kwargs) -> None:
        super().__init__(label, **kwargs)
        self.choices = choices
