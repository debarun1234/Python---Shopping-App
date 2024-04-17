# Python - Shopping App version 1a
import pickle
import os

class Product:
    def __init__(self, product_id, name, category_id, price):
        self.product_id = product_id
        self.name = name
        self.category_id = category_id
        self.price = price

class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity):
        if product.product_id in self.items:
            self.items[product.product_id]['quantity'] += quantity
        else:
            self.items[product.product_id] = {'product': product, 'quantity': quantity}
        return f"Added {quantity} {product.name} to your cart."

    def remove_item(self, product_id, quantity):
        if product_id in self.items and self.items[product_id]['quantity'] >= quantity:
            self.items[product_id]['quantity'] -= quantity
            if self.items[product_id]['quantity'] == 0:
                del self.items[product_id]
            return "Item removed from your cart."
        return "Item or quantity not found in cart."

    def view_cart(self):
        if not self.items:
            return "Your cart is empty."
        result = "Cart Contents:\n"
        for item_id, details in self.items.items():
            result += f"{details['product'].name}: Quantity = {details['quantity']} at Rs. {details['product'].price} each\n"
        return result

    def checkout(self, payment_method):
        if not self.items:
            return "Your cart is empty, no payment needed."

        total = sum(item['product'].price * item['quantity'] for item in self.items.values())
        self.items.clear()  # Clear the cart after checkout

        if payment_method.lower() == "upi":
            return f"You will be shortly redirected to the portal for Unified Payment Interface to make a payment of Rs. {total}."
        elif payment_method.lower() in ["net banking", "paypal"]:
            return f"Your order is successfully placed using {payment_method}. Total amount: Rs. {total}."
        else:
            return "Invalid payment method."

class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.cart = Cart()

class Catalog:
    def __init__(self):
        self.products = {}
        self.categories = {}

    def add_category(self, category):
        self.categories[category.category_id] = category
        return f"Category {category.name} added."

    def add_product(self, product):
        if product.category_id in self.categories:
            self.products[product.product_id] = product
            return f"Product {product.name} added under {self.categories[product.category_id].name}."
        return "Category does not exist."

    def update_product(self, product_id, name=None, category_id=None, price=None):
        if product_id in self.products:
            if name:
                self.products[product_id].name = name
            if category_id and category_id in self.categories:
                self.products[product_id].category_id = category_id
            if price:
                self.products[product_id].price = price
            return f"Product {product_id} updated."
        return "Product not found."

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            return "Product removed from catalog."
        return "Product not found."

    def view_catalog(self):
        if not self.products:
            return "Catalog is empty."
        result = "Available Products:\n"
        for product_id, product in self.products.items():
            result += f"ID: {product_id}, Name: {product.name}, Category: {self.categories[product.category_id].name}, Price: Rs. {product.price}\n"
        return result

def load_data():
    if os.path.exists('app_data.pkl'):
        with open('app_data.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return {"users": {}, "catalog": Catalog()}

def save_data(data):
    with open('app_data.pkl', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def authenticate(users, username, password):
    user = users.get(username)
    if user and user.password == password:
        return user
    return None

def main():
    data = load_data()
    catalog = data["catalog"]
    users = data["users"]

    # Initialize admin and user if not already present
    if "admin" not in users:
        users["admin"] = User("admin", "password123", is_admin=True)
    if "user1" not in users:
        users["user1"] = User("user1", "password123")

    print("Welcome to the Demo Marketplace!")
    while True:
        username = input("Enter username or 'exit' to quit: ").strip()
        if username.lower() == 'exit':
            print("Exiting the system. Goodbye!")
            break
        password = input("Enter password: ").strip()
        user = authenticate(users, username, password)
        if user:
            print(f"Welcome {user.username}! You are {'an admin' if user.is_admin else 'a user'}.")
            while True:
                if user.is_admin:
                    action = input("Actions for Admin (view_catalog, add_product, update_product, remove_product, add_category, logout): ").strip().lower()
                else:
                    action = input("Actions for User (view_catalog, add_to_cart, remove_from_cart, checkout, logout): ").strip().lower()
                
                if action == "logout":
                    print(f"{user.username} logged out.")
                    break
                elif action == "view_catalog":
                    print(catalog.view_catalog())
                elif action in ["add_to_cart", "remove_from_cart", "checkout"] and not user.is_admin:
                    product_id = input("Enter product ID: ")
                    if action == "add_to_cart":
                        quantity = int(input("Enter quantity: "))
                        product = catalog.products.get(product_id)
                        if product:
                            print(user.cart.add_item(product, quantity))
                        else:
                            print("Product not found.")
                    elif action == "remove_from_cart":
                        quantity = int(input("Enter quantity: "))
                        print(user.cart.remove_item(product_id, quantity))
                    elif action == "checkout":
                        payment_method = input("Enter payment method (UPI, Net banking, PayPal): ")
                        print(user.cart.checkout(payment_method))
                elif action in ["add_product", "update_product", "remove_product", "add_category"] and user.is_admin:
                    if action == "add_product":
                        name = input("Enter product name: ")
                        category_id = input("Enter category ID: ")
                        price = float(input("Enter price: "))
                        product_id = input("Enter product ID: ")
                        print(catalog.add_product(Product(product_id, name, category_id, price)))
                    elif action == "update_product":
                        product_id = input("Enter product ID: ")
                        name = input("Enter new product name (leave blank to skip): ")
                        category_id = input("Enter new category ID (leave blank to skip): ")
                        price = input("Enter new price (leave blank to skip): ")
                        price = float(price) if price else None
                        print(catalog.update_product(product_id, name, category_id, price))
                    elif action == "remove_product":
                        product_id = input("Enter product ID: ")
                        print(catalog.remove_product(product_id))
                    elif action == "add_category":
                        category_id = input("Enter category ID: ")
                        name = input("Enter category name: ")
                        print(catalog.add_category(Category(category_id, name)))
                else:
                    print("Invalid action or unauthorized.")
        else:
            print("Invalid login, please try again.")
    save_data({"users": users, "catalog": catalog})

if __name__ == "__main__":
    main()
