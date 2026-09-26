import strawberry

@strawberry.type
class Sport:
    id: int
    code: str
    name: str
    abbreviation: str
    active_status: bool