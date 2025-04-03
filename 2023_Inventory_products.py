# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:44:08 2023

@author: monte
"""

import json
import os
user_name = os.getlogin() 

class Inventory:

    def __init__(self, file_path):
        
        """
        Initialize inventory class
        load data from the specified file path
        """
        
        self.file_path = file_path
        self.load_inventory()

    def load_inventory(self):
        
        """
        Load inventory data
        If the file doesn't exist, initialize empty data structures
        """
        
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.products = data.get('products', {})
                self.products_sold = data.get('products_sold', {})
                self.profit_gross = data.get('profit_gross', 0)
                self.profit_net = data.get('profit_net', 0)
        except FileNotFoundError:
            self.products = {}
            self.products_sold = {}
            self.profit_gross = 0
            self.profit_net = 0

    def save_inventory(self):
        
        """
        Save the current state of the inventory to the specified file
        open and write in the json file
        """
        
        data = {
            'products': self.products,
            'products_sold': self.products_sold,
            'profit_gross': self.profit_gross,
            'profit_net': self.profit_net
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def add_products(self, name, quantity, cost, price):
        
        """
        Add products to the inventory
        If the product already exists, update the quantity
        """
        
        if name not in self.products:
            self.products[name] = {"Quantity": quantity, "Cost": cost, "Price": price}
            print(f"{name} added to the inventory")
        else:
            self.products[name]["Quantity"] += quantity
            print(f"{quantity} units of {name} added to the inventory")
        self.save_inventory()
        
    def list_products(self):
        
        """
        List all products in the inventory with their quantities, costs, and prices
        Cost = price of the product to be incurred for the warehouse
        Price = price of the product for the costumer
        """
        
        for key, values in self.products.items():
            print(f"Product: {key}, Quantity: {values['Quantity']} units, Cost: € {values['Cost']}, Price: € {values['Price']}")

    def sell_products(self, name, quantity):
        
        """
        Sell products from the inventory
        Update quantities and record sales
        """
        
        if name in self.products:
            q_available = self.products[name]["Quantity"]

            if quantity > q_available:
                print(f"Quantity of {name} is not available")
            else:
                price = self.products[name]["Price"]
                total_sold = quantity * price
                cost = self.products[name]["Cost"]
                total_cost = quantity * cost
                self.products[name]["Quantity"] -= quantity

                if name not in self.products_sold:
                    self.products_sold[name] = {"Quantity": quantity, "Total_Cost": total_cost, "Total_Sold": total_sold}
                else:
                    self.products_sold[name]["Quantity"] += quantity
                    self.products_sold[name]["Total_Cost"] += total_cost
                    self.products_sold[name]["Total_Sold"] += total_sold
    
                print(f"Product: {name}, Quantity: {quantity} units, Price: € {price}, Total: € {total_sold}")
                self.save_inventory()
        else:
            print(f"{name} is not in stock")

    def calculate_profit(self):
        
        """
        Calculate gross and net profits based on sales and costs
        """
        
        self.profit_gross = sum(item["Total_Sold"] for item in self.products_sold.values())
        total_cost = sum(item["Total_Cost"] for item in self.products_sold.values())
        self.profit_net = self.profit_gross - total_cost
        print(f"Total profit gross: €{self.profit_gross}, Total profit net: €{self.profit_net}")
        self.save_inventory()

def main():
    
    """
    Main function that collects input data from the user and provides commands: add, list, sell, help and close
    """
    
    file_path = r'C:\Users\{}\OneDrive\My Drive\OneDrive\Desktop\inventory_data.json'.format(user_name)
    inventory = Inventory(file_path)

    while True:
        command = input("Which command? ")
        if command.lower() == "add":
            try:
                name = input("Which product? ")
                if name.isdigit():
                    raise ValueError(f"{name} is a numeric value")

                if name not in inventory.products:
                    quantity = input(f"How many units of {name}? ")
                    if not quantity.isdigit():
                        raise ValueError(f"{quantity} is not a numeric value")
                    cost = input(f"Which cost for {name}? ")
                    if not cost.isdigit():
                        raise ValueError(f"{cost} is not a numeric value")
                    price = input(f"Which price for {name}? ")
                    if not price.isdigit():
                        raise ValueError(f"{price} is not a numeric value")
                    inventory.add_products(str(name), int(quantity), float(cost), float(price))
                else:
                    additional_quantity = input(f"How many additional units of {name}? ")
                    if not additional_quantity.isdigit():
                        raise ValueError(f"{additional_quantity} is not a numeric value")
                    inventory.add_products(str(name), int(additional_quantity), 0, 0)
                    
            except ValueError as error:
                print(f"Error: {error}")

        elif command.lower() == "list":
            inventory.list_products()
    
        elif command.lower() == "sell":
            try: 
                name = str(input("Which product? "))
                if name.isdigit():
                    raise ValueError(f"{name} is a numeric value")
                quantity = input(f"How many units of {name}? ")
                if not quantity.isdigit():
                    raise ValueError(f"{quantity} is not a numeric value")
                inventory.sell_products(name, int(quantity))
            except ValueError as error:
                print(f"Error: {error}")
                
        elif command.lower() == "profit":
            inventory.calculate_profit()
    
        elif command.lower() == "help":
            print(
                """
                Available commands:
                - add: add a product to the inventory
                - list: list products in inventory
                - sell: record a sale
                - profit: display total profits
                - help: display available commands
                - close: exit the program
                """
            )
    
        elif command.lower() == "close":
            print("Goodbye!")
            break
    
        else:
            print(f"{command} is not available")

                  
if __name__ == "__main__":
    main()



