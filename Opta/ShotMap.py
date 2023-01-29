import pandas as pd
import numpy as np

from mplsoccer import Pitch
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

SUCCESSFUL = "#a3f307"
UNSUCCESSFUL = "#FE53BB"

def create_shot_map(shots, team):

    shots['goalMouthY'] = shots['goalMouthY'].div(9.6).round(2)
    shots['goalMouthY'] = shots['goalMouthY'].mul(9).round(2)
    shots['goalMouthZ'] = shots['goalMouthZ'].div(39.95).round(2)
    shots['goalMouthZ'] = shots['goalMouthZ'].mul(3).round(2)

    fig, ax = plt.subplots(nrows=2, ncols=1)       
    fig.set_facecolor('#212946')
    ax[0].set_facecolor('#212946')
    ax[0].get_xaxis().set_visible(False)
    ax[0].get_yaxis().set_visible(False)
    ax[0].axis('off')


    pitch = Pitch(pitch_type='opta', pitch_color='#212946', line_color='#c7d5cc', axis=False, label=False)

    pitch.scatter(shots['x'].loc[shots['isGoal'] == True], shots['y'].loc[shots['isGoal'] == True], color=SUCCESSFUL, ax=ax[1], zorder=3)
    pitch.scatter(shots['x'].loc[shots['isGoal'] == False], shots['y'].loc[shots['isGoal'] == False], color=UNSUCCESSFUL, ax=ax[1], zorder=1)

    pitch.draw(ax=ax[1])

    ax[0].set_xlim(35,58)
    ax[0].set_ylim(0,10)
    line = mlines.Line2D([42.37, 42.37], [0, 2.99], color='#c7d5cc')
    ax[0].add_line(line)
    line = mlines.Line2D([51.38, 51.38], [0, 2.99], color='#c7d5cc')
    ax[0].add_line(line)
    line = mlines.Line2D([42.37, 51.38], [2.99, 2.99], color='#c7d5cc')
    ax[0].add_line(line)
    line = mlines.Line2D([35, 58], [0, 0], color='#c7d5cc')
    ax[0].add_line(line)
    ax[0].scatter(shots[['goalMouthY']].loc[shots['isGoal']==True], shots[['goalMouthZ']].loc[shots['isGoal']==True], color=SUCCESSFUL, zorder=3, cmap='#212946')
    ax[0].scatter(shots[['goalMouthY']].loc[shots['isGoal']==False], shots[['goalMouthZ']].loc[shots['isGoal']==False], color=UNSUCCESSFUL, zorder=1, cmap='#212946')

    ax[0] = ax[0].invert_xaxis()


    title = team + " Shot Map"
    fig.suptitle(title, fontsize=15, color='#c7d5cc')
    fn =  team + "-Shots" ".png"
    plt.savefig(fn, bbox_inches='tight')