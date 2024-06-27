import pytest
from cookie_shop import *


class Tests:
    @classmethod
    def get_mock_cookies(cls):
        cookies = [
            {
                "id": 1,
                "title": "Basboosa Semolina Cake",
                "description": "This is a This is a traditional Middle Eastern dessert made with semolina and yogurt then soaked in a rose water syrup.",
                "price": 3.99,
            },
            {
                "id": 2,
                "title": "Vanilla Chai Cookie",
                "description": "Crisp with a smooth inside. Rich vanilla pairs perfectly with its Chai partner a combination of cinnamon ands ginger and cloves. Can you think of a better way to have your coffee AND your Vanilla Chai in the morning?",
                "price": 5.50,
            },
        ]
        return cookies

    @classmethod
    def mock_input(cls, mock_data, call_counter, monkeypatch):
        """
        Mock the builtin input function
        :param mock_data: Dictionary of data to mock.
        :param call_counter: Dictionary of counters for function calls
        :param monkeypatch: pytest's monkeypatch object
        """

        # mock the input function
        def new_input(message):
            call_counter["input"] += 1
            return mock_data["input"].pop(0)

        monkeypatch.setattr("builtins.input", lambda x: new_input(x))

    def test_welcome(self, capsys, monkeypatch):
        """
        Does the welcome messagee output with the correct text?
        """
        # Mock the input function
        mock_inputs = iter(["no", "no", "no"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        # call the function
        welcome()

        # get the expected output
        expected = """
    Welcome to the Python Cookie Shop!
    We feed each according to their need.  
    """.strip()

        # get the output
        captured = capsys.readouterr()  # capture print output
        actual = captured.out.strip()  # split by line break
        actual = " ".join(actual.lower().split())  # remove multiple whitespace
        expected = " ".join(expected.lower().split())  # remove multiple whitespace
        assert actual == expected

    def test_bake_cookies_opens_file(self, monkeypatch):
        """
        Does bake_cookies open the data file.
        """

        def new_open(oldopen, file, mode):
            data["calls"] += 1
            data["file"] = file
            return oldopen(file, mode)

        oldopen = open
        monkeypatch.setattr(
            "builtins.open", lambda file, mode="r": new_open(oldopen, file, mode)
        )
        data = {"calls": 0, "file": ""}
        bake_cookies("data/cookies.csv")
        assert data["calls"] == 1
        assert data["file"] == "data/cookies.csv"

    def test_bake_cookies_gets_list(self, monkeypatch):
        """
        Does bake_cookies return a list with 10 or more items?
        """
        results = bake_cookies("data/cookies.csv")
        assert len(results) >= 10  # there are 10 or more results
        assert type(results) == list  # the results are in a list

    def test_bake_cookies_list_contains_dictionaries(self, monkeypatch):
        """
        Does bake_cookies return a list of dictionaries?
        """
        results = bake_cookies("data/cookies.csv")
        # check that each item in list is a dictionary
        for val in results:
            assert type(val) == dict  # each items in the list is a dictionary

    def test_bake_cookies_dictionaries_contain_valid_data(self, monkeypatch):
        """
        Does bake_cookies return a list of dictionaries?
        """
        results = bake_cookies("data/cookies.csv")

        # check that each item in list is a dictionary
        for val in results:
            assert type(val["id"]) == int  # the id is an int
            assert type(val["title"]) == str  # the title is a string
            assert type(val["description"]) == str  # the description is a string
            assert type(val["price"]) == float  # the price is a float

            assert len(val["title"]) >= 2  # a length of at least two
            assert len(val["description"]) >= 10  # a length of at least ten

    def test_display_cookies(self, capsys):
        """
        Does display_cookies output the right data?
        """
        nut_allergy = False
        gluten_allergy = False
        diabetic = False
        display_cookies(Tests.get_mock_cookies(), nut_allergy, gluten_allergy, diabetic)

        # what we expect
        expected = """
Here are the cookies we have in the shop for you:

#1 - Basboosa Semolina Cake
This is a This is a traditional Middle Eastern dessert made with semolina and yogurt then soaked in a rose water syrup.
Price: $3.99

#2 - Vanilla Chai Cookie
Crisp with a smooth inside. Rich vanilla pairs perfectly with its Chai partner a combination of cinnamon ands ginger and cloves. Can you think of a better way to have your coffee AND your Vanilla Chai in the morning?
Price: $5.50
    """.strip()

        # get the output
        captured = capsys.readouterr()  # capture print output
        actual = captured.out.strip()  # split by line break
        actual = " ".join(actual.lower().split())  # remove multiple whitespace
        expected = " ".join(expected.lower().split())  # remove multiple whitespace
        #assert actual == expected

    def test_get_cookie_from_dict(self):
        """
        Does the proper cookie get returned from the list, given its id?
        """
        cookies = Tests.get_mock_cookies()

        # see that we can get a cookie by its id
        for cookie in cookies:
            # call the function
            actual = get_cookie_from_dict(cookie["id"], cookies)
            # what we expect
            expected = cookie
            # compare the two
            assert actual == expected

    def test_solicit_quantity_validation(self, capsys, monkeypatch):
        """
        Do the validation rules work.
        """

        mock_data = {"input": ["foo", "bar", "-2", "4", "5"]}
        call_counter = { 
            "input": 0,
        }
        # mock the input function
        Tests.mock_input(mock_data, call_counter, monkeypatch)
        cookies = Tests.get_mock_cookies()

        # call the function
        quantity = solicit_quantity(1, cookies)

        # check the output for the correct diagnosis
        captured = capsys.readouterr()  # capture print output
        actual = captured.out.lower().strip()  # split by line break

        # check that the input function was called until the valid intput
        assert call_counter["input"] == 4

    def test_solicit_quantity_output(self, capsys, monkeypatch):
        """
        Does the function print the correct text and return the quantity?
        """

        mock_data = {"input": ["foo", "bar", "-2", "8", "4"]}
        call_counter = {
            "input": 0,
        }
        # mock the input function
        Tests.mock_input(mock_data, call_counter, monkeypatch)
        cookies = Tests.get_mock_cookies()

        # call the function
        quantity = solicit_quantity(2, cookies)

        # check the output for the correct diagnosis
        captured = capsys.readouterr()  # capture print output
        actual = captured.out.lower().strip()  # split by line break

        # check that the input function was called until the valid intput
        assert call_counter["input"] == 4

        # check that the output contained the correct price, quantity, and cookie
        assert "$44.00" in actual
        assert "8 Vanilla Chai Cookie".lower() in actual.lower()

        # assert that the function returned the quantity
        assert quantity == 8

    def test_display_order_total(self, capsys, monkeypatch):
        """
        Does the function print the correct text?
        """

        # mock an order
        order = [
            {"id": 1, "quantity": 10},
            {"id": 2, "quantity": 50},
        ]

        # get full list of cookies
        cookies = Tests.get_mock_cookies()

        # call the function
        display_order_total(order, cookies)

        # check the output for the correct diagnosis
        captured = capsys.readouterr()  # capture print output
        actual = captured.out.lower().strip()  # split by line break

        # check the output
        assert "$314.90" in actual  # total price
        assert "10 Basboosa Semolina Cake".lower() in actual.lower()
        assert "50 Vanilla Chai Cookie".lower() in actual.lower()

    def test_solicit_order_validate(self, capsys, monkeypatch):
        """
        Does the function validate the input correctly.
        """

        mock_data = {"input": ["foo", "bar", "-10", "2", "5", "quit", "5", "2"]}
        call_counter = {
            "input": 0,
        }
        # mock the input function
        Tests.mock_input(mock_data, call_counter, monkeypatch)
        cookies = Tests.get_mock_cookies()

        # call the function
        actual = solicit_order(cookies)

        # our expected result
        expected = [{"id": 2, "quantity": 5}]

        # check that the input function was called until the valid intput
        assert call_counter["input"] == 6

        # assert that the function returned the quantity
        assert actual == expected

    def test_solicit_order_data(self, capsys, monkeypatch):
        """
        Does the function return the proper order data?
        """

        mock_data = {"input": ["1", "5", "2", "10", "finished", "5", "10"]}
        call_counter = {
            "input": 0,
        }
        # mock the input function
        Tests.mock_input(mock_data, call_counter, monkeypatch)
        cookies = Tests.get_mock_cookies()

        # call the function
        actual = solicit_order(cookies)

        # our expected result
        expected = [{"id": 1, "quantity": 5}, {"id": 2, "quantity": 10}]

        # check that the input function was called until the valid intput
        assert call_counter["input"] == 5

        # assert that the function returned the quantity
        assert actual == expected
