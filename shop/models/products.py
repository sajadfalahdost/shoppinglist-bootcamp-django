import csv

shop_items = list()


with open('shop_item.csv', 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                shop_items.append(row)


# shop_items =[
#     ['apple', '10000', '5', 'TRUE', 'fruit'], 
#     ['kiwi', '20000', '3', 'TRUE', 'fruit'], 
#     ['banana', '30000', '4', 'TRUE', 'fruit'], 
#     ['orange', '2000', '2', 'TRUE', 'fruit'], 
#     ['cake', '40000', '5', 'TRUE', 'market'], 
#     ['chips', '50000', '1', 'TRUE', 'market'], 
#     ['water', '20000', '8', 'TRUE', 'market'], 
#     ['nuts', '10000', '0', 'FALSE', 'market'], 
#     ['ice cream', '25000', '0', 'FALSE', 'market'], 
#     ['shirt', '10000', '10', 'TRUE', 'botic']
#     ]