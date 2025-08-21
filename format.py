def get_team_record(team):
    return ('%s    %s - %s - %s   %s PF    %s PA' % 
            (team.display_name, str(team.wins), str(team.losses),
             str(team.ties), str(team.pf), str(team.pa)))


def get_standings_text(teams):
    teams_sorted_by_wins_then_pf = sorted(teams, key=lambda x: (x.wins, x.pf), reverse=True)
    standings_text = [get_team_record(team) for team in teams_sorted_by_wins_then_pf]
    text = ['Standings'] + standings_text
    return '\n'.join(text)


def get_power_rankings_text(scoreboard, teams, roster_ids_to_team_name):
    score = ['%s - %s' % (roster_ids_to_team_name[roster_id], rank)
             for roster_id, rank in scoreboard.items()]
    text = ['Power Rankings'] + score
    return '\n'.join(text)


def get_matchup(team1, team1_score, team2, team2_score):
    return '%s - %s vs %s - %s' % (team1, team1_score, team2, team2_score)


def get_matchups_text(matchups, roster_ids_to_team_name, week):
    matchups_text = [
        get_matchup(roster_ids_to_team_name[matchup.roster_ids[0]], str(matchup.scores[0]),
                    roster_ids_to_team_name[matchup.roster_ids[1]], str(matchup.scores[1]))
                    for count, matchup in enumerate(matchups)]
    text = ['Week ' + str(week)] + matchups_text
    return '\n'.join(text)


def get_trophies_text(data):
    [low_team_name, low_score, high_team_name, high_score, close_winner,
     close_loser, closest_score, blown_out_team_name, ownerer_team_name,
     biggest_blowout] = data
    low_score_str = ['Low score: %s with %.2f points' %
                     (low_team_name, low_score)]
    high_score_str = ['High score: %s with %.2f points' %
                      (high_team_name, high_score)]
    close_score_str = ['%s barely beat %s by a margin of %.2f' %
                       (close_winner, close_loser, closest_score)]
    blowout_str = ['%s blown out by %s by a margin of %.2f' %
                   (blown_out_team_name, ownerer_team_name, biggest_blowout)]

    text = ['Trophies of the week:'] + low_score_str + \
        high_score_str + close_score_str + blowout_str
    return '\n'.join(text)
