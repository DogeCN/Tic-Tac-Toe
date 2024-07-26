
ini = \
'''mode = 0
# 0: single player (first hand)
# 1: single player (last hand)
# 2: multiplayer
# 3: auto
'''

def get_mode():
    try:
        raw = open('mode.ini').readline()
        value = raw.split('=')[-1].split('#')[0].strip()
        mode = int(value)
    except:
        open('mode.ini', 'w').write(ini)
        mode = 0
    return mode
