import logging
import os
from conf import *
from getpass import getpass
from typing import List, Tuple, Dict, Any
from shop.helper.type_hint import *
from difflib import SequenceMatcher
from shop.utils.decorators import timer_decorator
from shop.models import shop_items



logger = logging.getLogger(__name__)


class ShoppingList:


    def __init__(self) -> None:
        self.basket: List[Tuple[str, int]] = []


    def add_item(self, item: str, item_quantity: int) -> None:
        """
        Add an item to the shopping list with the specified quantity.

        :param item: The name of the item to add.
        :param item_quantity: The quantity of the item to add.
        """
        if self.validation_item_check(item):
            if not self.is_temporary_check(item):
                if self.stock_check(item, item_quantity):
                    self.basket.append((item, item_quantity))
                    logger.debug(f"Adding `{item}` to user's basket.")
                    print(f'\t-You selected {item_quantity} of {item}')
                else:
                    print(f"\t-we haven't enough {item} in our stock !!!")
                    logger.warning(f"user wants to add an item ({item}) but we haven't {item_quantity} of that.")
            else:
                print('\t-You have this item in your list already!')
                logger.warning(f"user wants to add an item ({item}) that already exists in shopping list.")
        else:
            print(f"\t-We don't have enough {item} in our shop.")
            logger.warning(f"user wants to add an item ({item}) that doesn't exist in shopping list.")


    '''
    def remove_item(self, item: str) -> None:
        """
        Remove the specified item from the shopping list.

        :param item: The name of the item to remove.
        """
        removed = False
        self.basket = [item_for_remove for item_for_remove in self.basket if (not removed and (removed := item_for_remove[0] == item)) or not removed]
        if removed:
            print(f'\t-Removed {item} from the list')
            logger.debug(f'user removed `{item} from shopping list.')
        else:
            print(f'\t-{item} not found in the list')
            logger.warning(f"user wants to remove item ({item}) that doesn't exist in shopping list.")
        getpass('\n\nPress Enter to continue...')
    '''


    def remove_item(self, item: str, item_quantity: int) -> None:
        """
        Remove the specified item from the shopping list.

        :param item: The name of the item to remove.
        """
        for item_for_remove in self.basket:
            if item_for_remove[0] == item:
                self.basket.remove(item_for_remove)
                for item_name in shop_items:
                    if item_name[0] == item:         
                        item_name[2] = str(int(item_name[2]) + item_quantity)
                        print(f'\t-Removed {item} from the list')
                        logger.debug(f'user removed `{item} from shopping list.')
                getpass('\n\nPress Enter to continue...')
                break
        else:
            print(f'\t-{item} not found in the list')
            logger.warning(f"user wants to remove item ({item}) that doesn't exist in shopping list.")
            getpass('\n\nPress Enter to continue...')


    def is_temporary_check(self, item: str) -> bool:
        """
        Check if the specified item is already in the shopping list.

        :param item: The name of the item to check.
        :return: True if the item is in the list, False otherwise.
        """
        for item_in_basket in self.basket:
            if item_in_basket[0] == item:
                return True
        return False


    @staticmethod
    def validation_item_check(item: str) -> bool:
        """
        Check if the specified item exists in the shop.

        :param item: The name of the item to check.
        :return: True if the item exists in the shop, False otherwise.
        """
        item_quantity = list()
        item_name = list()
        for items in shop_items:
            item_name.append(items[0])
            item_quantity.append(items[2])
        
        if item in item_name:
            return True
        else:
            return False


    def permission_for_quantity_input(self, item: str) -> bool:
        """
        Check if the user is allowed to enter a quantity for the specified item.

        :param item: The name of the item to check.
        :return: True if the user is allowed to enter a quantity, False otherwise.
        """
        item_name = list()
        for items in shop_items:
            item_name.append(items[0])
            if item in item_name:
                if int(items[2])>0:
                    if self.validation_item_check(item):
                        if not self.is_temporary_check(item):
                            return True
                        else:
                            print('\t-You have added this item already!')
                            logger.warning(f"user wants to add an item ({item}) that already exists in shopping list.")
                    else:
                        print("\t-We don't have this item in our shop!")
                        logger.warning(f"user wants to add an item ({item}) that doesn't exist in shopping list.")
                    return False


    @staticmethod
    def item_can_user_choose() -> None:
        """
        Print a list of items that the user can choose from.
        """
        for item_can_user_choose in shop_items:
            print(f"\t-({item_can_user_choose[0]} x{item_can_user_choose[2]})-", end=" ")
        print()


    @staticmethod
    def show_help() -> None:
        """
        Print a list of available commands for the user.
        """
        print("\n\t-Please enter one of the commands below when you see `->`.")
        print('\t----')
        print("\t-`remove`, if you want to remove an item.")
        print("\t-`search`, if you want to search an item in your basket.")
        print("\t-`summery`, if you want to know what did you do.")
        print("\t-`show`, if you want to show your basket items.")
        print("\t-`exit`, if you want to exit the program. (you can also use `quit`,`q`,`ex`)")
        print('\t----')


    @property
    def show_basket(self) -> None:
        """
        Print the current items in the shopping list.
        """
        print('\t-Your basket till here ->', self.basket)


    def similarity(self, item_for_search: str) -> List[float]:
        """
        Calculate the similarity ratio between the given item and all the items in the shop.

        :param item_for_search: The name of the item to search for.
        :return: A list of similarity ratios between the given item and all the items in the shop.
        """
        
        item_name = [item[0] for item in shop_items]
        ratio = []
        for item in item_name:
            matcher = SequenceMatcher(None, item_for_search, item)
            ratio.append(matcher.ratio())
        return ratio

    @timer_decorator
    def search_item(self) -> None:
        """
        Prompt the user to enter an item for search, calculate the similarity ratio between the entered item and all the items in the shop,
        and print out the list of items that have a similarity ratio of 0.8 or higher. If no items are found, print a warning message.

        :return: None
        """
        item_for_search = (input('\t-Enter the name of the item you are searching for: ')).lower()
        similarity_percents = self.similarity(item_for_search)
        try:
            for similarity_percent in similarity_percents:
                if similarity_percent >= 0.75:
                    print(f'\n\t-yes , we have .')
                    print(f'\t-We found an item with {similarity_percent*100:.2f}% similarity to what we have.')
                    logger.debug(f'User searched for {item_for_search} and found a similar item in their basket.')
                    break
        except :
            print(f"\t-Sorry, we couldn't find any items similar to {item_for_search} in your basket.")
            logger.warning(f'User searched for {item_for_search} but found no similar items in their basket.')


    def stock_check(self, item: str, item_quantity: int) -> bool:
        """
        Check if the specified item is in stock and has enough quantity.

        :param item: The name of the item to check.
        :param item_quantity: The quantity of the item to check.
        :return: True if the item is in stock and has enough quantity, False otherwise.
        """
        item_name = list()
        for items in shop_items:
            item_name.append(items[0])
            if item in item_name:
                if int(items[2]) >= item_quantity:
                    items[2] = str(int(items[2]) - item_quantity)
                    return True
                else:
                    return False


    @staticmethod
    def clear_screen() -> None:
        """Clear screen function"""
        os.system('cls' if os.name == 'nt' else 'clear')


    def calculate_total_price(self) -> int:
        """
        Calculate the total price of the items in the shopping list.

        :return: The total price of the items in the shopping list.
        """
        total_price = 0
        for item, quantity in self.basket:
            for items in shop_items:
                if item in items[0]:
                    item_price = int(items[1])
                    total_price += item_price * quantity
                    return total_price


    def get_basket_summary(self) -> None:
        """
        Print a summary of the items in the shopping list, including the total price.
        """
        if self.basket:
            total_price = 0
            print('\n\n\t-Your shopping list summery :')
            for item, quantity in self.basket:
                total_price = self.calculate_total_price()
                print(f'\t-you have {item} x{quantity} in your basket')
            print(f'\t-Total price: {total_price}')
            logger.debug(f"user viewed shopping list summary. Total price: {total_price} ")
        else:
            print('\n\n\t-Your shopping list is empty.')
            logger.warning("user viewed shopping list summary but it's empty.")


    def ten_percent_discount(self,price:float)->float:
        return float(price)*0.9 


    def twenty_percent_discount(self,price:float)->float:
        return float(price)*0.8


    def thirty_percent_discount(self,price:float)->float:
        return float(price)*0.7


    def apply_discount(self,discount: float) -> None:
        """
        Apply a discount to the total price.

        :param total_price: The original total price of the items.
        :param discount: The discount to apply.
        """
        print(f'\t-Total price after applying discount is : {discount}')
