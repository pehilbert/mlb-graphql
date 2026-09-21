from mlb_types import HittingStats, HittingStatsItem, HittingStatsResult, PitchingStats, PitchingStatsItem, PitchingStatsResult, Player, PlayerDirectoryItem, SeasonStatsInput, Sport, StatGroupEnum, StatTypeEnum, StatsItem, StatsResult, Team, SportEnum, LeagueEnum, Game, GameTeam, GamesInputType
import requests
import json
from datetime import date, datetime
from functools import lru_cache

BASE_URL = "https://statsapi.mlb.com/api/v1"

@lru_cache(maxsize=64)
def get_sport(sport: SportEnum = SportEnum.MLB) -> list[Sport]:
    response = requests.get(
        f"{BASE_URL}/sports",
        { 'sportId': sport.value }
    )

    results: list[Sport] = []

    for result in json.loads(response.content)['sports']:
        results.append(map_sport(result))

    return results

def get_games(input: GamesInputType) -> list[Game]:
    params = map_games_input_params(input)
    params['sportId'] = SportEnum.MLB.value

    response = requests.get(f"{BASE_URL}/schedule", params)
    result: list[Game] = []

    for games_date in json.loads(response.content)['dates']:
        for game in games_date['games']:
            result.append(map_game(game))

    return result

def get_teams(leagues: list[LeagueEnum] = [LeagueEnum.NATIONAL_LEAGUE, LeagueEnum.AMERICAN_LEAGUE], active_status: bool = True) -> list[Team]:
    response = requests.get(
        f"{BASE_URL}/teams",
        {
            'sportIds': SportEnum.MLB.value,
            'leagueIds': ','.join(league.value for league in leagues),
            'activeStatus': active_status 
        }
    )

    results: list[Team] = []

    for result in json.loads(response.content)['teams']:
        results.append(map_team(result))

    return results

@lru_cache(maxsize=64)
def get_team(team_id: int) -> Team:
    response = requests.get(
        f"{BASE_URL}/teams",
        { 'teamId': team_id }
    )

    return map_team(json.loads(response.content)['teams'][0])

@lru_cache(maxsize=128)
def lookup_player(name: str) -> list[Player]:
    candidate_lookup: dict[int, PlayerDirectoryItem] = {}
    result: list[Player] = []
    player_dir = get_player_directory()

    for player in player_dir:
        if player.name.lower().startswith(name.lower()):
            candidate_lookup[player.id] = player

    if len(candidate_lookup.keys()) > 0:
        response = requests.get(
            f"{BASE_URL}/people",
            { 'personIds': ','.join(str(key) for key in candidate_lookup.keys()) }
        )

        for candidate in json.loads(response.content)['people']:
            result.append(map_player(candidate, candidate_lookup[candidate['id']].current_team_id))

    return result

def get_season_stats(stat_group: StatGroupEnum, input: SeasonStatsInput) -> HittingStatsResult | PitchingStatsResult:
    response = requests.get(
        f"{BASE_URL}/stats",
        map_season_stats_input_params(stat_group, input)
    )

    return map_stats_result(json.loads(response.content)['stats'][0])

def get_player_directory() -> list[PlayerDirectoryItem]:
    response = requests.get(
        f"{BASE_URL}/sports/{SportEnum.MLB.value}/players",
        {
            'fields': 'people,id,fullName,currentTeam'
        }
    )

    result: list[PlayerDirectoryItem] = []

    for player in json.loads(response.content)['people']:
        result.append(map_player_directory_item(player))

    return result

def map_sport(obj) -> Sport:
    return Sport(
        id=obj['id'],
        code=obj['code'],
        name=obj['name'],
        abbreviation=obj['abbreviation'],
        is_active=obj['activeStatus']
    )

def map_games_input_params(input: GamesInputType):
    return {
        'gameTypes': ','.join(game_type.value for game_type in input.game_types),
        'date': input.game_date,
        'startDate': input.date_range.start_date if input.date_range else None,
        'endDate': input.date_range.end_date if input.date_range else None
    }

def map_season_stats_input_params(stat_group: StatGroupEnum, input: SeasonStatsInput):
    return {
        'stats': StatTypeEnum.SEASON.value,
        'group': stat_group.value,
        'gameType': input.game_type.value,
        'season': input.season,
        'teamIds': ','.join(str(id) for id in input.team_ids or []),
        'sortStat': input.sort_stat,
        'position': input.position
    }

def map_team(obj) -> Team:
    return Team(
        id=obj['id'],
        name=obj['name'],
        abbreviation=obj['abbreviation'],
        spring_league=obj['springLeague']['name'],
        league=obj['league']['name'],
        division=obj['division']['name'],
        short_name=obj['shortName'],
        franchise_name=obj['franchiseName'],
        club_name=obj['clubName'],
        is_active=obj['active']
    )

def map_game(obj) -> Game:
    return Game(
        game_pk=obj['gamePk'],
        game_guid=obj['gameGuid'],
        game_type=obj['gameType'],
        season=obj['season'],
        game_date=datetime.fromisoformat(obj['gameDate']),
        official_date=datetime.fromisoformat(obj['gameDate']).date(),
        is_tbd=obj['status']['startTimeTBD'],
        venue=obj['venue']['name'],
        games_in_series=obj['gamesInSeries'],
        series_game_number=obj['seriesGameNumber'],
        status=obj['status']['detailedState'],
        home_team=map_game_team(obj['teams']['home']),
        away_team=map_game_team(obj['teams']['away'])
    )

def map_game_team(obj) -> GameTeam:
    return GameTeam(
        team=get_team(obj['team']['id']),
        record_wins=obj['leagueRecord']['wins'],
        record_losses=obj['leagueRecord']['losses'],
        record_ties=obj['leagueRecord']['ties'],
        winning_pct=obj['leagueRecord']['pct'],
        score=obj['score'] if 'score' in obj.keys() else None
    )

def map_player(obj, current_team_id) -> Player:
    return Player(
        id=obj['id'],
        fullName=obj['fullName'],
        number=obj['primaryNumber'],
        current_team=get_team(current_team_id).abbreviation,
        is_active=obj['active'],
        primary_position=obj['primaryPosition']['abbreviation'],
        bat_side=obj['batSide']['code'],
        pitch_hand=obj['pitchHand']['code']
    )

def map_player_directory_item(obj) -> PlayerDirectoryItem:
    return PlayerDirectoryItem(
        id=obj['id'],
        name=obj['fullName'],
        current_team_id=obj['currentTeam']['id']
    )

def map_hitting_stats(obj) -> HittingStats:
    return HittingStats(
        games_played=obj['gamesPlayed'],
        avg=obj['avg'],
        obp=obj['obp'],
        slg=obj['slg'],
        ops=obj['ops'],
        plate_appearances=obj['plateAppearances'],
        at_bats=obj['atBats'],
        hits=obj['hits'],
        walks=obj['baseOnBalls'],
        rbi=obj['rbi'],
        runs=obj['runs'],
        stolen_bases=obj['stolenBases'],
        caught_stealing=obj['caughtStealing'],
        doubles=obj['doubles'],
        triples=obj['triples'],
        home_runs=obj['homeRuns'],
        total_bases=obj['totalBases'],
        hit_by_pitch=obj['hitByPitch'],
        intentional_walks=obj['intentionalWalks'],
        catchers_interference=obj['catchersInterference'],
        strike_outs=obj['strikeOuts'],
        ground_outs=obj['groundOuts'],
        air_outs=obj['airOuts'],
        ground_into_double_play=obj['groundIntoDoublePlay'],
        sac_bunts=obj['sacBunts'],
        sac_flies=obj['sacFlies'],
        pitches_seen=obj['numberOfPitches'],
        at_bats_per_home_run=obj['atBatsPerHomeRun']
    )

