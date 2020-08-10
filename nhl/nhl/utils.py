from nhl.models import (Seeding, User, Bracket, SCF, Round0, RoundRobinResult,
                        Round1, Round2, Round3, Round4, PlayerTotals, Tally, PlayoffStatus)
from nhl import mail, db, bcrypt
from flask_mail import Message
from flask import url_for


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='thisis100percentnotfake@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)


def seeding_by_round(round_num, conf):
    seeding_dict = {}
    winners_list = []

    # get a list of the winners from the previous round to make an ordered list of teams remaining and their
    if round_num == 0:
        prev_round = 0
    else:
        prev_round = round_num - 1
    round_winners = Bracket.query.filter_by(round=prev_round).all()

    rr_teams = ["Boston Bruins", "Washington Capitals", "Tampa Bay Lightning", "Philadelphia Flyers",
                "St. Louis Blues", "Colorado Avalanche", "Las Vegas Golden Knights", "Dallas Stars"]

    if round_num == 1:
        for i in rr_teams:
            winners_list.append(i)

    for team in round_winners:
        winners_list.append(team.result)

    seeding = Seeding.query.filter_by(conference=conf).order_by(Seeding.seed.asc())

    seed_number = 1
    for i in seeding:
        if i.team in winners_list:
            seeding_dict[seed_number] = i.team
            seed_number += 1
        else:
            continue

    return seeding_dict


