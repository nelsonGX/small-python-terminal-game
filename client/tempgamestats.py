temp_stats_g1 = False
temp_stats_g2 = False
temp_stats_g3 = False
temp_stats_g4 = False   
temp_stats_g5 = False
temp_stats_g6 = False
temp_stats_g7 = False
temp_stats_g8 = False
temp_stats_g9 = False
temp_stats_g10 = False
temp_stats_g11 = False

temp_stats_boss_1 = False
temp_stats_boss_2 = False
temp_stats_boss_3 = False

async def set_stats(game):
    global temp_stats_g1
    global temp_stats_g2
    global temp_stats_g3
    global temp_stats_g4
    global temp_stats_g5
    global temp_stats_g6
    global temp_stats_g7
    global temp_stats_g8
    global temp_stats_g9
    global temp_stats_g10
    global temp_stats_g11
    if game == 1:
        temp_stats_g1 = True
    elif game == 2:
        temp_stats_g2 = True
    elif game == 3:
        temp_stats_g3 = True
    elif game == 4:
        temp_stats_g4 = True
    elif game == 5:
        temp_stats_g5 = True
    elif game == 6:
        temp_stats_g6 = True
    elif game == 7:
        temp_stats_g7 = True
    elif game == 8:
        temp_stats_g8 = True
    elif game == 9:
        temp_stats_g9 = True
    elif game == 10:
        temp_stats_g10 = True
    elif game == 11:
        temp_stats_g11 = True

async def get_stats(game):
    global temp_stats_g1
    global temp_stats_g2
    global temp_stats_g3
    global temp_stats_g4
    global temp_stats_g5
    global temp_stats_g6
    global temp_stats_g7
    global temp_stats_g8
    global temp_stats_g9
    global temp_stats_g10
    global temp_stats_g11
    if game == 1:
        return temp_stats_g1
    elif game == 2:
        return temp_stats_g2
    elif game == 3:
        return temp_stats_g3
    elif game == 4:
        return temp_stats_g4
    elif game == 5:
        return True
    elif game == 6:
        return temp_stats_g6
    elif game == 7:
        return temp_stats_g7
    elif game == 8:
        return temp_stats_g8
    elif game == 9:
        return temp_stats_g9
    elif game == 10:
        return temp_stats_g10
    elif game == 11:
        return temp_stats_g11
    
async def set_boss_stats(boss):
    global temp_stats_boss_1
    global temp_stats_boss_2
    global temp_stats_boss_3
    if boss == 1:
        temp_stats_boss_1 = True
    elif boss == 2:
        temp_stats_boss_2 = True
    elif boss == 3:
        temp_stats_boss_3 = True

async def get_boss_stats(boss):
    global temp_stats_boss_1
    global temp_stats_boss_2
    global temp_stats_boss_3
    if boss == 1:
        return temp_stats_boss_1
    elif boss == 2:
        return temp_stats_boss_2
    elif boss == 3:
        return temp_stats_boss_3