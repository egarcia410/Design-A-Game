from protorpc import messages


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    guesses = messages.IntegerField(3, repeated=True)
    rowA = messages.StringField(4, required=True)
    rowB = messages.StringField(5, required=True)
    rowC = messages.StringField(6, required=True)
    rowD = messages.StringField(7, required=True)
    rowE = messages.StringField(8, required=True)
    game_over = messages.BooleanField(9, required=True)
    message = messages.StringField(10, required=True)
    user_name = messages.StringField(11, required=True)


class UserGameForm(messages.Message):
    """Input Field for retrieving user's Game History and Active Games"""
    user_name = messages.StringField(1, required=True)


class UserActiveGamesForm(messages.Message):
    """Used to return users game that are active"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    guesses = messages.IntegerField(3, repeated=True)
    rowA = messages.StringField(4, required=True)
    rowB = messages.StringField(5, required=True)
    rowC = messages.StringField(6, required=True)
    rowD = messages.StringField(7, required=True)
    rowE = messages.StringField(8, required=True)
    game_over = messages.BooleanField(9, required=True)
    message = messages.StringField(10, required=True)
    user_name = messages.StringField(11, required=True)


class UserActiveGamesForms(messages.Message):
    """Used to return users game that are active"""
    items = messages.MessageField(UserActiveGamesForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Input Field, Used to create a new game request"""
    user_name = messages.StringField(1, required=True)
    attempts = messages.IntegerField(2, default=5)


class MakeMoveForm(messages.Message):
    """Input Field, Used to make a move in an existing game"""
    guess = messages.IntegerField(1, required=True)


class HighScoreForm(messages.Message):
    """Return Users With The Most Wins"""
    user_name = messages.StringField(1, required=True)
    total_wins = messages.FloatField(2, required=True)


class HighScoreForms(messages.Message):
    """Return Users With The Most Wins"""
    items = messages.MessageField(HighScoreForm, 1, repeated=True)


class UserRankingForm(messages.Message):
    """Returns All Users Percentage of Wins"""
    user_name = messages.StringField(1, required=True)
    percentage_wins = messages.FloatField(2, required=True)


class UserRankingForms(messages.Message):
    """Returns All Users Percentage of Wins"""
    items = messages.MessageField(UserRankingForm, 1, repeated=True)


class HistoryGameForm(messages.Message):
    """Return Users Game History"""
    attempts_remaining = messages.IntegerField(1, required=True)
    attempts_allowed = messages.IntegerField(2, required=True)
    message = messages.StringField(3, required=True)
    guesses = messages.IntegerField(4, repeated=True)
    rowA = messages.StringField(5, required=True)
    rowB = messages.StringField(6, required=True)
    rowC = messages.StringField(7, required=True)
    rowD = messages.StringField(8, required=True)
    rowE = messages.StringField(9, required=True)
    game_over = messages.BooleanField(10, required=True)


class HistoryGameForms(messages.Message):
    """Return Users Game History"""
    items = messages.MessageField(HistoryGameForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