def update_player_totals_r0():
    # add players as keys to dict and in the dict add in round totals and player totals
    players = User.query.all()
    round0 = Bracket.query.filter_by(round=0).all()
    rr = RoundRobinResult.query.first()

    r0_winners = {}
    for match0 in round0:
        r0_winners[match0.game_id] = {'team': match0.result, 'games': match0.games}


    jerk_totals = {}
    for name in players:
        jerk_totals[name.username] = {'round0': 0, 'skaters': 0, 'total': 0}

    # assign the prediction totals to the jerk dict
    for name in players:
        if name.r0_picksin == 'True':
            jerk0 = Round0.query.filter_by(users=name.id).first()

            # get values for the round 0 into the dict

            ###   game 1 east (match 1)
            if jerk0.pick1 == r0_winners[1]['team']:
                games_off = abs(int(r0_winners[1]['games']) - int(jerk0.games1)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 2 east (match 2)
            if jerk0.pick2 == r0_winners[2]['team']:
                games_off = abs(int(r0_winners[2]['games']) - int(jerk0.games2)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 3 east (match 3)
            if jerk0.pick3 == r0_winners[3]['team']:
                games_off = abs(int(r0_winners[3]['games']) - int(jerk0.games3)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 4 east (match 4)
            if jerk0.pick4 == r0_winners[4]['team']:
                games_off = abs(int(r0_winners[4]['games']) - int(jerk0.games4)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 1 west (match 5)
            if jerk0.pick5 == r0_winners[5]['team']:
                games_off = abs(int(r0_winners[5]['games']) - int(jerk0.games5)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 2 west (match 6)
            if jerk0.pick6 == r0_winners[6]['team']:
                games_off = abs(int(r0_winners[6]['games']) - int(jerk0.games6)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 3 west (match 7)
            if jerk0.pick7 == r0_winners[7]['team']:
                games_off = abs(int(r0_winners[7]['games']) - int(jerk0.games7)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ###   game 4 west (match 8)
            if jerk0.pick8 == r0_winners[8]['team']:
                games_off = abs(int(r0_winners[8]['games']) - int(jerk0.games8)) # how many points lost for game pick
                total = 3 - games_off
                jerk_totals[name.username]['round0'] += total
            else:
                jerk_totals[name.username]['round0'] += 0

            ### round robin stuff
            rr_total = 0
            if jerk0.east_team1 == rr.east1:
                rr_total += 1
            if jerk0.east_team2 == rr.east2:
                rr_total += 1
            if jerk0.east_team3 == rr.east3:
                rr_total += 1
            if jerk0.east_team4 == rr.east4:
                rr_total += 1
            if jerk0.west_team1 == rr.west1:
                rr_total += 1
            if jerk0.west_team2 == rr.west2:
                rr_total += 1
            if jerk0.west_team3 == rr.west3:
                rr_total += 1
            if jerk0.west_team4 == rr.west4:
                rr_total += 1

            jerk_totals[name.username]['round0'] += rr_total

            skater = PlayerTotals.query.filter_by(owner=name.username).all()
            points_skater = 0
            for i in skater:
                points_skater += i.points

            jerk_totals[name.username]['skaters'] += points_skater

            jerk_totals[name.username]['total'] = (jerk_totals[name.username]['round0'] +
                                                   jerk_totals[name.username]['skaters'])

            player_tally = Tally.query.filter_by(user=name.username).first()
            player_tally.round0 = jerk_totals[name.username]['round0']
            player_tally.player_totals = jerk_totals[name.username]['skaters']
            player_tally.total_points = jerk_totals[name.username]['total']

            db.session.commit()
        else:
            continue


def update_player_totals_r1():
    # add players as keys to dict and in the dict add in round totals and player totals
    players = User.query.all()
    round1 = Bracket.query.filter_by(round=1).all()

    r1_winners = {}
    for match1 in round1:
        r1_winners[match1.game_id] = {'team': match1.result, 'games': match1.games}

    jerk_totals = {}
    for name in players:
        if name.r1_picksin == 'True':
            jerk_totals[name.username] = {'round1': 0, 'skaters': 0, 'total': 0}

            # get values for the round 1 into the dict
            jerk1 = Round1.query.filter_by(users=name.id).first()

            ###   game 1 east (match 1)
            if jerk1.pick1 == r1_winners[1]['team']:
                games_off = abs(int(r1_winners[1]['games']) - int(jerk1.games1))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 2 east (match 2)
            if jerk1.pick2 == r1_winners[2]['team']:
                games_off = abs(int(r1_winners[2]['games']) - int(jerk1.games2))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 3 east (match 3)
            if jerk1.pick3 == r1_winners[3]['team']:
                games_off = abs(int(r1_winners[3]['games']) - int(jerk1.games3))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 4 east (match 4)
            if jerk1.pick4 == r1_winners[4]['team']:
                games_off = abs(int(r1_winners[4]['games']) - int(jerk1.games4))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 1 west (match 5)
            if jerk1.pick5 == r1_winners[5]['team']:
                games_off = abs(int(r1_winners[5]['games']) - int(jerk1.games5))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 2 west (match 6)
            if jerk1.pick6 == r1_winners[6]['team']:
                games_off = abs(int(r1_winners[6]['games']) - int(jerk1.games6))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 3 west (match 7)
            if jerk1.pick7 == r1_winners[7]['team']:
                games_off = abs(int(r1_winners[7]['games']) - int(jerk1.games7))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            ###   game 4 west (match 8)
            if jerk1.pick8 == r1_winners[8]['team']:
                games_off = abs(int(r1_winners[8]['games']) - int(jerk1.games8))  # how many points lost for game pick
                total = 7 - games_off
                jerk_totals[name.username]['round1'] += total
            else:
                jerk_totals[name.username]['round1'] += 0

            skater = PlayerTotals.query.filter_by(owner=name.username).all()
            points_skater = 0
            for i in skater:
                points_skater += i.points

            jerk_totals[name.username]['skaters'] += points_skater

            # get round 0 value
            jerk_tally = Tally.query.filter_by(user=name.username).first()
            jerk_totals[name.username]['total'] = (jerk_tally.round0 +
                                                   jerk_totals[name.username]['round1'] +
                                                   jerk_totals[name.username]['skaters'])

            jerk_tally.round1 = jerk_totals[name.username]['round1']
            jerk_tally.player_totals = jerk_totals[name.username]['skaters']
            jerk_tally.total_points = jerk_totals[name.username]['total']

            db.session.commit()
        else:
            continue


def update_player_totals_r2():
    # add players as keys to dict and in the dict add in round totals and player totals
    players = User.query.all()
    round2 = Bracket.query.filter_by(round=2).all()

    r2_winners = {}
    for match2 in round2:
        r2_winners[match2.game_id] = {'team': match2.result, 'games': match2.games}

    jerk_totals = {}
    for name in players:
        if name.r2_picksin == 'True':
            jerk_totals[name.username] = {'round2': 0, 'skaters': 0, 'total': 0}

            # get values for the round 2 into the dict
            jerk2 = Round2.query.filter_by(users=name.id).first()

            ###   game 1 east (match 1)
            if jerk2.pick1 == r2_winners[1]['team']:
                games_off = (abs(int(r2_winners[1]['games']) - int(
                    jerk2.games1))) * 2  # how many points lost for game pick
                total = 14 - games_off
                jerk_totals[name.username]['round2'] += total
            else:
                jerk_totals[name.username]['round2'] = 0

            ###   game 2 east (match 2)
            if jerk2.pick2 == r2_winners[2]['team']:
                games_off = (abs(int(r2_winners[2]['games']) - int(
                    jerk2.games2))) * 2  # how many points lost for game pick
                total = 14 - games_off
                jerk_totals[name.username]['round2'] += total
            else:
                jerk_totals[name.username]['round2'] += 0

            ###   game 1 west (match 3)
            if jerk2.pick3 == r2_winners[3]['team']:
                games_off = (abs(int(r2_winners[3]['games']) - int(
                    jerk2.games3))) * 2  # how many points lost for game pick
                total = 14 - games_off
                jerk_totals[name.username]['round2'] += total
            else:
                jerk_totals[name.username]['round2'] += 0

            ###   game 2 west (match 4)
            if jerk2.pick4 == r2_winners[4]['team']:
                games_off = (abs(int(r2_winners[4]['games']) - int(
                    jerk2.games4))) * 2  # how many points lost for game pick
                total = 14 - games_off
                jerk_totals[name.username]['round2'] += total
            else:
                jerk_totals[name.username]['round2'] += 0

            skater = PlayerTotals.query.filter_by(owner=name.username).all()
            points_skater = 0
            for i in skater:
                points_skater += i.points

            jerk_totals[name.username]['skaters'] += points_skater

            # get round 0 and 1 value for totals
            jerk_tally = Tally.query.filter_by(user=name.username).first()
            jerk_totals[name.username]['total'] = (jerk_tally.round0 +
                                                   jerk_tally.round1 +
                                                   jerk_totals[name.username]['round2'] +
                                                   jerk_totals[name.username]['skaters'])

            jerk_tally.round2 = jerk_totals[name.username]['round2']
            jerk_tally.player_totals = jerk_totals[name.username]['skaters']
            jerk_tally.total_points = jerk_totals[name.username]['total']

            db.session.commit()

        else:
            continue


def update_player_totals_r3():
    # add players as keys to dict and in the dict add in round totals and player totals
    players = User.query.all()
    round3 = Bracket.query.filter_by(round=3).all()

    r3_winners = {}
    for match3 in round3:
        r3_winners[match3.game_id] = {'team': match3.result, 'games': match3.games}

    jerk_totals = {}
    for name in players:
        if name.r3_picksin == 'True':
            jerk_totals[name.username] = {'round3': 0, 'skaters': 0, 'total': 0}

            # get values for the round 3 into the dict
            jerk3 = Round3.query.filter_by(users=name.id).first()

            ###   game 1 east (match 1)
            if jerk3.pick1 == r3_winners[1]['team']:
                games_off = (abs(int(r3_winners[1]['games']) - int(
                    jerk3.games1))) * 3  # how many points lost for game pick
                total = 21 - games_off
                jerk_totals[name.username]['round3'] += total
            else:
                jerk_totals[name.username]['round3'] = 0

            ###   game 2 east (match 2)
            if jerk3.pick2 == r3_winners[2]['team']:
                games_off = (abs(int(r3_winners[2]['games']) - int(
                    jerk3.games2))) * 3  # how many points lost for game pick
                total = 21 - games_off
                jerk_totals[name.username]['round3'] += total
            else:
                jerk_totals[name.username]['round3'] += 0

            skater = PlayerTotals.query.filter_by(owner=name.username).all()
            points_skater = 0
            for i in skater:
                points_skater += i.points

            jerk_totals[name.username]['skaters'] += points_skater

            # get round 0 and 1 value for totals
            jerk_tally = Tally.query.filter_by(user=name.username).first()
            jerk_totals[name.username]['total'] = (jerk_tally.round0 +
                                                   jerk_tally.round1 +
                                                   jerk_tally.round2 +
                                                   jerk_totals[name.username]['round3'] +
                                                   jerk_totals[name.username]['skaters'])

            jerk_tally.round3 = jerk_totals[name.username]['round3']
            jerk_tally.player_totals = jerk_totals[name.username]['skaters']
            jerk_tally.total_points = jerk_totals[name.username]['total']

            db.session.commit()
        else:
            continue


def update_player_totals_r4():
    # add players as keys to dict and in the dict add in round totals and player totals
    players = User.query.all()
    round4 = SCF.query.first()

    jerk_totals = {}
    for name in players:
        if name.r4_picksin == 'True':
            jerk_totals[name.username] = {'round4': 0, 'skaters': 0, 'total': 0}

            # get values for the SCF into the dict
            jerk4 = Round4.query.filter_by(users=name.id).first()

            if jerk4.game1 == round4.winner1:
                jerk_totals[name.username]['round4'] += 5
            if jerk4.game2 == round4.winner2:
                jerk_totals[name.username]['round4'] += 5
            if jerk4.game3 == round4.winner3:
                jerk_totals[name.username]['round4'] += 5
            if jerk4.game4 == round4.winner4:
                jerk_totals[name.username]['round4'] += 5
            if jerk4.game5 == round4.winner5:
                jerk_totals[name.username]['round4'] += 5
            if jerk4.game6 == round4.winner6:
                jerk_totals[name.username]['round4'] += 5
            if jerk4.game7 == round4.winner7:
                jerk_totals[name.username]['round4'] += 5

            skater = PlayerTotals.query.filter_by(owner=name.username).all()
            points_skater = 0
            for i in skater:
                points_skater += i.points

            jerk_totals[name.username]['skaters'] += points_skater

            # get round 0 and 1 value for totals
            jerk_tally = Tally.query.filter_by(user=name.username).first()
            jerk_totals[name.username]['total'] = (jerk_tally.round0 +
                                                   jerk_tally.round1 +
                                                   jerk_tally.round2 +
                                                   jerk_tally.round3 +
                                                   jerk_totals[name.username]['round4'] +
                                                   jerk_totals[name.username]['skaters'])

            jerk_tally.round4 = jerk_totals[name.username]['round4']
            jerk_tally.player_totals = jerk_totals[name.username]['skaters']
            jerk_tally.total_points = jerk_totals[name.username]['total']

            db.session.commit()

        else:
            continue


def update_round0_db():
    # add teams to db when you remake the thing for the 1000th time...

    east_ranks = {
        "Boston Bruins" : 1,
        "Washington Capitals": 2,
        "Tampa Bay Lightning": 3,
        "Philadelphia Flyers": 4,
        "Pittsburgh Penguins": 5,
        "Carolina Hurricanes": 6,
        "New York Islanders": 7,
        "Toronto Maple Leafs": 8,
        "Columbus Blue Jackets": 9,
        "Florida Panthers": 10,
        "New York Rangers": 11,
        "Montreal Canadiens": 12
    }

    for key, val in east_ranks.items():
        team_seed = Seeding(conference='east', seed=val, team=key)
        db.session.add(team_seed)
        db.session.commit()

    west_ranks = {
        "St. Louis Blues": 1,
        "Colorado Avalanche": 2,
        "Las Vegas Golden Knights": 3,
        "Dallas Stars": 4,
        "Edmonton Oilers": 5,
        "Nashville Predators": 6,
        "Vancouver Canucks": 7,
        "Calgary Flames": 8,
        "Winnipeg Jets": 9,
        "Minnesota Wild": 10,
        "Arizona Coyotes": 11,
        "Chicago Black Hawks": 12
    }

    for key, val in west_ranks.items():
        team_seed = Seeding(conference='west', seed=val, team=key)
        db.session.add(team_seed)
        db.session.commit()

    status = PlayoffStatus()
    status.round0 = 'Playing'
    status.roundrobin = 'Playing'
    db.session.add(status)
    db.session.commit()


def update_matchups():

    # add in blank options for round 1 - 4
    match0_1 = Bracket(game_id=1, home_team="Toronto Maple Leafs", away_team="Columbus Blue Jackets", round=0)
    match0_2 = Bracket(game_id=2, home_team="Carolina Hurricanes", away_team="New York Rangers", round=0)
    match0_3 = Bracket(game_id=3, home_team="Pittsburgh Penguins", away_team="Montreal Canadiens", round=0)
    match0_4 = Bracket(game_id=4, home_team="New York Islanders", away_team="Florida Panthers", round=0)
    match0_5 = Bracket(game_id=5, home_team="Calgary Flames", away_team="Winnipeg Jets", round=0)
    match0_6 = Bracket(game_id=6, home_team="Nashville Predators", away_team="Arizona Coyotes", round=0)
    match0_7 = Bracket(game_id=7, home_team="Edmonton Oilers", away_team="Chicago Black Hawks", round=0)
    match0_8 = Bracket(game_id=8, home_team="Vancouver Canucks", away_team="Minnesota Wild", round=0)

    db.session.add(match0_1)
    db.session.add(match0_2)
    db.session.add(match0_3)
    db.session.add(match0_4)
    db.session.add(match0_5)
    db.session.add(match0_6)
    db.session.add(match0_7)
    db.session.add(match0_8)

    db.session.commit()

    # add in the blank row for results in Round Robin Result
    rr_blank = RoundRobinResult(east1='TBD', east2='TBD', east3='TBD', east4='TBD',
                                west1='TBD', west2='TBD', west3='TBD', west4='TBD')
    db.session.add(rr_blank)
    db.session.commit()

    # add in blank entries (with only game_id and round) for round 1, 2, and 3
    match1_1 = Bracket(game_id=1, home_team="TBD", away_team="TBD", round=1)
    match1_2 = Bracket(game_id=2, home_team="TBD", away_team="TBD", round=1)
    match1_3 = Bracket(game_id=3, home_team="TBD", away_team="TBD", round=1)
    match1_4 = Bracket(game_id=4, home_team="TBD", away_team="TBD", round=1)
    match1_5 = Bracket(game_id=5, home_team="TBD", away_team="TBD", round=1)
    match1_6 = Bracket(game_id=6, home_team="TBD", away_team="TBD", round=1)
    match1_7 = Bracket(game_id=7, home_team="TBD", away_team="TBD", round=1)
    match1_8 = Bracket(game_id=8, home_team="TBD", away_team="TBD", round=1)

    db.session.add(match1_1)
    db.session.add(match1_2)
    db.session.add(match1_3)
    db.session.add(match1_4)
    db.session.add(match1_5)
    db.session.add(match1_6)
    db.session.add(match1_7)
    db.session.add(match1_8)
    db.session.commit()

    match2_1 = Bracket(game_id=1, home_team="TBD", away_team="TBD", round=2)
    match2_2 = Bracket(game_id=2, home_team="TBD", away_team="TBD", round=2)
    match2_3 = Bracket(game_id=3, home_team="TBD", away_team="TBD", round=2)
    match2_4 = Bracket(game_id=4, home_team="TBD", away_team="TBD", round=2)

    db.session.add(match2_1)
    db.session.add(match2_2)
    db.session.add(match2_3)
    db.session.add(match2_4)
    db.session.commit()

    match3_1 = Bracket(game_id=1, home_team="TBD", away_team="TBD", round=3)
    match3_2 = Bracket(game_id=2, home_team="TBD", away_team="TBD", round=3)

    db.session.add(match3_1)
    db.session.add(match3_2)
    db.session.commit()

    match4_1 = Bracket(game_id=1, home_team="TBD", away_team="TBD", round=4)

    db.session.add(match4_1)
    db.session.commit()

    scf_blank = SCF(winner1='TBD', winner2='TBD', winner3='TBD', winner4='TBD', winner5='TBD', winner6='TBD', winner7='TBD')
    db.session.add(scf_blank)
    db.session.commit()


def update_players():
    player_dict = [
        {
            'username': 'Brian',
            'email': 'admin@nhl.com',
            'password': 'admin'
        },
        {
            'username': 'Evan',
            'email': 'evan@nhl.com',
            'password': 'evan'
        },
        {
            'username': 'Gabe',
            'email': 'gabe@nhl.com',
            'password': 'gabe'
        },
        {
            'username': 'Dallas',
            'email': 'dallas@nhl.com',
            'password': 'dallas'
        },
        {
            'username': 'Mack',
            'email': 'mack@nhl.com',
            'password': 'mack'
        },
        {
            'username': 'Mike B',
            'email': 'mikeb@nhl.com',
            'password': 'mikeb'
        },
        {
            'username': 'Mike Z',
            'email': 'mikez@nhl.com',
            'password': 'mikez'
        },
        {
            'username': 'Mark',
            'email': 'mark@nhl.com',
            'password': 'mark'
        }
    ]

    for play in player_dict:
        hashed_pw = bcrypt.generate_password_hash(play['password']).decode('utf-8')
        user = User(username=play['username'], email=play['email'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()

    for play in player_dict:
        u_tally = Tally(user=play['username'])
        db.session.add(u_tally)
        db.session.commit()

    skaters = {
        'Pastrnak': ['Evan', 0],
        'Perron': ['Evan', 1],
        'Marchand': ['Gabe', 0],
        'Landeskog': ['Gabe', 2],
        'Kucherov': ['Dallas', 2],
        'Stone': ['Dallas', 2],
        'McDavid': ['Mack', 7],
        'Ovechkin': ['Mack', 0],
        'MacKinnon': ['Brian', 2],
        'Point': ['Brian', 2],
        'Draisaitl': ['Mike B', 6],
        'Matthews': ['Mike B', 2],
        'Rantanen': ['Mike Z', 2],
        'Aho': ['Mike Z', 8],
        'OReilly': ['Mark', 1],
        'Bergeron': ['Mark', 1]
    }

    for skater, owner in skaters.items():
        sk = PlayerTotals(player=skater, owner=owner[0], points=owner[1])
        db.session.add(sk)

    db.session.commit()
