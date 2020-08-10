from nhl.models import (User, Round0, Round1, Round2, Round3, Round4, Seeding,
                        Tally, Bracket, PlayoffStatus, RoundRobinResult, PlayerTotals, SCF)
from flask import render_template, url_for, flash, redirect, request
from nhl.forms import (RegistrationForm, LoginForm, PlayerPicks0, PlayerPicks1, PlayerPicks2, PlayerPicks3,
                       PlayerPicks4, UpdateSeeding, RequestResetForm, ResultForm0, MatchupForm, ResultForm1, ResultForm2,
                       ResultForm3, ResultForm4, SkaterTotalForm)
from nhl import app, db, bcrypt
from nhl.utils import (send_reset_email, seeding_by_round, update_player_totals_r0, update_player_totals_r1,
                       update_player_totals_r2, update_player_totals_r3, update_player_totals_r4)
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    return render_template('home.html', user=user)


@app.route("/standings")
def standings():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    # update standings to include
    status = PlayoffStatus.query.filter_by(id=1).first()

    # update the player totals even if round not done yet
    players = User.query.all()
    for name in players:
        player_tally = Tally.query.filter_by(user=name.username).first()
        skater = PlayerTotals.query.filter_by(owner=name.username).all()
        points_skater = 0
        for i in skater:
            points_skater += i.points
        player_tally.player_totals = points_skater
        player_tally.total_points = points_skater
        db.session.commit()

    if status.round0 == 'True' and status.roundrobin == 'True':
        update_player_totals_r0()

    if status.round1 == 'True':
        update_player_totals_r1()

    if status.round2 == 'True':
        update_player_totals_r2()

    if status.round3 == 'True':
        update_player_totals_r3()

    if status.round4 == 'True':
        update_player_totals_r4()

    totals = Tally.query.filter().order_by(Tally.total_points.desc())

    return render_template('standings.html', user=user, totals=totals)


@app.route("/everyone")
def everyone():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    everyone0 = Round0.query.all()
    everyone1 = Round1.query.all()
    everyone2 = Round2.query.all()
    everyone3 = Round3.query.all()
    everyone4 = Round4.query.all()

    return render_template('everyone.html', user=user, everyone0=everyone0, everyone1=everyone1,
                           everyone2=everyone2, everyone3=everyone3, everyone4=everyone4)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        player_tally = Tally(user=form.username.data, round0=0, round1=0, round2=0, round3=0, round4=0, player_totals=0, total_points=0)
        db.session.add(user)
        db.session.add(player_tally)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, user=user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('home.html', title='Reset Password')


@app.route("/seeding", methods=['GET', 'POST'])
@login_required
def update_seeding():
    if current_user.is_authenticated:
        # get the results from the round 0 round robin and redistribute the 1 - 4 seeds for teams
        status = PlayoffStatus.query.filter_by(id=1).first()

        seed1_e = Seeding.query.filter_by(conference='east', seed=1).first()
        seed2_e = Seeding.query.filter_by(conference='east', seed=2).first()
        seed3_e = Seeding.query.filter_by(conference='east', seed=3).first()
        seed4_e = Seeding.query.filter_by(conference='east', seed=4).first()
        seed1_w = Seeding.query.filter_by(conference='west', seed=1).first()
        seed2_w = Seeding.query.filter_by(conference='west', seed=2).first()
        seed3_w = Seeding.query.filter_by(conference='west', seed=3).first()
        seed4_w = Seeding.query.filter_by(conference='west', seed=4).first()

        if status.roundrobin == 'True':
            rr_results = RoundRobinResult.query.first()
            seed1_e.team = rr_results.east1
            seed2_e.team = rr_results.east2
            seed3_e.team = rr_results.east3
            seed4_e.team = rr_results.east4

            seed1_w.team = rr_results.west1
            seed2_w.team = rr_results.west2
            seed3_w.team = rr_results.west3
            seed4_w.team = rr_results.west4

            db.session.commit()

            flash('Seeding has been updated', 'success')
            return redirect(url_for('home'))


