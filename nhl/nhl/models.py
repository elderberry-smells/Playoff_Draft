from datetime import datetime
import secrets
from nhl import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    r0_picksin = db.Column(db.String, default='False')
    r1_picksin = db.Column(db.String, default='False')
    r2_picksin = db.Column(db.String, default='False')
    r3_picksin = db.Column(db.String, default='False')
    r4_picksin = db.Column(db.String, default='False')
    totals = db.relationship('Tally', backref='points', lazy=True)
    ro_user = db.relationship('Round0', backref='author', lazy=True)
    r1_user = db.relationship('Round1', backref='author', lazy=True)
    r2_user = db.relationship('Round2', backref='author', lazy=True)
    r3_user = db.relationship('Round3', backref='author', lazy=True)
    r4_user = db.relationship('Round4', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}"


class Tally(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    round0 = db.Column(db.Integer, default=0)
    round1 = db.Column(db.Integer, default=0)
    round2 = db.Column(db.Integer, default=0)
    round3 = db.Column(db.Integer, default=0)
    round4 = db.Column(db.Integer, default=0)
    player_totals = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"{self.user}, {self.round0}, {self.round1}, {self.round2}, {self.round3}, " \
               f"{self.round4}, {self.player_totals}, {self.total_points}"


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    logo = db.Column(db.String, nullable=False)
    conference = db.Column(db.String, nullable=False)
    seed = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Team('{self.name}', '{self.logo}')"


class Bracket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, nullable=False)
    home_team = db.Column(db.String(20))
    away_team = db.Column(db.String(20))
    round = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(20))
    games = db.Column(db.Integer)


class RoundRobinResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    east1 = db.Column(db.String(20))
    east2 = db.Column(db.String(20))
    east3 = db.Column(db.String(20))
    east4 = db.Column(db.String(20))
    west1 = db.Column(db.String(20))
    west2 = db.Column(db.String(20))
    west3 = db.Column(db.String(20))
    west4 = db.Column(db.String(20))


class SCF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner1 = db.Column(db.String(20), nullable=False)
    winner2 = db.Column(db.String(20), nullable=False)
    winner3 = db.Column(db.String(20), nullable=False)
    winner4 = db.Column(db.String(20), nullable=False)
    winner5 = db.Column(db.String(20), nullable=False)
    winner6 = db.Column(db.String(20), nullable=False)
    winner7 = db.Column(db.String(20), nullable=False)


class Seeding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference = db.Column(db.String, nullable=False)
    seed = db.Column(db.Integer, nullable=False)
    team = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        print(f"'{self.team}, '{self.seed}'")

class Round0(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, default=10)
    users = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pick1 = db.Column(db.String, nullable=False)
    games1 = db.Column(db.Integer, nullable=False)
    pick2 = db.Column(db.String, nullable=False)
    games2 = db.Column(db.Integer, nullable=False)
    pick3 = db.Column(db.String, nullable=False)
    games3 = db.Column(db.Integer, nullable=False)
    pick4 = db.Column(db.String, nullable=False)
    games4 = db.Column(db.Integer, nullable=False)
    pick5 = db.Column(db.String, nullable=False)
    games5 = db.Column(db.Integer, nullable=False)
    pick6 = db.Column(db.String, nullable=False)
    games6 = db.Column(db.Integer, nullable=False)
    pick7 = db.Column(db.String, nullable=False)
    games7 = db.Column(db.Integer, nullable=False)
    pick8 = db.Column(db.String, nullable=False)
    games8 = db.Column(db.Integer, nullable=False)
    east_team1 = db.Column(db.String, nullable=False)
    east_team2 = db.Column(db.String, nullable=False)
    east_team3 = db.Column(db.String, nullable=False)
    east_team4 = db.Column(db.String, nullable=False)
    west_team1 = db.Column(db.String, nullable=False)
    west_team2 = db.Column(db.String, nullable=False)
    west_team3 = db.Column(db.String, nullable=False)
    west_team4 = db.Column(db.String, nullable=False)


class Round1(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, default=1)
    users = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pick1 = db.Column(db.String, nullable=False)
    games1 = db.Column(db.Integer, nullable=False)
    pick2 = db.Column(db.String, nullable=False)
    games2 = db.Column(db.Integer, nullable=False)
    pick3 = db.Column(db.String, nullable=False)
    games3 = db.Column(db.Integer, nullable=False)
    pick4 = db.Column(db.String, nullable=False)
    games4 = db.Column(db.Integer, nullable=False)
    pick5 = db.Column(db.String, nullable=False)
    games5 = db.Column(db.Integer, nullable=False)
    pick6 = db.Column(db.String, nullable=False)
    games6 = db.Column(db.Integer, nullable=False)
    pick7 = db.Column(db.String, nullable=False)
    games7 = db.Column(db.Integer, nullable=False)
    pick8 = db.Column(db.String, nullable=False)
    games8 = db.Column(db.Integer, nullable=False)


class Round2(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, default=2)
    users = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pick1 = db.Column(db.String, nullable=False)
    games1 = db.Column(db.Integer, nullable=False)
    pick2 = db.Column(db.String, nullable=False)
    games2 = db.Column(db.Integer, nullable=False)
    pick3 = db.Column(db.String, nullable=False)
    games3 = db.Column(db.Integer, nullable=False)
    pick4 = db.Column(db.String, nullable=False)
    games4 = db.Column(db.Integer, nullable=False)


class Round3(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, default=3)
    users = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pick1 = db.Column(db.String, nullable=False)
    games1 = db.Column(db.Integer, nullable=False)
    pick2 = db.Column(db.String, nullable=False)
    games2 = db.Column(db.Integer, nullable=False)


class Round4(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, default=4)
    users = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game1 = db.Column(db.String, nullable=False)
    game2 = db.Column(db.String, nullable=False)
    game3 = db.Column(db.String, nullable=False)
    game4 = db.Column(db.String, nullable=False)
    game5 = db.Column(db.String, nullable=False)
    game6 = db.Column(db.String, nullable=False)
    game7 = db.Column(db.String, nullable=False)


class PlayerTotals(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, default=0)


class PlayoffStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round0 = db.Column(db.String, default='False')
    roundrobin = db.Column(db.String, default='False')
    round1 = db.Column(db.String, default='False')
    round2 = db.Column(db.String, default='False')
    round3 = db.Column(db.String, default='False')
    round4 = db.Column(db.String, default='False')