# Prerequisities
- [python3](https://docs.python.org/3/using/index.html)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

# Instructions for downloading
1. Clone the repo: `git clone https://github.com/nicholaswong112/gameoflife.git`
2. Run `virtualenv venv` then `source venv/bin/activate` to create and activate the virtual environment
3. Install necessary packages with `pip install -r requirements.txt`
4. Run `python3 main.py`

# TODO
* docstrings instead of comments
* GRID CLASS
- Display the grid lines
- Make the buttons more responsive (lags sometimes, and if you hold down they keep activating) -- have their own thread/handler?
- Add a speed slider --> should be changing argument to clock.tick()
- Be able to change the number of squares, resize the window
- There shouldn't be "walls" at the edge, theoretically, a glider would just glide away (easy fix, extend grid some small number of squares in all directions)
- Make UI more pretty