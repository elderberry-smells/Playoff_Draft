from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, IPAddress, NumberRange
from nhl.models import User, Bracket, Seeding
from nhl import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please try another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please try another one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.  You must register first.')


class MatchupForm(FlaskForm):
    # update nhl.models Bracket to fill in the "result" column with winner and "games" column with games
    round = IntegerField("Round", validators=[DataRequired()])
    game_id = IntegerField("Game Id")
    home_team = db.Column(db.String, nullable=False)
    away_team = db.Column(db.String, nullable=False)
    submit = SubmitField('Update Matchup')


class ResultForm0(FlaskForm):
    # update nhl.models Bracket to fill in the "result" column with winner and "games" column with games
    winner1 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games1 = IntegerField('Number of Games', validators=[DataRequired()])
    winner2 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games2 = IntegerField('Number of Games', validators=[DataRequired()])
    winner3 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games3 = IntegerField('Number of Games', validators=[DataRequired()])
    winner4 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games4 = IntegerField('Number of Games', validators=[DataRequired()])
    winner5 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games5 = IntegerField('Number of Games', validators=[DataRequired()])
    winner6 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games6 = IntegerField('Number of Games', validators=[DataRequired()])
    winner7 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games7 = IntegerField('Number of Games', validators=[DataRequired()])
    winner8 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games8 = IntegerField('Number of Games', validators=[DataRequired()])
    east1 = SelectField('1st East', validators=[DataRequired()], choices=[])
    east2 = SelectField('2nd East', validators=[DataRequired()], choices=[])
    east3 = SelectField('3rd East', validators=[DataRequired()], choices=[])
    east4 = SelectField('4th East', validators=[DataRequired()], choices=[])
    west1 = SelectField('1st West', validators=[DataRequired()], choices=[])
    west2 = SelectField('2nd West', validators=[DataRequired()], choices=[])
    west3 = SelectField('3rd West', validators=[DataRequired()], choices=[])
    west4 = SelectField('4th West', validators=[DataRequired()], choices=[])
    submit = SubmitField('Enter Result for Round 0')


class ResultForm1(FlaskForm):
    # update nhl.models Bracket to fill in the "result" column with winner and "games" column with games
    winner1 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games1 = IntegerField('Number of Games', validators=[DataRequired()])
    winner2 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games2 = IntegerField('Number of Games', validators=[DataRequired()])
    winner3 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games3 = IntegerField('Number of Games', validators=[DataRequired()])
    winner4 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games4 = IntegerField('Number of Games', validators=[DataRequired()])
    winner5 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games5 = IntegerField('Number of Games', validators=[DataRequired()])
    winner6 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games6 = IntegerField('Number of Games', validators=[DataRequired()])
    winner7 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games7 = IntegerField('Number of Games', validators=[DataRequired()])
    winner8 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games8 = IntegerField('Number of Games', validators=[DataRequired()])
    submit = SubmitField('Enter Result for Round 1')


class ResultForm2(FlaskForm):
    # update nhl.models Bracket to fill in the "result" column with winner and "games" column with games
    winner1 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games1 = IntegerField('Number of Games', validators=[DataRequired()])
    winner2 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games2 = IntegerField('Number of Games', validators=[DataRequired()])
    winner3 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games3 = IntegerField('Number of Games', validators=[DataRequired()])
    winner4 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games4 = IntegerField('Number of Games', validators=[DataRequired()])
    submit = SubmitField('Enter Result for Round 2')


class ResultForm3(FlaskForm):
    # update nhl.models Bracket to fill in the "result" column with winner and "games" column with games
    winner1 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games1 = IntegerField('Number of Games', validators=[DataRequired()])
    winner2 = SelectField('Winning team', choices=[], validators=[DataRequired()])
    games2 = IntegerField('Number of Games', validators=[DataRequired()])
    submit = SubmitField('Enter Result for Round 3')


class ResultForm4(FlaskForm):
    # update nhl.models Bracket to fill in the "result" column with winner and "games" column with games
    game_number = SelectField('Game Number', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                        ('5', '5'), ('6', '6'), ('7', '7')])
    winner = SelectField('Winning team', choices=[])
    submit = SubmitField('Enter Result for Stanley Cup Final Game')


class UpdateSeeding(FlaskForm):
    round = 1
    seed = IntegerField("Seeding", validators=[DataRequired()])
    conference_e = 'east'
    team_e = StringField('Team Name', validators=[DataRequired()], choices=[])
    conference_w = 'west'
    team_w = StringField('Team Name', validators=[DataRequired()], choices=[])
    submit = SubmitField('Update Seeding')