def map_pitching_stats(obj) -> PitchingStats:
    return PitchingStats(
        games_played=obj['gamesPlayed'],
        games_started=obj['gamesStarted'],
        era=obj['era'],
        whip=obj['whip'],
        wins=obj['wins'],
        losses=obj['losses'],
        saves=obj['saves'],
        blown_saves=obj['blownSaves'],
        save_opportunities=obj['saveOpportunities'],
        holds=obj['holds'],
        games_finished=obj['gamesFinished'],
        complete_games=obj['completeGames'],
        shutouts=obj['shutouts'],
        innings_pitched=obj['inningsPitched'],
        earned_runs=obj['earnedRuns'],
        batters_faced=obj['battersFaced'],
        outs=obj['outs'],
        number_of_pitches=obj['numberOfPitches'],
        strikes=obj['strikes'],
        strike_percentage=obj['strikePercentage'],
        balks=obj['balks'],
        wild_pitches=obj['wildPitches'],
        pickoffs=obj['pickoffs'],
        inherited_runners=obj['inheritedRunners'],
        inherited_runners_scored=obj['inheritedRunnersScored'],
        catchers_interference=obj['catchersInterference'],
        hits=obj['hits'],
        runs=obj['runs'],
        strike_outs=obj['strikeOuts'],
        walks=obj['baseOnBalls'],
        intentional_walks=obj['intentionalWalks'],
        hit_by_pitch=obj['hitBatsmen'],
        ground_outs=obj['groundOuts'],
        air_outs=obj['airOuts'],
        ground_into_double_play=obj['groundIntoDoublePlay'],
        pitches_per_inning=obj['pitchesPerInning'],
        strikeouts_per_nine=obj['strikeoutsPer9Inn'],
        walks_per_nine=obj['walksPer9Inn'],
        hits_per_nine=obj['hitsPer9Inn'],
        home_runs_per_nine=obj['homeRunsPer9'],
        runs_scored_per_nine=obj['runsScoredPer9'],
        doubles=obj['doubles'],
        triples=obj['triples'],
        home_runs=obj['homeRuns'],
        avg=obj['avg'],
        obp=obj['obp'],
        slg=obj['slg'],
        ops=obj['ops'],
        total_bases=obj['totalBases'],
        caught_stealing=obj['caughtStealing'],
        stolen_bases=obj['stolenBases'],
        sac_bunts=obj['sacBunts'],
        sac_flies=obj['sacFlies']
    )

def map_stats_result(obj) -> HittingStatsResult | PitchingStatsResult:
    stat_type = StatTypeEnum(obj['type']['displayName'])
    stat_group = StatGroupEnum(obj['group']['displayName'])

    match stat_group:
        case StatGroupEnum.HITTING:
            hitting_splits: list[HittingStatsItem] = []

            for split_obj in obj['splits']:
                hitting_splits.append(HittingStatsItem(
                    player=split_obj['player']['fullName'],
                    position=split_obj['position']['abbreviation'],
                    team=split_obj['team']['name'],
                    league=LeagueEnum(str(split_obj['league']['id'])),
                    sport=SportEnum(str(split_obj['sport']['id'])),
                    num_teams=split_obj['numTeams'],
                    rank=split_obj['rank'],
                    season=split_obj['season'],
                    stats=map_hitting_stats(split_obj['stat'])
                ))

            return HittingStatsResult(stat_type=stat_type, stat_group=stat_group, splits=hitting_splits)

        case StatGroupEnum.PITCHING:
            pitching_splits: list[PitchingStatsItem] = []

            for split_obj in obj['splits']:
                pitching_splits.append(PitchingStatsItem(
                    player=split_obj['player']['fullName'],
                    position=split_obj['position']['abbreviation'],
                    team=split_obj['team']['name'],
                    league=LeagueEnum(str(split_obj['league']['id'])),
                    sport=SportEnum(str(split_obj['sport']['id'])),
                    num_teams=split_obj['numTeams'],
                    rank=split_obj['rank'],
                    season=split_obj['season'],
                    stats=map_pitching_stats(split_obj['stat'])
                ))

            return PitchingStatsResult(stat_type=stat_type, stat_group=stat_group, splits=pitching_splits)