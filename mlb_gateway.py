import requests
import json
from automapper import mapper
from config.api_config import BASE_URL
from schema.exceptions import NotFoundException, UnexpectedResponseException
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
