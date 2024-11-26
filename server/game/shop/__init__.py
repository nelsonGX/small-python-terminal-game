from typing import List

from server.data.data import ShopData
from server.data.loader import DataLoader
from server.proto.game import Retcode


class ShopManager:
    def __init__(self, server):
        self.session = server

    # Get available shop data
    async def get_available_items(self):
        return_list: List[ShopData] = []
        # Find not bought items
        for item in DataLoader.shop_data:
            if item.ItemID not in self.session.saving.data.player_cur_data.shop_info.bought_items:
                return_list.append(item)
        return return_list

    # Buy item in shop
    async def buy_item(self, item_id: int) -> Retcode:
        if item_id in self.session.saving.data.player_cur_data.shop_info.bought_items:
            return Retcode.ITEM_ALREADY_BOUGHT
        else:
            # Find item in Excel
            item = next((item for item in DataLoader.shop_data if item.ItemID == item_id), None)
            # Check if item exists
            if item is None:
                return Retcode.ITEM_NOT_FOUND
            player_cur_data = self.session.saving.data.player_cur_data
            # Check if player has enough currency
            if player_cur_data.shop_info.owned_currency < item.ItemCost:
                return Retcode.NOT_ENOUGH_CURRENCY
            # Add item to bought list
            player_cur_data.shop_info.bought_items.append(item_id)
            # Save data
            await self.session.saving.save()
            # Return success
            return Retcode.SUCCESS
        
    async def get_owned_currencies(self) -> int:
        return self.session.saving.data.player_cur_data.shop_info.owned_currency
    
    async def set_owned_currencies(self, currency: int):
        self.session.saving.data.player_cur_data.shop_info.owned_currency = currency