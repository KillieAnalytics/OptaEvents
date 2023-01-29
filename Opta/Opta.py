import json
import sys
sys.path.append('../')

import pandas as pd
import PassMaps as pm
import ShotMap as sm
import numpy as np

def open_file(file):
    with open(file) as match:
        return json.load(match)

def clean_events(df):
    df['minute'] = df['minute'].astype('int8')
    df['expandedMinute'] = df['expandedMinute'].astype('int8')
    df['eventId'] = df['eventId'].astype('int16')
    df['teamId'] = df['teamId'].astype('int16')
    df['second'] = df['second'].astype('float16')
    df['isGoal'] = df['isGoal'].map({np.NaN:False, True:True})
    df['isShot'] = df['isShot'].map({np.NaN:False, True:True})
    df['period.value'] = df['period.value'].astype('int8')
    df['period.displayName'] = df['period.displayName'].astype('category')
    df['type.value'] = df['type.value'].astype('int16')
    df['type.displayName'] = df['type.displayName'].astype('category')
    df['outcomeType.value'] = df['outcomeType.value'].astype('int8')
    df['outcomeType.displayName'] = df['outcomeType.displayName'].astype('category')

    df = drop_columns(df)
    df = rename_columns(df)

    return df

def rename_columns(df):
    df.rename(columns={'type.displayName': 'type_displayName'}, inplace=True)
    return df

def drop_columns(df):
    return df.drop(['id'], axis=1)

def get_events(file):
    return pd.json_normalize(file['events'])

def get_teams(file):
    match = pd.DataFrame(columns=["type", "teamId", "team", "team_against"])
    home = pd.DataFrame(file['home'].items())
    away = pd.DataFrame(file['away'].items())
    
    match.loc[0] = ["home", home.loc[home[0] == 'teamId'][1].item(), home.loc[home[0] == 'name'][1].item(), away.loc[away[0] == 'name'][1].item()]
    match.loc[1] = ["away", away.loc[away[0] == 'teamId'][1].item(), away.loc[away[0] == 'name'][1].item(), home.loc[home[0] == 'name'][1].item()]
    return match

def get_players(file):
    return pd.DataFrame(file['playerIdNameDictionary'].items(), columns=['playerId', 'player'])

def get_all_passes(file):
    events = get_events(file)

    events = clean_events(events)

    passes = events[events.type_displayName == 'Pass']

    return passes

def get_all_shots(file_name):
    file_opened = open_file(file_name)

    players = get_players(file_opened)
    events = get_events(file_opened)
    teams = get_teams(file_opened)

    events = clean_events(events)

    shots = events[events.isShot == True]

    players['playerId'] = players['playerId'].astype(float)
    shots = shots.merge(players, on='playerId')
    shots = shots.merge(teams, on='teamId')

    return shots

def get_passes(file_name):
    file_opened = open_file(file_name)
    passes = get_all_passes(file_opened)
    players = get_players(file_opened)
    players['playerId'] = players['playerId'].astype(float)
    passes = passes.merge(players, on='playerId')
    return passes

def get_corners(file_name):
    file_opened = open_file(file_name)
    passes = get_all_passes(file_opened)
    events  =  get_events(file_opened)
    players = get_players(file_opened)
    players['playerId'] = players['playerId'].astype(float)
    passes['corner'] = pd.json_normalize(events['qualifiers']).apply(lambda row: row.astype(str).str.contains('CornerTaken').any(), axis=1)
    passes = passes.merge(players, on='playerId')
    corners = passes.loc[passes['corner']==True]
    return corners

def get_open_play_passes(file_name):
    file_opened = open_file(file_name)
    passes = get_all_passes(file_opened)
    events  =  get_events(file_opened)
    players = get_players(file_opened)
    players['playerId'] = players['playerId'].astype(float)
    passes['corner'] = pd.json_normalize(events['qualifiers']).apply(lambda row: ~row.astype(str).str.contains('CornerTaken').any(), axis=1)
    passes = passes.merge(players, on='playerId')
    corners = passes.loc[passes['corner']==True]
    return corners

def create_pass_map(df, player, team_against):
    pm.create_pass_map(df, player, team_against)

def create_shot_map(df, team):
    sm.create_shot_map(df.loc[df['isShot']==True], team)

def test_for_passes():
    file_name = '../matches/ManCityManUnited.json'
    player = "Bruno Fernandes"
    passes = get_passes(file_name)
    create_pass_map(passes[passes.player == player], player, "Man City")

def test_for_shots():
    file_name = '../matches/ManCityManUnited.json'
    team = "Man Utd"
    shots = get_all_shots(file_name)
    create_shot_map(shots[shots.team == team], team)

test_for_shots()