from client.animations import load_boss
from client.bossfight.boss1.boss import fight as fight_1
from client.bossfight.boss2.boss import fight as fight_2
from client.bossfight.boss2.boss import fight as fight_3

async def fight_boss(target_boss):
    await load_boss(speed=0.05)
    if target_boss == 1:
        await fight_1()
    elif target_boss == 2:
        await fight_2()
    elif target_boss == 3:
        await fight_3()

if __name__ == "__main__":
    import asyncio
    asyncio.run(fight_boss(1))