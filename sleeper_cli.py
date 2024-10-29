import httputil
import json
import discord_client
from team import Team
from matchup import Matchup
from power_rankings import PowerRankings
from format import (get_standings_text, get_matchups_text,
                    get_power_rankings_text, get_trophies_text)

urls = {
    "get_users": "https://api.sleeper.app/v1/league/{}/users",
    "get_roster": "https://api.sleeper.app/v1/league/{}/rosters",
    "get_matchups": "https://api.sleeper.app/v1/league/{}/matchups/{}"
}


def get_teams(league_id):
    url = urls['get_users'].format(league_id)
    response = httputil.get(url)
    parsed = json.loads(response.read().decode('utf-8'))
    teams = []
    for team in parsed:
        teams.append(Team(team['display_name'], team['user_id']))
    return teams


def get_rosters_keyed_by_owner_id(league_id):
    url = urls['get_roster'].format(league_id)
    response = httputil.get(url)
    parsed = json.loads(response.read().decode('utf-8'))
    rosters_keyed_by_owner_id = {}
    for roster in parsed:
        owner_id = roster['owner_id']
        rosters_keyed_by_owner_id[owner_id] = roster
    return rosters_keyed_by_owner_id


def get_teams_with_roster_data(teams, roster_keyed_by_owner_id):
    for team in teams:
        roster = roster_keyed_by_owner_id[str(team.user_id)]
        wins = roster['settings']['wins']
        losses = roster['settings']['losses']
        ties = roster['settings']['ties']
        pf = roster['settings']['fpts']
        pa = roster['settings']['fpts_against']
        team.add_roster_data(roster['roster_id'], wins, losses, ties, pf, pa)
    return teams


def get_roster_ids_to_team_name(teams):
    roster_ids_to_team_name = {}
    for team in teams:
        roster_ids_to_team_name[team.roster_id] = team.display_name
    return roster_ids_to_team_name


def get_matchups(league_id, number_of_weeks_played):
    matchups = []
    for week in range(1, number_of_weeks_played + 1):
        weekly_matchups = {}
        url = urls['get_matchups'].format(league_id, week)
        response = httputil.get(url)
        parsed = json.loads(response.read().decode('utf-8'))
        for matchup in parsed:
            matchup_id = matchup['matchup_id']
            if matchup_id in weekly_matchups:
                weekly_matchups[matchup_id].add_opponent_data(
                    matchup['roster_id'], matchup['points'])
            else:
                weekly_matchups[matchup_id] = Matchup(
                    matchup['roster_id'], matchup['points'], week)
        matchups.extend(weekly_matchups.values())
    sorted_matchups = sorted(matchups, key=lambda x: x.week, reverse=False)
    return sorted_matchups


def get_matchups_by_week(matchups, week):
    return [matchup for matchup in matchups if matchup.week == week]


def get_trophies(matchups, roster_ids_to_team_name):
    low_score = 9999
    low_team_name = ''
    high_score = -1
    high_team_name = ''
    closest_score = 9999
    close_winner = ''
    close_loser = ''
    biggest_blowout = -1
    blown_out_team_name = ''
    ownerer_team_name = ''

    for matchup in matchups:
        winner_score, winner_roster_id = matchup.get_winner()
        loser_score, loser_roster_id = matchup.get_loser()
        score_difference = matchup.get_score_difference()
        if winner_score > high_score:
            high_score = winner_score
            high_team_name = roster_ids_to_team_name[winner_roster_id]
        if loser_score < low_score:
            low_score = loser_score
            low_team_name = roster_ids_to_team_name[loser_roster_id]
        if score_difference < closest_score:
            closest_score = score_difference
            close_winner = roster_ids_to_team_name[winner_roster_id]
            close_loser = roster_ids_to_team_name[loser_roster_id]
        if score_difference > biggest_blowout:
            biggest_blowout = score_difference
            ownerer_team_name = roster_ids_to_team_name[winner_roster_id]
            blown_out_team_name = roster_ids_to_team_name[loser_roster_id]

    return (low_team_name, low_score, high_team_name, high_score, close_winner,
            close_loser, closest_score, blown_out_team_name, ownerer_team_name,
            biggest_blowout)


def print_choices():
    print()
    print('what would you like to do next?')
    print('1 to post standings')
    print('2 to post power rankings')
    print('3 to post weekly matchups')
    print('4 to post weekly trophies')
    print('5 to send a custom message')


if __name__ == '__main__':
    league_id = 0
    discord_token = ''
    channel_id = ''
    with open('tokens.json') as f:
        tokens = json.load(f)
        discord_token = tokens['discordToken']
        channel_id = tokens['channelId']
        league_id = tokens['sleeperLeagueId']
    number_of_weeks_played = int(input('enter number of weeks played:\n'))
    print('gathering data for {} weeks of play\n'.format(
        str(number_of_weeks_played)))
    teams = get_teams(league_id)
    rosters_keyed_by_owner_id = get_rosters_keyed_by_owner_id(league_id)
    teams = get_teams_with_roster_data(teams, rosters_keyed_by_owner_id)
    roster_ids_to_team_name = get_roster_ids_to_team_name(teams)
    matchups = get_matchups(league_id, number_of_weeks_played)
    for week in range(1, number_of_weeks_played + 1):
        weekly_matchups = get_matchups_by_week(matchups, week)
        print(get_matchups_text(weekly_matchups, roster_ids_to_team_name, week))
        print(get_trophies_text(get_trophies(
            weekly_matchups, roster_ids_to_team_name)))
        print()
    power_rankings = PowerRankings(matchups, len(teams))
    scoreboard = power_rankings.get_scoreboard(0.5)
    print(get_power_rankings_text(scoreboard, teams, roster_ids_to_team_name))
    print()
    print(get_standings_text(teams))
    discordClient = discord_client.DiscordClient(discord_token, channel_id)
    print_choices()
    choice = input('any other key to exit\n')
    while choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice == '5':
        message = ''
        if choice == '1':
            message = get_standings_text(teams)
        elif choice == '2':
            message = get_power_rankings_text(
                scoreboard, teams, roster_ids_to_team_name)
        elif choice == '3':
            week = int(input('enter week\n'))
            message = get_matchups_text(
                weekly_matchups, roster_ids_to_team_name, week)
        elif choice == '4':
            week = int(input('enter week\n'))
            message = get_trophies_text(get_trophies(
                weekly_matchups, roster_ids_to_team_name))
        elif choice == '5':
            message = input('enter your message\n')
        print()
        print('the message to be sent is: \n')
        print(message)
        print('ok to send?')
        final_say = input('y for yes or any other key for no\n')
        if final_say == 'y' or final_say == 'Y':
            discordClient.send_message(message)
        print_choices()
        choice = input('any other key to exit\n')
