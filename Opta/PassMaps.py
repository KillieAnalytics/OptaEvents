import pandas as pd

from mplsoccer import Pitch, FontManager
import matplotlib.pyplot as plt
from highlight_text import fig_text

SUCCESSFUL = "#a3f307"
UNSUCCESSFUL = "#FE53BB"

def create_pass_map(passes, player, team):

    passes = passes[['player', 'x', 'y', 'endX', 'endY', 'outcomeType.displayName']] 

    successful = passes.loc[passes['outcomeType.displayName']=='Successful']
    unsuccessful = passes.loc[passes['outcomeType.displayName']=='Unsuccessful']

    pitch = Pitch(pitch_type='opta', pitch_color='#212946', line_color='#c7d5cc', axis=False, label=False)

    fig, axs = pitch.grid(figheight=12,
                        title_height=0.0,
                        endnote_height=0.01, endnote_space=0.01,
                        axis=False)
    fig.set_facecolor('#212946')

    pitch.arrows(unsuccessful.x, unsuccessful.y,
                 unsuccessful.endX, unsuccessful.endY, width=2,
                 headwidth=5, headlength=5,
                 color='#FE53BB', ax=axs['pitch'], label='Unsuccessful')

    pitch.arrows(successful.x, successful.y,
                successful.endX, successful.endY, width=2, headwidth=5,
                headlength=5, color='#a3f307', ax=axs['pitch'], label='Successful')

    robotto_regular = FontManager()

    fig_text(
        x = 0.03, y = 0.92,
        s = player + " <successful> and <unsuccessful> passes vs " + team,
        highlight_textprops = [
            {"color": "#a3f307", "weight": "bold"},
            {"color": "#FE53BB", "weight": "bold"}
        ],
        color = "white",
        size = 25,
        va='center',
        vpad=30,
        annotationbbox_kw={"xycoords": "figure fraction"}
    )

    fn =  player + "-vs-" + team + ".png"
    plt.savefig(fn, bbox_inches='tight')