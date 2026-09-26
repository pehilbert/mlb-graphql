import strawberry
from typing import Optional

@strawberry.type
class LeagueSeasonDateInfo:
	season_id: Optional[str] = None
	pre_season_start_date: Optional[str] = None
	pre_season_end_date: Optional[str] = None
	season_start_date: Optional[str] = None
	spring_start_date: Optional[str] = None
	spring_end_date: Optional[str] = None
	regular_season_start_date: Optional[str] = None
	last_date_1st_half: Optional[str] = None
	all_star_date: Optional[str] = None
	first_date_2nd_half: Optional[str] = None
	regular_season_end_date: Optional[str] = None
	post_season_start_date: Optional[str] = None
	post_season_end_date: Optional[str] = None
	season_end_date: Optional[str] = None
	offseason_start_date: Optional[str] = None
	off_season_end_date: Optional[str] = None
	season_level_gameday_type: Optional[str] = None
	game_level_gameday_type: Optional[str] = None
	qualifier_plate_appearances: Optional[float] = None
	qualifier_outs_pitched: Optional[float] = None

@strawberry.type
class League:
	id: Optional[int] = None
	name: Optional[str] = None
	abbreviation: Optional[str] = None
	name_short: Optional[str] = None
	season_state: Optional[str] = None
	has_wild_card: Optional[bool] = None
	has_split_season: Optional[bool] = None
	num_games: Optional[int] = None
	has_playoff_points: Optional[bool] = None
	num_teams: Optional[int] = None
	num_wildcard_teams: Optional[int] = None
	season_date_info: Optional[LeagueSeasonDateInfo] = None
	season: Optional[str] = None
	org_code: Optional[str] = None
	conferences_in_use: Optional[bool] = None
	divisions_in_use: Optional[bool] = None
	active: Optional[bool] = None
