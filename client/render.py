import sys

a = """
+-- 你好，冒險者 nelsonGX ----- 你在 主大廳 ------ 血量: 69/100 [|||||||    ] 金幣: 69 --+
|                                                                                     |
|                                                                                     |
|                    .    _    +     .  ______   .          .                         |
|                (      /|\      .    |      \      .   +                             |
|                    . |||||     _    | |   | | ||         .                          |
|               .      |||||    | |  _| | | | |_||    .                               |
|                  /\  ||||| .  | | |   | |      |       .                            |
|               __||||_|||||____| |_|_____________\__________                         |
|               . |||| |||||  /\   _____      _____  .   .                            |
|                 |||| ||||| ||||   .   .  .         ________                         |
|                . \|`-'|||| ||||    __________       .    .                          |
|                   \__ |||| ||||      .          .     .                             |
|                __    ||||`-'|||  .       .    __________                            |
|               .    . |||| ___/  ___________             .                           |
|                  . _ ||||| . _               .   _________                          |
|               _   ___|||||__  _ \\--//     .          _                              |
|                    _ `---'    .)=\oo|=(.   _   .   .    .                           |
|                _  ^      .  -    . \.|                                              |
|                                                                                     |
|                                                                                     |
|                                         O                                           |
|                                       --||--                                        |
|                                         /\                                          |
|                                         你                                          |
|                                                                                     |
|                                                                                     |
|                                                                                     |
+-------------------------------------------------------------按下 [e] 開啟背包--------+
"""

async def render():
    sys.stdout.write('\033[H')
    sys.stdout.write(a)
    sys.stdout.flush()
