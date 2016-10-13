"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

from math import floor
from random import randint
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

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

        ship_location = randint(1, 26)

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
                if guesses >= 1 and guesses<=5:
                    row1[col-1] = 'X'
                if guesses >= 6 and guesses<=10:
                    row2[col-1] = 'X'
                if guesses >= 11 and guesses<=15:
                    row3[col-1] = 'X'
                if guesses >= 16 and guesses<=20:
                    row4[col-1] = 'X'
                if guesses >= 21 and guesses<=25:
                    row5[col-1] = 'X'

        row1 = ' '.join(row1)
        row2 =' '.join(row2)
        row3 =' '.join(row3)
        row4 =' '.join(row4)
        row5 =' '.join(row5)

        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.guesses = self.guesses
        form.rowOne = row1
        form.rowTwo = row2
        form.rowThree = row3
        form.rowFour = row4
        form.rowFive = row5
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        return form


    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)

class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    guesses = messages.StringField(3, repeated=True)
    rowOne = messages.StringField(4, required=True)
    rowTwo = messages.StringField(5, required=True)
    rowThree = messages.StringField(6, required=True)
    rowFour = messages.StringField(7, required=True)
    rowFive = messages.StringField(8, required=True)
    game_over = messages.BooleanField(9, required=True)
    message = messages.StringField(10, required=True)
    user_name = messages.StringField(11, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    attempts = messages.IntegerField(2, default=5)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.IntegerField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
