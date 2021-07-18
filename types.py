import typing


class ParentDatabase(typing.NamedTuple):
    database_id: str
    type: str = "database_id"


class NotionPage(typing.NamedTuple):
    parent: typing.Dict[str, typing.Any]
    properties: typing.Dict[str, typing.Any]
    children: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = []