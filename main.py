import strawberry
import mlb_gateway
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from schema.league import League
from schema.sport import Sport

@strawberry.type
class Query:
    @strawberry.field
    def sport(self, id: int) -> Sport:
        return mlb_gateway.get_sport(id)

    @strawberry.field
    def league(self, id: int) -> League:
        return mlb_gateway.get_league(id)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