class PlayerPicks0(FlaskForm):
    # Eastern Conference Matchups round 1
    match1 = SelectField('Pick Winner of East Game 1 (seed 8 vs seed 9)', choices=[], validators=[DataRequired()])
    games1 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    match2 = SelectField('Pick Winner of East Game 2 (seed 6 vs seed 11)', choices=[], validators=[DataRequired()])
    games2 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    match3 = SelectField('Pick Winner of East Game 3 (seed 5 vs seed 12)', choices=[], validators=[DataRequired()])
    games3 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    match4 = SelectField('Pick Winner of East Game 4 (seed 7 vs seed 10)', choices=[], validators=[DataRequired()])
    games4 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])

    # Western Conference Matchups round 1
    match5 = SelectField('Pick Winner of West Game 1 (seed 8 vs seed 9)', choices=[], validators=[DataRequired()])
    games5 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    match6 = SelectField('Pick Winner of West Game 2 (seed 6 vs seed 11)', choices=[], validators=[DataRequired()])
    games6 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    match7 = SelectField('Pick Winner of West Game 3 (seed 5 vs seed 12)', choices=[], validators=[DataRequired()])
    games7 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    match8 = SelectField('Pick Winner of West Game 4 (seed 7 vs seed 10)', choices=[], validators=[DataRequired()])
    games8 = SelectField('How Many Games?', choices=[('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    east_pick1 = SelectField('Pick Top Eastern Round Robin Team', choices=[], validators=[DataRequired()])
    east_pick2 = SelectField('Pick Second Eastern Round Robin Team', choices=[], validators=[DataRequired()])
    east_pick3 = SelectField('Pick Third Eastern Round Robin Team', choices=[], validators=[DataRequired()])
    east_pick4 = SelectField('Pick Last Eastern Round Robin Team', choices=[], validators=[DataRequired()])
    west_pick1 = SelectField('Pick Top Western Round Robin Team', choices=[], validators=[DataRequired()])
    west_pick2 = SelectField('Pick Second Western Round Robin Team', choices=[], validators=[DataRequired()])
    west_pick3 = SelectField('Pick Third Western Round Robin Team', choices=[], validators=[DataRequired()])
    west_pick4 = SelectField('Pick Last Western Round Robin Team', choices=[], validators=[DataRequired()])
    submit = SubmitField('Lock in Play In Round Picks')


class PlayerPicks1(FlaskForm):
    # Eastern Conference Matchups round 1
    match1 = SelectField('Pick Winner of East Game 1 (seed 1 vs seed 8)', choices=[], validators=[DataRequired()])
    games1 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match2 = SelectField('Pick Winner of East Game 2 (seed 2 vs seed 7)', choices=[], validators=[DataRequired()])
    games2 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match3 = SelectField('Pick Winner of East Game 3 (seed 3 vs seed 6)', choices=[], validators=[DataRequired()])
    games3 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match4 = SelectField('Pick Winner of East Game 4 (seed 4 vs seed 5)', choices=[], validators=[DataRequired()])
    games4 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])

    # Western Conference Matchups round 1
    match5 = SelectField('Pick Winner of West Game 1 (seed 1 vs seed 8)', choices=[], validators=[DataRequired()])
    games5 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match6 = SelectField('Pick Winner of West Game 2 (seed 2 vs seed 7)', choices=[], validators=[DataRequired()])
    games6 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match7 = SelectField('Pick Winner of West Game 3 (seed 3 vs seed 6)', choices=[], validators=[DataRequired()])
    games7 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match8 = SelectField('Pick Winner of West Game 4 (seed 4 vs seed 5)', choices=[], validators=[DataRequired()])
    games8 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    submit = SubmitField('Lock in Round 1 Picks')


class PlayerPicks2(FlaskForm):
    # Eastern Conference Matchups round 2
    match1 = SelectField('Pick Winner of East Game 1 (seed 1 vs seed 4)', choices=[], validators=[DataRequired()])
    games1 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match2 = SelectField('Pick Winner of East Game 2 (seed 2 vs seed 3)', choices=[], validators=[DataRequired()])
    games2 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])

    # Western Conference Matchups round 2
    match3 = SelectField('Pick Winner of West Game 1 (seed 1 vs seed 4)', choices=[], validators=[DataRequired()])
    games3 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match4 = SelectField('Pick Winner of West Game 2 (seed 2 vs seed 3)', choices=[], validators=[DataRequired()])
    games4 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    submit = SubmitField('Lock in Round 2 Picks')


class PlayerPicks3(FlaskForm):
    # Eastern Conference Matchups round 3
    match1 = SelectField('Pick Winner of East Conference', choices=[], validators=[DataRequired()])
    games1 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    match2 = SelectField('Pick Winner of West Conference', choices=[], validators=[DataRequired()])
    games2 = SelectField('How Many Games?', choices=[('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                         validators=[DataRequired()])
    submit = SubmitField('Lock in Conference Finals Picks')


class PlayerPicks4(FlaskForm):
    # Eastern Conference Matchups round 3
    game1 = SelectField('Pick Winner of Game 1', choices=[], validators=[DataRequired()])
    game2 = SelectField('Pick Winner of Game 2', choices=[], validators=[DataRequired()])
    game3 = SelectField('Pick Winner of Game 3', choices=[], validators=[DataRequired()])
    game4 = SelectField('Pick Winner of Game 4', choices=[], validators=[DataRequired()])
    game5 = SelectField('Pick Winner of Game 5', choices=[], validators=[DataRequired()])
    game6 = SelectField('Pick Winner of Game 6', choices=[], validators=[DataRequired()])
    game7 = SelectField('Pick Winner of Game 7', choices=[], validators=[DataRequired()])
    submit = SubmitField('Lock in Stanley Cup Game Winners')


class SkaterTotalForm(FlaskForm):
    evan1 = IntegerField('Pastrnak')
    evan2 = IntegerField('Perron')
    gabe1 = IntegerField('Marchand')
    gabe2 = IntegerField('Landeskog')
    dallas1 = IntegerField('Kucherov')
    dallas2 = IntegerField('Stone')
    mack1 = IntegerField('McDavid')
    mack2 = IntegerField('Ovechkin')
    brian1 = IntegerField('MacKinnon')
    brian2 = IntegerField('Point')
    mikeb1 = IntegerField('Draisaitl')
    mikeb2 = IntegerField('Matthews')
    mikez1 = IntegerField('M.Rantanen')
    mikez2 = IntegerField('Aho')
    mark1 = IntegerField('OReilly')
    mark2 = IntegerField('Bergeron')
    submit = SubmitField('Update Player totals')
