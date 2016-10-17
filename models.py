"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

from random import randint
from datetime import date
from google.appengine.ext import ndb
from forms import (
    GameForm,
    UserActiveGamesForm,
    HistoryGameForm,
    UserRankingForm,
    HighScoreForm)


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    user = ndb.KeyProperty(required=True, kind='User')
    guesses = ndb.IntegerProperty(repeated=True)
    ship_location = ndb.IntegerProperty(required=True)
    attempts_allowed = ndb.IntegerProperty(required=True, default=5)
    attempts_remaining = ndb.IntegerProperty(required=True)
    game_over = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def new_game(cls, user, attempts):
        """Creates and returns a new game"""
        ship_location = randint(1, 25)

        game = Game(user=user,
                    ship_location=ship_location,
                    attempts_allowed=attempts,
                    attempts_remaining=attempts,
                    game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        row1 = (['O'] * 5)
        row2 = (['O'] * 5)
        row3 = (['O'] * 5)
        row4 = (['O'] * 5)
        row5 = (['O'] * 5)

        if len(self.guesses) > 0:
            for guesses in self.guesses:
                col = guesses % 5
                if guesses >= 1 and guesses <= 5:
                    row1[col-1] = 'X'
                if guesses >= 6 and guesses <= 10:
                    row2[col-1] = 'X'
                if guesses >= 11 and guesses <= 15:
                    row3[col-1] = 'X'
                if guesses >= 16 and guesses <= 20:
                    row4[col-1] = 'X'
                if guesses >= 21 and guesses <= 25:
                    row5[col-1] = 'X'

        if self.game_over is True:
            for guesses in self.guesses:
                if guesses == self.ship_location:
                    col = guesses % 5
                    if guesses >= 1 and guesses <= 5:
                        row1[col-1] = 'S'
                    if guesses >= 6 and guesses <= 10:
                        row2[col-1] = 'S'
                    if guesses >= 11 and guesses <= 15:
                        row3[col-1] = 'S'
                    if guesses >= 16 and guesses <= 20:
                        row4[col-1] = 'S'
                    if guesses >= 21 and guesses <= 25:
                        row5[col-1] = 'S'

        row1 = ' '.join(row1)
        row2 = ' '.join(row2)
        row3 = ' '.join(row3)
        row4 = ' '.join(row4)
        row5 = ' '.join(row5)

        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.guesses = self.guesses
        form.rowA = row1
        form.rowB = row2
        form.rowC = row3
        form.rowD = row4
        form.rowE = row5
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        return form

    def active_form(self, message):
        """Returns a GameForm representation of
        the Game for users active games"""
        row1 = (['O'] * 5)
        row2 = (['O'] * 5)
        row3 = (['O'] * 5)
        row4 = (['O'] * 5)
        row5 = (['O'] * 5)

        if len(self.guesses) > 0:
            for guesses in self.guesses:
                col = guesses % 5
                if guesses >= 1 and guesses <= 5:
                    row1[col-1] = 'X'
                if guesses >= 6 and guesses <= 10:
                    row2[col-1] = 'X'
                if guesses >= 11 and guesses <= 15:
                    row3[col-1] = 'X'
                if guesses >= 16 and guesses <= 20:
                    row4[col-1] = 'X'
                if guesses >= 21 and guesses <= 25:
                    row5[col-1] = 'X'

        if self.game_over is True:
            for guesses in self.guesses:
                if guesses == self.ship_location:
                    col = guesses % 5
                    if guesses >= 1 and guesses <= 5:
                        row1[col-1] = 'S'
                    if guesses >= 6 and guesses <= 10:
                        row2[col-1] = 'S'
                    if guesses >= 11 and guesses <= 15:
                        row3[col-1] = 'S'
                    if guesses >= 16 and guesses <= 20:
                        row4[col-1] = 'S'
                    if guesses >= 21 and guesses <= 25:
                        row5[col-1] = 'S'

        row1 = ' '.join(row1)
        row2 = ' '.join(row2)
        row3 = ' '.join(row3)
        row4 = ' '.join(row4)
        row5 = ' '.join(row5)

        form = UserActiveGamesForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.guesses = self.guesses
        form.rowA = row1
        form.rowB = row2
        form.rowC = row3
        form.rowD = row4
        form.rowE = row5
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        return form

    def history_form(self):
        """Returns a GameForm representation of
        the Game for users history of games"""
        row1 = (['O'] * 5)
        row2 = (['O'] * 5)
        row3 = (['O'] * 5)
        row4 = (['O'] * 5)
        row5 = (['O'] * 5)

        if len(self.guesses) > 0:
            for guesses in self.guesses:
                col = guesses % 5
                if guesses >= 1 and guesses <= 5:
                    row1[col-1] = 'X'
                if guesses >= 6 and guesses <= 10:
                    row2[col-1] = 'X'
                if guesses >= 11 and guesses <= 15:
                    row3[col-1] = 'X'
                if guesses >= 16 and guesses <= 20:
                    row4[col-1] = 'X'
                if guesses >= 21 and guesses <= 25:
                    row5[col-1] = 'X'

        if self.game_over is True:
            message = 'You Lost'
            for guesses in self.guesses:
                if guesses == self.ship_location:
                    message = 'You Won!'
                    col = guesses % 5
                    if guesses >= 1 and guesses <= 5:
                        row1[col-1] = 'S'
                    if guesses >= 6 and guesses <= 10:
                        row2[col-1] = 'S'
                    if guesses >= 11 and guesses <= 15:
                        row3[col-1] = 'S'
                    if guesses >= 16 and guesses <= 20:
                        row4[col-1] = 'S'
                    if guesses >= 21 and guesses <= 25:
                        row5[col-1] = 'S'

        if self.game_over is False:
            message = 'Game Not Finished!'

        row1 = ' '.join(row1)
        row2 = ' '.join(row2)
        row3 = ' '.join(row3)
        row4 = ' '.join(row4)
        row5 = ' '.join(row5)

        form = HistoryGameForm()
        form.guesses = self.guesses
        form.rowA = row1
        form.rowB = row2
        form.rowC = row3
        form.rowD = row4
        form.rowE = row5
        form.attempts_remaining = self.attempts_remaining
        form.attempts_allowed = self.attempts_allowed
        form.message = message
        form.game_over = self.game_over
        return form

    def user_score(self):
        '''Creates Score Model for user'''
        score = Score(user=self.user, date=date.today())
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    victories = ndb.FloatProperty(required=True, default=0.0)
    losses = ndb.FloatProperty(required=True, default=0.0)
    percentage = ndb.FloatProperty(required=True, default=0.0)

    def high_scores(self):
        return HighScoreForm(
            user_name=self.user.get().name,
            total_wins=self.victories
        )

    def user_rankings(self):
        return UserRankingForm(
            user_name=self.user.get().name,
            percentage_wins=self.percentage
        )
