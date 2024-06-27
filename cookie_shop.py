"""
Functions necessary for running a virtual cookie shop.
See README.md for instructions.
Do not run this file directly.  Rather, run main.py instead.
"""
from pathlib import Path

def bake_cookies(filepath):
    """
    Opens up the CSV data file from the path specified as an argument.
    - Each line in the file, except the first, is assumed to contain comma-separated information about one cookie.
    - Creates a dictionary with the data from each line.
    - Adds each dictionary to a list of all cookies that is returned.

    :param filepath: The path to the data file.
    :returns: A list of all cookie data, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    cookies = []
    with open(filepath, 'r') as file:
        # Skip the header row
        header = next(file).strip().split(',')
        has_extra_fields = len(header) > 4

        for line in file:
            cookie_data = line.strip().split(',')
            cookie = {
                'id': int(cookie_data[0]),
                'title': cookie_data[1],
                'description': cookie_data[2],
                'price': float(cookie_data[3].replace('$', ''))
            }
            if has_extra_fields:
                cookie['sugar_free'] = cookie_data[4] == 'True'
                cookie['gluten_free'] = cookie_data[5] == 'True'
                cookie['contains_nuts'] = cookie_data[6] == 'True'
            cookies.append(cookie)
    return cookies

def welcome():
    """
    Prints a welcome message to the customer in the format:

      Welcome to the Python Cookie Shop!
      We feed each according to their need.

    """
    # write your code for this function below this line
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.")

    # Extra credit: Ask for dietary restrictions
    nut_allergy = input("Are you allergic to nuts? (yes/no) ").lower() in ['yes', 'y']
    gluten_allergy = input("Are you allergic to gluten? (yes/no) ").lower() in ['yes', 'y']
    diabetic = input("Do you suffer from diabetes? (yes/no) ").lower() in ['yes', 'y']

    return nut_allergy, gluten_allergy, diabetic




def display_cookies(cookies, nut_allergy, gluten_allergy, diabetic):
    # ... (rest of the function remains the same)
    """
    Prints a list of all cookies in the shop to the user.
    - Sample output - we show only two cookies here, but imagine the output continues for all cookiese:
        Here are the cookies we have in the shop for you:

          #1 - Basboosa Semolina Cake
          This is a This is a traditional Middle Eastern dessert made with semolina and yogurt then soaked in a rose water syrup.
          Price: $3.99

          #2 - Vanilla Chai Cookie
          Crisp with a smooth inside. Rich vanilla pairs perfectly with its Chai partner a combination of cinnamon ands ginger and cloves. Can you think of a better way to have your coffee AND your Vanilla Chai in the morning?
          Price: $5.50

    - If doing the extra credit version, ask the user for their dietary restrictions first, and only print those cookies that are suitable for the customer.

    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below this line
    for cookie in cookies:
        if (not nut_allergy or not cookie['contains_nuts']) and \
           (not gluten_allergy or cookie['gluten_free']) and \
           (not diabetic or cookie['sugar_free']):
            print(f"\n#{cookie['id']} - {cookie['title']}")
            print(cookie['description'])
            print(f"Price: ${cookie['price']:.2f}")
def run_shop(cookies):
     nut_allergy, gluten_allergy, diabetic = welcome()
     display_cookies(cookies, nut_allergy, gluten_allergy, diabetic)
     print("Here are the cookies we have in the shop for you:")



def get_cookie_from_dict(id, cookies):
    """
    Finds the cookie that matches the given id from the full list of cookies.

    :param id: the id of the cookie to look for
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: the matching cookie, as a dictionaryq`
    """
    # write your code for this function below this line
    for cookie in cookies:
        if cookie['id'] == id:
            return cookie
    return None


def solicit_quantity(id, cookies):
    """
    Asks the user how many of the given cookie they would like to order.
    - Validates the response.
    - Uses the get_cookie_from_dict function to get the full information about the cookie whose id is passed as an argument, including its title and price.
    - Displays the subtotal for the given quantity of this cookie, formatted to two decimal places.
    - Follows the format (with sample responses from the user):

        My favorite! How many Animal Cupcakes would you like? 5
        Your subtotal for 5 Animal Cupcake is $4.95.

    :param id: the id of the cookie to ask about
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: The quantity the user entered, as an integer.
    """
    # write your code for this function below this line
    cookie = get_cookie_from_dict(id, cookies)
    if cookie:
        while True:
            quantity = input(f"My favorite! How many {cookie['title']} would you like? ")
            if quantity.isdigit() and int(quantity) > 0:
                quantity = int(quantity)
                subtotal = quantity * cookie['price']
                print(f"Your subtotal for {quantity} {cookie['title']} is ${subtotal:.2f}.")
                return quantity
            else:
                print("Invalid input. Please enter a positive integer.")
    else:
        print("Invalid cookie ID. Please try again.")
        return 0



def solicit_order(cookies):
    """
    Takes the complete order from the customer.
    - Asks over-and-over again for the user to enter the id of a cookie they want to order until they enter 'finished', 'done', 'quit', or 'exit'.
    - Validates the id the user enters.
    - For every id the user enters, determines the quantity they want by calling the solicit_quantity function.
    - Places the id and quantity of each cookie the user wants into a dictionary with the format
        {'id': 5, 'quantity': 10}
    - Returns a list of all sub-orders, in the format:
        [
          {'id': 5, 'quantity': 10},
          {'id': 1, 'quantity': 3}
        ]

    :returns: A list of the ids and quantities of each cookies the user wants to order.
    """
    # write your code for this function below this line
    order = []
    while True:
        cookie_id = input("Please enter the number of any cookie you would like to purchase (type 'finished' if finished with your order): ")
        if cookie_id.lower() in ['finished', 'done', 'quit', 'exit']:
            break
        elif cookie_id.isdigit():
            cookie_id = int(cookie_id)
            quantity = solicit_quantity(cookie_id, cookies)
            if quantity > 0:
                order.append({'id': cookie_id, 'quantity': quantity})
        else:
            print("Invalid input. Please enter a valid cookie ID or 'finished'.")
    return order



def display_order_total(order, cookies):
    """
    Prints a summary of the user's complete order.
    - Includes a breakdown of the title and quantity of each cookie the user ordereed.
    - Includes the total cost of the complete order, formatted to two decimal places.
    - Follows the format:

        Thank you for your order. You have ordered:

        -8 Animal Cupcake
        -1 Basboosa Semolina Cake

        Your total is $11.91.
        Please pay with Bitcoin before picking-up.

        Thank you!
        -The Python Cookie Shop Robot.

    """
    # write your code for this function below this line
    total = 0
    print("Thank you for your order. You have ordered:")
    for item in order:
        cookie = get_cookie_from_dict(item['id'], cookies)
        quantity = item['quantity']
        price = cookie['price']
        subtotal = quantity * price
        total += subtotal
        print(f"-{quantity} {cookie['title']}")
    print(f"\nYour total is ${total:.2f}.")
    print("Please pay with Bitcoin before picking-up.")
    print("\nThank you!")
    print("-The Python Cookie Shop Robot.")



def run_shop(cookies):
    """
    Executes the cookie shop program, following requirements in the README.md file.
    - This function definition is given to you.
    - Do not modify it!

    :param cookies: A list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    nut_allergy, gluten_allergy, diabetic = welcome()
    display_cookies(cookies, nut_allergy, gluten_allergy, diabetic)
    order = solicit_order(cookies)
    display_order_total(order, cookies)
