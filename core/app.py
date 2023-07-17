import logging
from conf import  *
from getpass import getpass
from shop.shopping_list_class import ShoppingList
from shop.helper import EXIT_COMMANDS,unaccepted_value,accepted_value


logger = logging.getLogger(__name__)


def main() -> None:
    """
    Interactively create and manage a shopping list.

    This function creates a `ShoppingList` object and presents a menu to the user,
    allowing them to add, remove, and view items in the list. The user can also
    search for items and view a summary of the current basket.

    The function loops until the user specifies an exit command, at which point
    it calculates and displays the total price of the items in the basket.

    Raises:
        ValueError: If the user enters an invalid item quantity.

    Returns:
        None
    """
    shopping_list = ShoppingList()
    while True:
        shopping_list.clear_screen()
        print('\n\t\t\t\t\t\t\t\t\t-You can choose from the items below-\n')
        shopping_list.item_can_user_choose()
        item = input('\n\t-Please enter what you want (if you want help just type , help) -> ').lower()

        if item in EXIT_COMMANDS:
            total_price = shopping_list.calculate_total_price()
            print(f'\t-Your basket is -> {shopping_list.basket}')
            print(f'\t-Total price: {total_price}')
            has_discount = input('\n\t-do you have discount code ? ').lower()
            if has_discount in accepted_value:
                discount_code = input('\t-enter your code : ')
                shopping_list.clear_screen()
                print(f'\t-Your basket is -> {shopping_list.basket}')
                print(f'\t-price: {total_price}')
                if discount_code == 'shopping-10':
                    shopping_list.apply_discount(shopping_list.ten_percent_discount(total_price))
                    print('\n\t-tanks for your shopping')
                    logger.debug(f"user has discount code for shopping.")
                elif discount_code == 'shopping-20':
                    shopping_list.apply_discount(shopping_list.twenty_percent_discount(total_price))
                    print('\n\t-tanks for your shopping')
                    logger.debug(f"user has discount code for shopping.")
                elif discount_code == 'shopping-30':
                    shopping_list.apply_discount(shopping_list.thirty_percent_discount(total_price))
                    print('\n\t-tanks for your shopping')
                    logger.debug(f"user has discount code for shopping.")
                else:
                    print('\n\t-wrong discount code')
                    logger.warning(f"user inout wrong discount code.")
                break
            else:
                if has_discount in unaccepted_value :
                    shopping_list.clear_screen()
                    print('\n\t-tanks for your shopping')
                    logger.warning(f"user hasn't discount code for shopping.")
                    logger.debug(f"user left from app.")
                    break
                else:
                    shopping_list.clear_screen()
                    print('\t-invalid input')
                    print('\t-tanks for your shopping')
                    logger.warning(f"user hasn't discount code for shopping.")
                    logger.debug(f"user left from app.")
                break

        elif item == 'remove':
            item = input('\t-Please enter the item to remove -> ').lower()
            shopping_list.remove_item(item,item_quantity)
            continue

        elif item == 'help':
            shopping_list.show_help()

        elif item == 'show':
            shopping_list.show_basket

        elif item == 'add':
            pass

        elif item == 'search':
            shopping_list.search_item()

        elif item == 'help':
            shopping_list.show_help()

        elif item == 'summery':
            shopping_list.get_basket_summary()

        elif item == '':
            continue # ignore empty inputs

        else:
            if shopping_list.permission_for_quantity_input(item):
                try:
                    item_quantity = input(f"\t-How many {item} do you want to add? ")
                    item_quantity = int(item_quantity)
                except ValueError:
                    print("\t-Invalid quantity. Please enter a number.")
                    logger.warning(f"user input wrong value in input as item quantity -> -`{item_quantity}`")
                    getpass('\n\nPress Enter to continue...')
                    continue
                shopping_list.add_item(item, item_quantity)
            else:
                print(f"\t-we haven't {item} ,choose another item !!!")
                logger.warning(f"user select item that we finished in stock  -> -`{item}`")
        getpass('\n\nPress Enter to continue...')

