import strawberry
from typing import Optional

@strawberry.type
class Sport:
	id: Optional[int] = None
	code: Optional[str] = None
	link: Optional[str] = None
	name: Optional[str] = None
	abbreviation: Optional[str] = None
	active_status: Optional[bool] = None
