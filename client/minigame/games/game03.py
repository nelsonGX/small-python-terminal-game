import random
import time

from client.minigame.games.game01 import pause
from server import Server


def AppearCount(rollRoll):
  AppearTime = {}
  for i in range(1, 7):

    AppearTime[f"AppearTime{i}"] = int(rollRoll.count(i))  #字典
  return AppearTime



#生成點數!!!!!!!!!!!!!!!!!!!!
def GOdice():
  point = []
  for i in range(4):
    dice_roll = random.randint(1, 6)
    point.append(dice_roll)
  return point

#從投擲到結算數字
def countPoint():
  fpoint = 0
  rollRoll = GOdice()
  rollRoll.sort()
  print(f'{rollRoll}')#印出哪四個點數
  AppearTime = AppearCount(rollRoll)
  again_needed = True

  while again_needed:  #重骰
    if AppearTime["AppearTime1"] < 2 and AppearTime[
        "AppearTime2"] < 2 and AppearTime["AppearTime3"] < 2 and AppearTime[
            "AppearTime4"] < 2 and AppearTime[
                "AppearTime5"] < 2 and AppearTime["AppearTime6"] < 2:
      rollRoll = GOdice()
      rollRoll.sort()
      print(f'{rollRoll}')
      AppearTime = AppearCount(rollRoll)

    elif AppearTime["AppearTime1"] == 3 or AppearTime[
        "AppearTime2"] == 3 or AppearTime["AppearTime3"] == 3 or AppearTime[
            "AppearTime4"] == 3 or AppearTime[
                "AppearTime5"] == 3 or AppearTime["AppearTime6"] == 3:
      rollRoll = GOdice()
      rollRoll.sort()
      print(f'{rollRoll}')
      AppearTime = AppearCount(rollRoll)
    else:
      again_needed = False

  if AppearTime["AppearTime1"] == 2:  #判斷分數#1122and1123
    for k in range(2, 7):
      if AppearTime[f"AppearTime{k}"] > 0:
        fpoint += AppearTime[f"AppearTime{k}"] * k
    return fpoint
  if AppearTime["AppearTime2"] == 2:  #2233
    if AppearTime["AppearTime3"] == 2:
      fpoint = 6
      return fpoint
    if AppearTime["AppearTime4"] == 2:
      fpoint = 8
      return fpoint
    if AppearTime["AppearTime5"] == 2:
      fpoint = 10
      return fpoint
    if AppearTime["AppearTime6"] == 2:
      fpoint = 12
      return fpoint
    for k in range(1, 7):
      if AppearTime[f"AppearTime{k}"] == 1:  #2231
        fpoint += AppearTime[f"AppearTime{k}"] * k
    return fpoint
  if AppearTime["AppearTime3"] == 2:
    if AppearTime["AppearTime4"] == 2:
      fpoint = 8
      return fpoint
    if AppearTime["AppearTime5"] == 2:
      fpoint = 10
      return fpoint
    if AppearTime["AppearTime6"] == 2:
      fpoint = 12
      return fpoint
    for k in range(1, 7):
      if AppearTime[f"AppearTime{k}"] == 1:  #3324
        fpoint += AppearTime[f"AppearTime{k}"] * k
    return fpoint
  if AppearTime["AppearTime4"] == 2:
    if AppearTime["AppearTime5"] == 2:
      fpoint = 10
      return fpoint
    if AppearTime["AppearTime6"] == 2:
      fpoint = 12
      return fpoint
    for k in range(1, 7):
      if AppearTime[f"AppearTime{k}"] == 1:  #4435
        fpoint += AppearTime[f"AppearTime{k}"] * k
    return fpoint
  if AppearTime["AppearTime5"] == 2:
    if AppearTime["AppearTime6"] == 2:
      fpoint = 12
      return fpoint
    for k in range(1, 7):
      if AppearTime[f"AppearTime{k}"] == 1:  #5536
        fpoint += AppearTime[f"AppearTime{k}"] * k
    return fpoint
  if AppearTime["AppearTime6"] == 2:
    for k in range(1, 6):  #6613
      if AppearTime[f"AppearTime{k}"] == 1:
        fpoint += AppearTime[f"AppearTime{k}"] * k
    return fpoint

  if AppearTime["AppearTime1"] == 4:  #四顆一樣
    fpoint = 2
    return fpoint
  if AppearTime["AppearTime6"] == 4:
    fpoint = 12
    return fpoint
  if AppearTime["AppearTime2"] == 4:
    fpoint = 4
    return fpoint
  if AppearTime["AppearTime3"] == 4:
    fpoint = 6
    return fpoint
  if AppearTime["AppearTime4"] == 4:
    fpoint = 8
    return fpoint
  if AppearTime["AppearTime5"] == 4:
    fpoint = 10
    return fpoint
  


#-----------------------------------------分界線，以上是投骰子及判斷點數的主程式，以下是呼叫投骰印出點數和判斷輸贏，要加入金錢或經驗職等數值應該從下面加就好了

class Game03:
  def __init__(self, session: Server):
    self.session = session

  async def start(self):
    WaitForPlayer = str(input('客官，輸入"投骰"擲出你的骰子:'))
    if WaitForPlayer == '投骰':
      Player = countPoint()
      print(f"你的點數是 {Player}")
      time.sleep(1)
      Computer = countPoint()
      print(f"對手的點數是 {Computer}")
      time.sleep(1)
      if Player > Computer:
        print('會贏喔!!')
        pause()
      if Player < Computer:
        print('不是哥們!你輸了🖥️ 🦐')
        pause()
      if Player == Computer:
        print('平手!')
        pause()

