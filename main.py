import mlb_service
from mlb_types import Game, GamesInputType, HittingStatsResult, PitchingStatsResult, Player, SeasonStatsInput, Sport, SportEnum, StatGroupEnum, StatsResult, Team, LeagueEnum
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import statsapi

DEFAULT_LEAGUES = [LeagueEnum.NATIONAL_LEAGUE, LeagueEnum.AMERICAN_LEAGUE]

@strawberry.type
class Query:
    @strawberry.field
    def sport(self, sport: SportEnum) -> list[Sport]:
        return mlb_service.get_sport(sport)

    @strawberry.field
    def teams(self, leagues: list[LeagueEnum] = DEFAULT_LEAGUES, active_teams: bool = True) -> list[Team]:
        return mlb_service.get_teams(leagues, active_teams)

    @strawberry.field
    def games(self, input: GamesInputType) -> list[Game]:
        return mlb_service.get_games(input)

    @strawberry.field
    def player_lookup(self, name: str) -> list[Player]:
        return mlb_service.lookup_player(name)

    @strawberry.field
    def season_stats_hitting(self, input: SeasonStatsInput) -> HittingStatsResult:
        result = mlb_service.get_season_stats(StatGroupEnum.HITTING, input)

        if not isinstance(result, HittingStatsResult):
            raise AttributeError("MLB returned unexpected results")

        return result

    @strawberry.field
    def season_stats_pitching(self, input: SeasonStatsInput) -> PitchingStatsResult:
        result = mlb_service.get_season_stats(StatGroupEnum.PITCHING, input)

        if not isinstance(result, PitchingStatsResult):
            raise AttributeError("MLB returned unexpected results")

        return result

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

