from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker
from django.db.models import Count

def index(request):
	context = {
		'baseball_leagues': League.objects.filter(sport='Baseball'),
		'womens_leagues': League.objects.filter(name__contains='Womens\''),
		'hockey_leagues': League.objects.filter(sport__contains='Hockey'),
		'non_football_leagues': League.objects.exclude(sport__contains='Football'),
		'conferences': League.objects.filter(name__contains='Conference'),
		'atlantic_leagues': League.objects.filter(name__contains='Atlantic'),
		'dallas_teams': Team.objects.filter(location__contains='Dallas'),
		'raptor_teams': Team.objects.filter(team_name__contains='Raptor'),
		'city_teams': Team.objects.filter(location__contains='City'),
		't_teams': Team.objects.filter(team_name__startswith='T'),
		'alpha_teams': Team.objects.all().order_by('team_name'),
		'alpha_reverse_teams': Team.objects.all().order_by('-team_name'),
		'coopers': Player.objects.filter(last_name='Cooper'),
		'joshuas': Player.objects.filter(first_name='Joshua'),
		'non_josh_coopers': Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua'),
		'alex_wyatts': Player.objects.filter(first_name='Alexander') | Player.objects.filter(first_name='Wyatt'),
	}
	return render(request, 'leagues/index.html', context)

def orm2(request):
	context = {
		# all teams in the Atlantic Soccer Conference
		'asc_teams': Team.objects.filter(league__name='Atlantic Soccer Conference'),
		# all (current) players on the Boston Penguins
		'penguins_roster': Player.objects.filter(curr_team__team_name='Penguins'),
		# all (current) players in the International Collegiate Baseball Conference
		'icbc_curr_players': Player.objects.filter(curr_team__league__name="International Collegiate Baseball Conference").order_by('last_name'),
		# all (current) players in the American Conference of Amateur Football with last name "Lopez"
		'lopez_players': Player.objects.filter(curr_team__league__name='American Conference of Amateur Football') & Player.objects.filter(last_name='Lopez'),
		# all football players
		'football_players': Player.objects.filter(curr_team__league__name__contains='Football'),
		# all teams with a (current) player named "Sophia"
		'sophia_teams': Team.objects.filter(curr_players__first_name='Sophia'),
		# all leagues with a (current) player named "Sophia"
		'sophia_leagues': League.objects.filter(teams__curr_players__first_name='Sophia'),
		# everyone with the last name "Flores" who DOESN'T (currently) play for the Washington Roughriders
		'non_rough_flores': Player.objects.filter(last_name='Flores').exclude(curr_team__team_name='Roughriders'),
		# all teams, past and present, that Samuel Evans has played with
		'sam_evans_teams': Team.objects.filter(all_players__first_name='Samuel', all_players__last_name='Evans'),
		# all players, past and present, with the Manitoba Tiger-Cats
		'man_tc_history': Player.objects.filter(all_teams__location='Manitoba', all_teams__team_name='Tiger-Cats'),
		# all players who were formerly (but aren't currently) with the Wichita Vikings
		'former_vikings': Player.objects.filter(all_teams__location='Wichita', all_teams__team_name='Vikings').exclude(curr_team__location='Wichita', curr_team__team_name='Vikings'),
		# every team that Jacob Gray played for before he joined the Oregon Colts
		'jgray_former_teams': Team.objects.filter(all_players__first_name='Jacob', all_players__last_name='Gray').exclude(location='Oregon', team_name='Colts'),
		# everyone named "Joshua" who has ever played in the Atlantic Federation of Amateur Baseball Players
		'afabp_joshuas': Player.objects.filter(first_name='Joshua', all_teams__league__name='Atlantic Federation of Amateur Baseball Players'),
		# all teams that have had 12 or more players, past and present. (HINT: Look up the Django annotate function.)
		'dozen_teams': Team.objects.annotate(Count('all_players')).filter(all_players__count__gt=11),
		# all players and count of teams played for, sorted by the number of teams they've played for
		'player_team_count': Player.objects.annotate(Count('all_teams')).order_by('-all_teams__count'),
		'leagues': League.objects.all(),
		'teams': Team.objects.all(),
		'players': Player.objects.all(),
	}
	return render(request, 'leagues/orm2.html', context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect('index')