@app.route("/bracket", methods=['GET', 'POST'])
@login_required
def bracket():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    status = PlayoffStatus.query.filter_by(id=1).first()
    return render_template('bracket.html', title='Bracket', user=user, status=status)


@app.route("/bracket/update_matchups", methods=['GET', 'POST'])
@login_required
def update_matchups():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    status = PlayoffStatus.query.filter_by(id=1).first()

    ## Round 0
    if status.round0 == 'False' and status.roundrobin == 'False':
        round_num = 0
        seeds_east = seeding_by_round(round_num, 'east')
        seeds_west = seeding_by_round(round_num, 'west')

        match1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
        match2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
        match3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
        match4 = Bracket.query.filter_by(round=round_num, game_id=4).first()

        match5 = Bracket.query.filter_by(round=round_num, game_id=5).first()
        match6 = Bracket.query.filter_by(round=round_num, game_id=6).first()
        match7 = Bracket.query.filter_by(round=round_num, game_id=7).first()
        match8 = Bracket.query.filter_by(round=round_num, game_id=8).first()

        ## East
        match1.home_team = seeds_east[8]
        match1.away_team = seeds_east[9]
        match2.home_team = seeds_east[6]
        match2.away_team = seeds_east[11]
        match3.home_team = seeds_east[5]
        match3.away_team = seeds_east[12]
        match4.home_team = seeds_east[7]
        match4.away_team = seeds_east[10]

        ## West
        match5.home_team = seeds_west[8]
        match5.away_team = seeds_west[9]
        match6.home_team = seeds_west[6]
        match6.away_team = seeds_west[11]
        match7.home_team = seeds_west[5]
        match7.away_team = seeds_west[12]
        match8.home_team = seeds_west[7]
        match8.away_team = seeds_west[10]

        status.round0 = 'Playing'
        status.roundrobin = 'Playing'

        db.session.commit()
        flash('Matchups have been updated based on seedings', 'success')
        return redirect(url_for('home'))

    ## Round 1
    elif status.round0 == 'True' and status.roundrobin == 'True' and status.round1 == 'False':
        round_num = 1
        seeds_east = seeding_by_round(round_num, 'east')
        seeds_west = seeding_by_round(round_num, 'west')

        match1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
        match2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
        match3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
        match4 = Bracket.query.filter_by(round=round_num, game_id=4).first()

        match5 = Bracket.query.filter_by(round=round_num, game_id=5).first()
        match6 = Bracket.query.filter_by(round=round_num, game_id=6).first()
        match7 = Bracket.query.filter_by(round=round_num, game_id=7).first()
        match8 = Bracket.query.filter_by(round=round_num, game_id=8).first()

        ## East
        match1.home_team = seeds_east[1]
        match1.away_team = seeds_east[8]
        match2.home_team = seeds_east[2]
        match2.away_team = seeds_east[7]
        match3.home_team = seeds_east[3]
        match3.away_team = seeds_east[6]
        match4.home_team = seeds_east[4]
        match4.away_team = seeds_east[5]

        ## West
        match5.home_team = seeds_west[1]
        match5.away_team = seeds_west[8]
        match6.home_team = seeds_west[2]
        match6.away_team = seeds_west[7]
        match7.home_team = seeds_west[3]
        match7.away_team = seeds_west[6]
        match8.home_team = seeds_west[4]
        match8.away_team = seeds_west[5]

        status.round1 = 'Playing'
        db.session.commit()
        flash('Matchups have been updated based on seedings', 'success')
        return redirect(url_for('home'))

    ## Round 2
    elif status.round1 == 'True' and status.round2 == 'False':
        round_num = 2
        seeds_east = seeding_by_round(round_num, 'east')
        seeds_west = seeding_by_round(round_num, 'west')

        match1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
        match2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
        match3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
        match4 = Bracket.query.filter_by(round=round_num, game_id=4).first()

        ## East
        match1.home_team = seeds_east[1]
        match1.away_team = seeds_east[4]
        match2.home_team = seeds_east[2]
        match2.away_team = seeds_east[3]
        match3.home_team = seeds_west[1]
        match3.away_team = seeds_west[4]
        match4.home_team = seeds_west[2]
        match4.away_team = seeds_west[3]

        status.round2 = 'Playing'
        db.session.commit()
        flash('Matchups have been updated based on seedings', 'success')
        return redirect(url_for('home'))

    ## Round 3
    elif status.round2 == 'True' and status.round3 == 'False':
        round_num = 3
        seeds_east = seeding_by_round(round_num, 'east')
        seeds_west = seeding_by_round(round_num, 'west')

        match1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
        match2 = Bracket.query.filter_by(round=round_num, game_id=2).first()

        ## East
        match1.home_team = seeds_east[1]
        match1.away_team = seeds_east[2]
        match2.home_team = seeds_west[1]
        match2.away_team = seeds_west[2]

        status.round3 = 'Playing'
        db.session.commit()
        flash('Matchups have been updated based on seedings', 'success')
        return redirect(url_for('home'))

    ## Round 4
    elif status.round3 == 'True' and status.round4 == 'False':
        round_num = 4
        seeds_east = seeding_by_round(round_num, 'east')
        seeds_west = seeding_by_round(round_num, 'west')

        match1 = Bracket.query.filter_by(round=round_num, game_id=1).first()

        ## East
        match1.home_team = seeds_east[1]
        match1.away_team = seeds_west[1]

        status.round4 = 'Playing'
        db.session.commit()
        flash('Matchups have been updated based on seedings', 'success')
        return redirect(url_for('home'))
    else:
        return(redirect(url_for('home')))



