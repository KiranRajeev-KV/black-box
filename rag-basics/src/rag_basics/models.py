from dataclasses import dataclass, field


@dataclass
class Document:
    text: str
    metadata: dict[str, str | int] = field(default_factory=dict)
