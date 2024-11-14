from dataclasses import dataclass

@dataclass
class BossData:
    ID: int
    Name: str
    HP: int
    ATK: int
    DEF: int

@dataclass
class HeroData:
    ID: int
    Name: str
    SkillID: int
    HeroTypeID: int
    UpgradeCurveID: int
    BaseAtk: int
    BaseDef: int

@dataclass
class HeroSkillData:
    ID: int
    HeroID: int
    Name: str
    Description: str
    AtkMultiplier: float

@dataclass
class HeroTypeData:
    ID: int
    Name: str

@dataclass
class ItemTypeData:
    ID: int
    Name: str

@dataclass
class MinigameData:
    ID: int
    LevelLimit: int
    Name: str

@dataclass
class RewardData:
    ID: int
    Name: str
    Description: str

@dataclass
class RoomData:
    ID: int
    LevelLimit: int
    Name: str
    BossID: int

@dataclass
class ShopData:
    ItemType: int
    ItemID: int
    ItemCost: int

@dataclass
class UpgradeCurveData:
    ID: int
    Atk: float
    Def: float

@dataclass
class WeaponData:
    ID: int
    Name: str
    Description: str
    UpgradeCurveID: int
    SkillID: int

@dataclass
class WeaponSkillData:
    ID: int
    WeaponID: int
    Name: str
    Description: str