@app.route("/bracket/update_results0", methods=['GET', 'POST'])
@login_required
def update_results0():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 0
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
    matchup3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
    matchup4 = Bracket.query.filter_by(round=round_num, game_id=4).first()
    matchup5 = Bracket.query.filter_by(round=round_num, game_id=5).first()
    matchup6 = Bracket.query.filter_by(round=round_num, game_id=6).first()
    matchup7 = Bracket.query.filter_by(round=round_num, game_id=7).first()
    matchup8 = Bracket.query.filter_by(round=round_num, game_id=8).first()

    rr = RoundRobinResult.query.first()
    status = PlayoffStatus.query.filter_by(id=1).first()
    seed1_e = Seeding.query.filter_by(conference='east', seed=1).first()
    seed2_e = Seeding.query.filter_by(conference='east', seed=2).first()
    seed3_e = Seeding.query.filter_by(conference='east', seed=3).first()
    seed4_e = Seeding.query.filter_by(conference='east', seed=4).first()
    seed1_w = Seeding.query.filter_by(conference='west', seed=1).first()
    seed2_w = Seeding.query.filter_by(conference='west', seed=2).first()
    seed3_w = Seeding.query.filter_by(conference='west', seed=3).first()
    seed4_w = Seeding.query.filter_by(conference='west', seed=4).first()

    form = ResultForm0()

    form.winner1.choices = [(matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.winner2.choices = [(matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]
    form.winner3.choices = [(matchup3.home_team, matchup3.home_team), (matchup3.away_team, matchup3.away_team)]
    form.winner4.choices = [(matchup4.home_team, matchup4.home_team), (matchup4.away_team, matchup4.away_team)]
    form.winner5.choices = [(matchup5.home_team, matchup5.home_team), (matchup5.away_team, matchup5.away_team)]
    form.winner6.choices = [(matchup6.home_team, matchup6.home_team), (matchup6.away_team, matchup6.away_team)]
    form.winner7.choices = [(matchup7.home_team, matchup7.home_team), (matchup7.away_team, matchup7.away_team)]
    form.winner8.choices = [(matchup8.home_team, matchup8.home_team), (matchup8.away_team, matchup8.away_team)]
    form.east1.choices = [(seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.east2.choices = [(seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.east3.choices = [(seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.east4.choices = [(seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.west1.choices = [(seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]
    form.west2.choices = [(seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]
    form.west3.choices = [(seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]
    form.west4.choices = [(seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]

    if request.method == 'POST' and form.validate_on_submit():
        matchup1.result = form.winner1.data
        matchup1.games = form.games1.data

        matchup2.result = form.winner2.data
        matchup2.games = form.games2.data

        matchup3.result = form.winner3.data
        matchup3.games = form.games3.data

        matchup4.result = form.winner4.data
        matchup4.games = form.games4.data

        matchup5.result = form.winner5.data
        matchup5.games = form.games5.data

        matchup6.result = form.winner6.data
        matchup6.games = form.games6.data

        matchup7.result = form.winner7.data
        matchup7.games = form.games7.data

        matchup8.result = form.winner8.data
        matchup8.games = form.games8.data

        rr.east1 = form.east1.data
        rr.east2 = form.east2.data
        rr.east3 = form.east3.data
        rr.east4 = form.east4.data
        rr.west1 = form.west1.data
        rr.west2 = form.west2.data
        rr.west3 = form.west3.data
        rr.west4 = form.west4.data

        # change the seeding from the results
        seed1_e.team = form.east1.data
        seed2_e.team = form.east2.data
        seed3_e.team = form.east3.data
        seed4_e.team = form.east4.data
        seed1_w.team = form.west1.data
        seed2_w.team = form.west2.data
        seed3_w.team = form.west3.data
        seed4_w.team = form.west4.data

        status.round0 = 'True'
        status.roundrobin = 'True'

        db.session.commit()
        flash('Updated results for Round 0', 'success')
        return redirect(url_for('update_seeding'))
    return render_template('winners0.html', title='Results', user=user, form=form, round=0)


@app.route("/bracket/update_results1", methods=['GET', 'POST'])
@login_required
def update_results1():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 1
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
    matchup3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
    matchup4 = Bracket.query.filter_by(round=round_num, game_id=4).first()
    matchup5 = Bracket.query.filter_by(round=round_num, game_id=5).first()
    matchup6 = Bracket.query.filter_by(round=round_num, game_id=6).first()
    matchup7 = Bracket.query.filter_by(round=round_num, game_id=7).first()
    matchup8 = Bracket.query.filter_by(round=round_num, game_id=8).first()

    status = PlayoffStatus.query.filter_by(id=1).first()

    form = ResultForm1()

    form.winner1.choices = [(matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.winner2.choices = [(matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]
    form.winner3.choices = [(matchup3.home_team, matchup3.home_team), (matchup3.away_team, matchup3.away_team)]
    form.winner4.choices = [(matchup4.home_team, matchup4.home_team), (matchup4.away_team, matchup4.away_team)]
    form.winner5.choices = [(matchup5.home_team, matchup5.home_team), (matchup5.away_team, matchup5.away_team)]
    form.winner6.choices = [(matchup6.home_team, matchup6.home_team), (matchup6.away_team, matchup6.away_team)]
    form.winner7.choices = [(matchup7.home_team, matchup7.home_team), (matchup7.away_team, matchup7.away_team)]
    form.winner8.choices = [(matchup8.home_team, matchup8.home_team), (matchup8.away_team, matchup8.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        matchup1.result = form.winner1.data
        matchup1.games = form.games1.data

        matchup2.result = form.winner2.data
        matchup2.games = form.games2.data

        matchup3.result = form.winner3.data
        matchup3.games = form.games3.data

        matchup4.result = form.winner4.data
        matchup4.games = form.games4.data

        matchup5.result = form.winner5.data
        matchup5.games = form.games5.data

        matchup6.result = form.winner6.data
        matchup6.games = form.games6.data

        matchup7.result = form.winner7.data
        matchup7.games = form.games7.data

        matchup8.result = form.winner8.data
        matchup8.games = form.games8.data

        status.round1 = 'True'

        db.session.commit()
        flash('Updated results for Round 1', 'success')
        return redirect(url_for('update_seeding'))
    return render_template('winners1.html', title='Results', user=user, form=form)


@app.route("/bracket/update_results2", methods=['GET', 'POST'])
@login_required
def update_results2():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 2
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
    matchup3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
    matchup4 = Bracket.query.filter_by(round=round_num, game_id=4).first()

    status = PlayoffStatus.query.filter_by(id=1).first()

    form = ResultForm2()

    form.winner1.choices = [(matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.winner2.choices = [(matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]
    form.winner3.choices = [(matchup3.home_team, matchup3.home_team), (matchup3.away_team, matchup3.away_team)]
    form.winner4.choices = [(matchup4.home_team, matchup4.home_team), (matchup4.away_team, matchup4.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        matchup1.result = form.winner1.data
        matchup1.games = form.games1.data

        matchup2.result = form.winner2.data
        matchup2.games = form.games2.data

        matchup3.result = form.winner3.data
        matchup3.games = form.games3.data

        matchup4.result = form.winner4.data
        matchup4.games = form.games4.data

        status.round2 = 'True'
        db.session.commit()
        flash('Updated results for Round 2', 'success')
        return redirect(url_for('standings'))
    return render_template('winners2.html', title='Round 2 results', user=user, form=form)


@app.route("/bracket/update_results3", methods=['GET', 'POST'])
@login_required
def update_results3():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 3
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()

    status = PlayoffStatus.query.filter_by(id=1).first()

    form = ResultForm3()

    form.winner1.choices = [(matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.winner2.choices = [(matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        matchup1.result = form.winner1.data
        matchup1.games = form.games1.data

        matchup2.result = form.winner2.data
        matchup2.games = form.games2.data

        status.round3 = 'True'
        db.session.commit()
        flash('Updated results for Round 3', 'success')
        return redirect(url_for('update_seeding'))
    return render_template('winners3.html', title='Results', user=user, form=form)


@app.route("/bracket/update_results4", methods=['GET', 'POST'])
@login_required
def update_results4():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 4
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    status = PlayoffStatus.query.filter_by(id=1).first()
    scf_result = SCF.query.first()

    form = ResultForm4()
    form.winner.choices = [(matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        if form.game_number.data == '1':
            scf_result.winner1 = form.winner.data
            db.session.commit()
        elif form.game_number.data == '2':
            scf_result.winner2 = form.winner.data
            db.session.commit()
        elif form.game_number.data == '3':
            scf_result.winner3 = form.winner.data
            db.session.commit()
        elif form.game_number.data == '4':
            scf_result.winner4 = form.winner.data
            db.session.commit()
        elif form.game_number.data == '5':
            scf_result.winner5 = form.winner.data
            db.session.commit()
        elif form.game_number.data == '6':
            scf_result.winner6 = form.winner.data
            db.session.commit()
        elif form.game_number.data == '7':
            scf_result.winner7 = form.winner.data
            status.round4 = 'True'
            db.session.commit()

        update_player_totals_r4()
        flash('Game winner updated', 'success')
        return redirect(url_for('standings'))
    return render_template('winners4.html', form=form, user=user)


@app.route("/skaters", methods=['GET', 'POST'])
@login_required
def update_skaters():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    form = SkaterTotalForm()
    if request.method == 'POST' and form.validate_on_submit():
        sk1 = PlayerTotals.query.filter_by(player='Pastrnak').first()
        sk1.points = form.evan1.data
        sk2 = PlayerTotals.query.filter_by(player='Perron').first()
        sk2.points = form.evan2.data
        sk3 = PlayerTotals.query.filter_by(player='Marchand').first()
        sk3.points = form.gabe1.data
        sk4 = PlayerTotals.query.filter_by(player='Landeskog').first()
        sk4.points = form.gabe2.data
        sk5 = PlayerTotals.query.filter_by(player='Kucherov').first()
        sk5.points = form.dallas1.data
        sk6 = PlayerTotals.query.filter_by(player='Stone').first()
        sk6.points = form.dallas2.data
        sk7 = PlayerTotals.query.filter_by(player='McDavid').first()
        sk7.points = form.mack1.data
        sk8 = PlayerTotals.query.filter_by(player='Ovechkin').first()
        sk8.points = form.mack2.data
        sk9 = PlayerTotals.query.filter_by(player='MacKinnon').first()
        sk9.points = form.brian1.data
        sk10 = PlayerTotals.query.filter_by(player='Point').first()
        sk10.points = form.brian2.data
        sk11 = PlayerTotals.query.filter_by(player='Draisaitl').first()
        sk11.points = form.mikeb1.data
        sk12 = PlayerTotals.query.filter_by(player='Matthews').first()
        sk12.points = form.mikeb2.data
        sk13 = PlayerTotals.query.filter_by(player='Rantanen').first()
        sk13.points = form.mikez1.data
        sk14 = PlayerTotals.query.filter_by(player='Aho').first()
        sk14.points = form.mikez2.data
        sk15 = PlayerTotals.query.filter_by(player='OReilly').first()
        sk15.points = form.mark1.data
        sk16 = PlayerTotals.query.filter_by(player='Bergeron').first()
        sk16.points = form.mark2.data
        db.session.commit()

        flash('skaters totals added to db', 'success')
        return redirect(url_for('standings'))
    return render_template('skaters.html', user=user, form=form)



@app.route("/picks")
@login_required
def picks():
    if current_user.is_authenticated:
        user = current_user
    else:
        user= None
    # check to see if rounds have been set up yet
    status = PlayoffStatus.query.filter_by(id=1).first()

    # determine if the player has already made picks
    user_playin = Round0.query.filter_by(users=user.id).first()
    user_round1 = Round1.query.filter_by(users=user.id).first()
    user_round2 = Round2.query.filter_by(users=user.id).first()
    user_round3 = Round3.query.filter_by(users=user.id).first()
    user_round4 = Round4.query.filter_by(users=user.id).first()

    return render_template('picks.html', user=current_user, playin=user_playin, round1=user_round1,
                           round2=user_round2, round3=user_round3, round4=user_round4, status=status)


@app.route("/picks/playin", methods=['GET', 'POST'])
@login_required
def playin():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    round_num = 0

    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
    matchup3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
    matchup4 = Bracket.query.filter_by(round=round_num, game_id=4).first()
    matchup5 = Bracket.query.filter_by(round=round_num, game_id=5).first()
    matchup6 = Bracket.query.filter_by(round=round_num, game_id=6).first()
    matchup7 = Bracket.query.filter_by(round=round_num, game_id=7).first()
    matchup8 = Bracket.query.filter_by(round=round_num, game_id=8).first()
    seed1_e = Seeding.query.filter_by(conference='east', seed=1).first()
    seed2_e = Seeding.query.filter_by(conference='east', seed=2).first()
    seed3_e = Seeding.query.filter_by(conference='east', seed=3).first()
    seed4_e = Seeding.query.filter_by(conference='east', seed=4).first()
    seed1_w = Seeding.query.filter_by(conference='west', seed=1).first()
    seed2_w = Seeding.query.filter_by(conference='west', seed=2).first()
    seed3_w = Seeding.query.filter_by(conference='west', seed=3).first()
    seed4_w = Seeding.query.filter_by(conference='west', seed=4).first()

    form = PlayerPicks0()
    form.match1.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.match2.choices = [("", ""), (matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]
    form.match3.choices = [("", ""), (matchup3.home_team, matchup3.home_team), (matchup3.away_team, matchup3.away_team)]
    form.match4.choices = [("", ""), (matchup4.home_team, matchup4.home_team), (matchup4.away_team, matchup4.away_team)]
    form.match5.choices = [("", ""), (matchup5.home_team, matchup5.home_team), (matchup5.away_team, matchup5.away_team)]
    form.match6.choices = [("", ""), (matchup6.home_team, matchup6.home_team), (matchup6.away_team, matchup6.away_team)]
    form.match7.choices = [("", ""), (matchup7.home_team, matchup7.home_team), (matchup7.away_team, matchup7.away_team)]
    form.match8.choices = [("", ""), (matchup8.home_team, matchup8.home_team), (matchup8.away_team, matchup8.away_team)]
    form.east_pick1.choices = [("", ""), (seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.east_pick2.choices = [("", ""), (seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.east_pick3.choices = [("", ""), (seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.east_pick4.choices = [("", ""), (seed1_e.team, seed1_e.team), (seed2_e.team, seed2_e.team),
                          (seed3_e.team, seed3_e.team), (seed4_e.team, seed4_e.team)]
    form.west_pick1.choices = [("", ""), (seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]
    form.west_pick2.choices = [("", ""), (seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]
    form.west_pick3.choices = [("", ""), (seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]
    form.west_pick4.choices = [("", ""), (seed1_w.team, seed1_w.team), (seed2_w.team, seed2_w.team),
                          (seed3_w.team, seed3_w.team), (seed4_w.team, seed4_w.team)]

    if request.method == 'POST' and form.validate_on_submit():
        pir_picks = Round0(users=current_user.id, round=round_num, pick1=form.match1.data, games1=form.games1.data,
                                pick2=form.match2.data, games2=form.games2.data, pick3=form.match3.data,
                                games3=form.games3.data, pick4=form.match4.data, games4=form.games4.data,
                                pick5=form.match5.data, games5=form.games5.data, pick6=form.match6.data,
                                games6=form.games6.data, pick7=form.match7.data, games7=form.games7.data,
                                pick8=form.match8.data, games8=form.games8.data,
                                east_team1=form.east_pick1.data, east_team2=form.east_pick2.data,
                                east_team3=form.east_pick3.data, east_team4=form.east_pick4.data,
                                west_team1=form.west_pick1.data, west_team2=form.west_pick2.data,
                                west_team3=form.west_pick3.data, west_team4=form.west_pick4.data)
        db.session.add(pir_picks)
        db.session.commit()

        user.r0_picksin = 'True'
        db.session.commit()

        flash('Picks have been successfully entered for the Play in Round', 'success')
        return redirect(url_for('standings'))
    return render_template('playin.html', title='Play In Round', form=form, user=current_user)


@app.route("/picks/round1", methods=['GET', 'POST'])
@login_required
def round1():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    round_num = 1
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
    matchup3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
    matchup4 = Bracket.query.filter_by(round=round_num, game_id=4).first()
    matchup5 = Bracket.query.filter_by(round=round_num, game_id=5).first()
    matchup6 = Bracket.query.filter_by(round=round_num, game_id=6).first()
    matchup7 = Bracket.query.filter_by(round=round_num, game_id=7).first()
    matchup8 = Bracket.query.filter_by(round=round_num, game_id=8).first()

    form = PlayerPicks1()
    form.match1.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.match2.choices = [("", ""), (matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]
    form.match3.choices = [("", ""), (matchup3.home_team, matchup3.home_team), (matchup3.away_team, matchup3.away_team)]
    form.match4.choices = [("", ""), (matchup4.home_team, matchup4.home_team), (matchup4.away_team, matchup4.away_team)]
    form.match5.choices = [("", ""), (matchup5.home_team, matchup5.home_team), (matchup5.away_team, matchup5.away_team)]
    form.match6.choices = [("", ""), (matchup6.home_team, matchup6.home_team), (matchup6.away_team, matchup6.away_team)]
    form.match7.choices = [("", ""), (matchup7.home_team, matchup7.home_team), (matchup7.away_team, matchup7.away_team)]
    form.match8.choices = [("", ""), (matchup8.home_team, matchup8.home_team), (matchup8.away_team, matchup8.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        pir_picks = Round1(users=user.id, round=round_num,
                           pick1=form.match1.data, games1=form.games1.data,
                           pick2=form.match2.data, games2=form.games2.data,
                           pick3=form.match3.data, games3=form.games3.data,
                           pick4=form.match4.data, games4=form.games4.data,
                           pick5=form.match5.data, games5=form.games5.data,
                           pick6=form.match6.data, games6=form.games6.data,
                           pick7=form.match7.data, games7=form.games7.data,
                           pick8=form.match8.data, games8=form.games8.data)
        db.session.add(pir_picks)
        user.r1_picksin = 'True'
        db.session.commit()
        flash('Picks have been successfully entered for Round 1', 'success')
        return redirect(url_for('standings'))
    return render_template('round1.html', title='Round1', form=form, user=current_user)


@app.route("/picks/round2", methods=['GET', 'POST'])
@login_required
def round2():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    round_num = 2

    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()
    matchup3 = Bracket.query.filter_by(round=round_num, game_id=3).first()
    matchup4 = Bracket.query.filter_by(round=round_num, game_id=4).first()

    form = PlayerPicks2()
    form.match1.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.match2.choices = [("", ""), (matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]
    form.match3.choices = [("", ""), (matchup3.home_team, matchup3.home_team), (matchup3.away_team, matchup3.away_team)]
    form.match4.choices = [("", ""), (matchup4.home_team, matchup4.home_team), (matchup4.away_team, matchup4.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        pir_picks = Round2(users=user.id, round=round_num,
                           pick1=form.match1.data, games1=form.games1.data,
                           pick2=form.match2.data, games2=form.games2.data,
                           pick3=form.match3.data, games3=form.games3.data,
                           pick4=form.match4.data, games4=form.games4.data)

        db.session.add(pir_picks)
        user.r2_picksin = 'True'
        db.session.commit()
        flash('Picks have been successfully entered for Round 2', 'success')
        return redirect(url_for('standings'))
    return render_template('round2.html', title='Round2', form=form, user=current_user)


@app.route("/picks/round3", methods=['GET', 'POST'])
@login_required
def round3():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 3
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()
    matchup2 = Bracket.query.filter_by(round=round_num, game_id=2).first()

    form = PlayerPicks3()
    form.match1.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.match2.choices = [("", ""), (matchup2.home_team, matchup2.home_team), (matchup2.away_team, matchup2.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        pir_picks3 = Round3(users=user.id, round=round_num, pick1=form.match1.data, games1=form.games1.data,
                            pick2=form.match2.data, games2=form.games2.data)

        db.session.add(pir_picks3)
        user.r3_picksin = 'True'
        db.session.commit()
        flash('Picks have been successfully entered for Conference Finals', 'success')
        return redirect(url_for('standings'))
    return render_template('round3.html', title='Round3', form=form, user=current_user)


@app.route("/picks/round4", methods=['GET', 'POST'])
@login_required
def round4():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    round_num = 4
    matchup1 = Bracket.query.filter_by(round=round_num, game_id=1).first()

    form = PlayerPicks4()
    form.game1.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.game2.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.game3.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.game4.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.game5.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.game6.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]
    form.game7.choices = [("", ""), (matchup1.home_team, matchup1.home_team), (matchup1.away_team, matchup1.away_team)]

    if request.method == 'POST' and form.validate_on_submit():
        pir_picks = Round4(users=user.id, round=round_num,
                           game1=form.game1.data,
                           game2=form.game2.data,
                           game3=form.game3.data,
                           game4=form.game4.data,
                           game5=form.game5.data,
                           game6=form.game6.data,
                           game7=form.game7.data)

        db.session.add(pir_picks)
        user.r4_picksin = 'True'
        db.session.commit()
        flash('Picks have been successfully entered for Stanley Cup Finals', 'success')
        return redirect(url_for('standings'))
    return render_template('round4.html', title='Round4', form=form, user=current_user)


@app.route("/points")
def points():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None

    # update standings to include
    skaters = PlayerTotals.query.filter().order_by(PlayerTotals.points.desc())

    return render_template('points.html', user=user, skaters=skaters)