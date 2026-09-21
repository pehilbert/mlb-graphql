import strawberry
from enum import Enum
from datetime import date, datetime
from dataclasses import field
from typing import Optional

@strawberry.enum
class SportEnum(Enum):
    MLB = '1'

@strawberry.enum
class LeagueEnum(Enum):
    AMERICAN_LEAGUE = '103'
    NATIONAL_LEAGUE = '104'

@strawberry.enum
class GameTypeEnum(Enum):
    REGULAR_SEASON = 'R'
    SPRING_TRAINING = 'S'
    POSTSEASON = 'P'

@strawberry.type
class Sport:
    id: int
    code: str
    name: str
    abbreviation: str
    is_active: bool

@strawberry.type
class Team:
    id: int
    name: str
    abbreviation: str
    spring_league: str
    league: str
    division: str
    short_name: str
    franchise_name: str
    club_name: str
    is_active: bool
    
@strawberry.type
class GameTeam:
    team: Team
    record_wins: int
    record_losses: int
    record_ties: int
    winning_pct: str
    score: Optional[int]

@strawberry.input
class DateRange:
    start_date: date
    end_date: date | None

@strawberry.input
class GamesInputType:
    game_types: list[GameTypeEnum] = field(default_factory=lambda: [GameTypeEnum.REGULAR_SEASON])
    game_date: date = date.today()
    date_range: Optional[DateRange]

@strawberry.type
class Game:
    game_pk: int
    game_guid: str
    game_type: GameTypeEnum
    season: str
    game_date: datetime
    official_date: date
    is_tbd: bool
    games_in_series: int
    series_game_number: int
    venue: str
    status: str
    home_team: GameTeam
    away_team: GameTeam

@strawberry.type
class Player:
    id: int
    fullName: str
    number: str
    current_team: str
    is_active: bool
    primary_position: str
    bat_side: str
    pitch_hand: str

@strawberry.type
class HittingStats:
    avg: str
    obp: str
    slg: str
    ops: str

    games_played: int
    plate_appearances: int
    at_bats: int
    hits: int
    walks: int
    rbi: int
    runs: int
    stolen_bases: int
    caught_stealing: int

    doubles: int
    triples: int
    home_runs: int
    total_bases: int
    hit_by_pitch: int
    intentional_walks: int
    catchers_interference: int

    strike_outs: int
    ground_outs: int
    air_outs: int
    ground_into_double_play: int
    sac_bunts: int
    sac_flies: int
    pitches_seen: int
    at_bats_per_home_run: str

@strawberry.type
class PitchingStats:
    games_played: int
    games_started: int
    era: str
    whip: str
    wins: int
    losses: int
    saves: int
    blown_saves: int
    save_opportunities: int
    holds: int
    games_finished: int
    complete_games: int
    shutouts: int

    innings_pitched: str
    earned_runs: int
    batters_faced: int
    outs: int
    number_of_pitches: int
    strikes: int
    strike_percentage: str
    balks: int
    wild_pitches: int
    pickoffs: int
    inherited_runners: int
    inherited_runners_scored: int
    catchers_interference: int

    hits: int
    runs: int
    strike_outs: int
    walks: int
    intentional_walks: int
    hit_by_pitch: int
    ground_outs: int
    air_outs: int
    ground_into_double_play: int

    pitches_per_inning: str
    strikeouts_per_nine: str
    walks_per_nine: str
    hits_per_nine: str
    home_runs_per_nine: str
    runs_scored_per_nine: str

    doubles: int
    triples: int
    home_runs: int
    avg: str
    obp: str
    slg: str
    ops: str
    total_bases: int
    caught_stealing: int
    stolen_bases: int
    sac_bunts: int
    sac_flies: int

@strawberry.enum
class StatGroupEnum(Enum):
    HITTING = 'hitting'
    PITCHING = 'pitching'

@strawberry.enum
class StatTypeEnum(Enum):
    SEASON = 'season'
    CAREER = 'career'

@strawberry.input
class SeasonStatsInput:
    season: str = str(date.today().year)
    game_type: GameTypeEnum = GameTypeEnum.REGULAR_SEASON
    limit: int = 50
    position: str | None = None
    team_ids: list[int] | None = None
    sort_stat: str | None = None

@strawberry.type
class StatsItem:
    player: str
    position: str
    team: str
    league: LeagueEnum
    sport: SportEnum
    num_teams: int
    rank: int
    season: str

@strawberry.type
class HittingStatsItem(StatsItem):
    stats: HittingStats

@strawberry.type
class PitchingStatsItem(StatsItem):
    stats: PitchingStats

@strawberry.type
class StatsResult:
    stat_type: StatTypeEnum
    stat_group: StatGroupEnum

@strawberry.type
class HittingStatsResult(StatsResult):
    splits: list[HittingStatsItem]

@strawberry.type
class PitchingStatsResult(StatsResult):
    splits: list[PitchingStatsItem]

class PlayerDirectoryItem:
    id: int
    name: str
    current_team_id: int

    def __init__(self, id: int, name: str, current_team_id: int):
        self.id = id
        self.name = name
        self.current_team_id = current_team_id