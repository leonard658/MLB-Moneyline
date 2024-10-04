# MLB Game predictor:
## Currently a work in progress and is extremely messy.
### Basic rundown of things inside:
functions to compile data held in - getLineup.py, getOddsData.py, getRecentStats.py, buildData.py...
csv files hold the compiled data - main training data is held in CombinedWithWin files.
Jupyter Notebooks hold the actual model development and analysis.
glStuff folder just holds previously data I was experiment with.
I've been getting daily bets by running getOptimalBets.py file and changing the date at the bottom.
    This goes through all the games on the given date, compiles the needed stats and produces a prediction for every game.

### Upcoming plans:
Currently building out frontend.
Continued development on the actual model.
Eventually deploy a website when next season starts.
