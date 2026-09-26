import strawberry

@strawberry.type
class LeagueSport:
	id: int
	link: str

@strawberry.type
class LeagueSeasonDateInfo:
	season_id: str
	pre_season_start_date: str
	pre_season_end_date: str
	season_start_date: str
	spring_start_date: str
	spring_end_date: str
	regular_season_start_date: str
	last_date_1st_half: str
	all_star_date: str
	first_date_2nd_half: str
	regular_season_end_date: str
	post_season_start_date: str
	post_season_end_date: str
	season_end_date: str
	offseason_start_date: str
	off_season_end_date: str
	season_level_gameday_type: str
	game_level_gameday_type: str
	qualifier_plate_appearances: float
	qualifier_outs_pitched: float

@strawberry.type
class League:
	id: int
	name: str
	link: str
	abbreviation: str
	name_short: str
	season_state: str
	has_wild_card: bool
	has_split_season: bool
	num_games: int
	has_playoff_points: bool
	num_teams: int
	num_wildcard_teams: int
	season_date_info: LeagueSeasonDateInfo
	season: str
	org_code: str
	conferences_in_use: bool
	divisions_in_use: bool
	sport: LeagueSport
	sort_order: int
	active: bool
