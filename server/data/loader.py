from typing import List
import json
import aiofiles

from server.data.data import *


class DataLoader:
    boss_data: List[BossData] = []
    hero_data: List[HeroData] = []
    hero_skill_data: List[HeroSkillData] = []
    hero_type_data: List[HeroTypeData] = []
    item_type_data: List[ItemTypeData] = []
    minigame_data: List[MinigameData] = []
    reward_data: List[RewardData] = []
    room_data: List[RoomData] = []
    shop_data: List[ShopData] = []
    upgrade_curve_data: List[UpgradeCurveData] = []
    weapon_data: List[WeaponData] = []
    weapon_skill_data: List[WeaponSkillData] = []

    @staticmethod
    async def load_data(file_path: str, data_class):
        async with aiofiles.open(file_path, 'r', encoding="utf-8") as file:
            content = await file.read()
            data_list = json.loads(content)
            return [data_class(**data) for data in data_list]

    @classmethod
    async def initialize(cls):
        DataLoader.boss_data = await cls.load_data('data/BossData.json', BossData)
        DataLoader.hero_data = await cls.load_data('./data/HeroData.json', HeroData)
        DataLoader.hero_skill_data = await cls.load_data('./data/HeroSkillData.json', HeroSkillData)
        DataLoader.hero_type_data = await cls.load_data('./data/HeroTypeData.json', HeroTypeData)
        DataLoader.item_type_data = await cls.load_data('./data/ItemTypeData.json', ItemTypeData)
        DataLoader.minigame_data = await cls.load_data('./data/MinigameData.json', MinigameData)
        DataLoader.reward_data = await cls.load_data('./data/RewardData.json', RewardData)
        DataLoader.room_data = await cls.load_data('./data/RoomData.json', RoomData)
        DataLoader.shop_data = await cls.load_data('./data/ShopData.json', ShopData)
        DataLoader.upgrade_curve_data = await cls.load_data('./data/UpgradeCurveData.json', UpgradeCurveData)
        DataLoader.weapon_data = await cls.load_data('./data/WeaponData.json', WeaponData)
        DataLoader.weapon_skill_data = await cls.load_data('./data/WeaponSkillData.json', WeaponSkillData)