# helper function updates the key by the value if the key exists and adds the key with the value if it doesn't already exist
# updates contents of dictionary, no return
def update_or_add(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value


# helper function determines if a chain from chain_values list has a certain key
# returns int
def chain_has_value(dictionary, key, mapped_val):
    if key not in dictionary:
        return False
    return mapped_val in dictionary[key]


# helper function that takes a dictionary and a list (chain) and if the chain var is a key in the dictionary, returns the key with the highest value
# returns int (-1 if no value in the list is a key)
def optimal_chain_value(dictionary, chain):
    best_chain_val = -1
    max_val = 0
    for i in chain:
        if i in dictionary:
            if dictionary[i] > max_val:
                max_val = dictionary[i]
                best_chain_val = i
    return best_chain_val

# helper function determines if subtracting a number from a key's value in a dictionary would drop the key's value below zero
# returns bool
def not_drop_below_zero(dictionary, key, value):
    if key in dictionary:
        key_val = dictionary[key]
        if key_val - value >= 0:
            return True
    return False

# main function that takes an inventory (dictionary that associates an int to an int), products_needed (dictionary that associates an int to an int), and product_chain (dictionary that associates an int to a list of ints)
# returns added products (dictionary that associates an int to an int) and returns an updated inventory
def order_optimize(inventory, products_needed, product_chain):

    # we need to initialize a dictionary to keep track of products we have added
    added_products = {}

    # we need to go through every value (both product id and quantity) in our products needed dictionary
    for product_id, quantity in products_needed.items():
        quantity_num = quantity

        # keep going until we have fulfilled the order
        while quantity_num > 0:

            # make sure product id exists in the inventory, if not, return a string stating the product doesn't exist
            if product_id in inventory:
                # if the original product we want has more than 0 in quantity, update added_products and the inventory accordingly
                if inventory[product_id] > 0:
                    # see if the value of the item will drop below 0
                    if not_drop_below_zero(inventory, product_id, quantity_num):
                        update_or_add(added_products, product_id, quantity_num)
                        # if it doesn't subtract the quantity
                        update_or_add(inventory, product_id, -quantity_num)
                        quantity_num -= quantity_num
                    # if it does drop the value below 0, subtract what we have left of that product
                    elif quantity_num > 0:
                        quantity_num -= inventory[product_id]
                        update_or_add(added_products, product_id, inventory[product_id])
                        update_or_add(inventory, product_id, -inventory[product_id])
                # in this case, the original product has run out so we need to use our backup product
                else:

                    # find the best backup product
                    map_list = product_chain[product_id]
                    optimal_chain_id = optimal_chain_value(inventory, map_list)

                    # if there is no backup product with a quantity above 0, this means we have run out of product
                    if optimal_chain_id == -1:
                        return "We have run out of relevant product for product id #" + str(product_id)
                    
                    # otherwise, the logical remains the same as the original product in inventory
                    if optimal_chain_id in inventory:
                        if not_drop_below_zero(inventory, optimal_chain_id, quantity_num):
                            update_or_add(added_products, optimal_chain_id, quantity_num)
                            update_or_add(inventory, optimal_chain_id, -quantity_num)
                            quantity_num -= quantity_num
                            
                        elif quantity_num > 0:
                            quantity_num -= inventory[optimal_chain_id]
                            update_or_add(added_products, optimal_chain_id, inventory[optimal_chain_id])
                            update_or_add(inventory, optimal_chain_id, -inventory[optimal_chain_id])
            else:
                return "Product id #" + str(product_id) + " does not exist in inventory"

    # return what we have added to the order and our updated inventory                  
    return added_products, inventory


# tests

# test 1: the test given in the take home assessment
inventory1 = {51: 14, 88: 1, 109: 7, 343: 500}
product_chain1 = {51: [109], 88: [343]}
products_needed1 = {51: 20, 88: 10}
# in real application, I would call add_product_to_order(product_id, amount) and add the values in order_optimize(inventory1, products_needed1, product_chain1)[0]
# for test purposes, I will print out what order_optimize returns for test values
print(order_optimize(inventory1, products_needed1, product_chain1))


# test 2: multiple products in the product_chain
inventory2 = {51: 14, 88: 1, 109: 7, 343: 500, 90: 20, 101: 8, 800: 101}
product_chain2 = {51: [109, 90, 101], 88: [343, 800]}
products_needed2 = {51: 45, 88: 600}
# print test 2
print(order_optimize(inventory2, products_needed2, product_chain2))


# test 3: inventory runs out
inventory3 = {51: 14, 88: 1, 109: 7, 343: 500, 90: 20, 101: 8, 800: 101}
product_chain3 = {51: [109, 90, 101], 88: [343, 800]}
products_needed3 = {51: 45, 88: 700}
# print test 3
print(order_optimize(inventory3, products_needed3, product_chain3))


# test 4: wrong product id
inventory4 = {51: 14, 88: 1, 109: 7, 343: 500, 90: 20, 101: 8, 800: 101}
product_chain4 = {51: [109, 90, 101], 88: [343, 800]}
products_needed4 = {52: 45, 88: 700}
# print test 4
print(order_optimize(inventory4, products_needed4, product_chain4))




