import requests
import json
from automapper import mapper
from config.api_config import BASE_URL
from schema.exceptions import NotFoundException, UnexpectedResponseException
from schema.league import League, LeagueSeasonDateInfo, LeagueSport
from schema.sport import Sport
from utils.casing import keys_to_snake_case

def get_sport(sport_id: int) -> Sport:
    response = requests.get(f'{BASE_URL}/sports/{sport_id}')
    results: list[Sport] = []

    try:
        sports = json.loads(response.content)['sports']

        for sport in sports:
            results.append(mapper.to(Sport).map(keys_to_snake_case(sport)))

    except KeyError as e:
        raise UnexpectedResponseException(repr(e))

    if len(results) == 0:
        raise NotFoundException

    return results[0]

def get_league(league_id: int) -> League:
    response = requests.get(f'{BASE_URL}/leagues', { 'leagueIds': str(league_id) })
    results: list[League] = []

    try:
        leagues = json.loads(response.content)['leagues']

        for league in leagues:
            league = keys_to_snake_case(league)

            results.append(mapper.to(League).map(
                league,
                fields_mapping= {
                    'season_date_info': mapper.to(LeagueSeasonDateInfo).map(league['season_date_info']),
                    'sport': mapper.to(LeagueSport).map(league['sport'])
                }
            ))

    except KeyError as e:
        raise UnexpectedResponseException(repr(e))

    if len(results) == 0:
        raise NotFoundException

    return results[0]
