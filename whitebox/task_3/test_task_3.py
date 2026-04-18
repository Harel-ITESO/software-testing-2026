from whitebox.book_store import Book, BookStore, main
from whitebox.exercises import BankAccount, BankingSystem, Product, ShoppingCart


def test_bank_account_view_and_regular_transfer_integration(capsys):
    account = BankAccount("user123", 1000)
    banking_system = BankingSystem()

    account.view_account()
    assert banking_system.authenticate("user123", "pass123") is True
    assert banking_system.transfer_money("user123", "user456", 200, "regular") is True

    output = capsys.readouterr().out
    assert "The account user123 has a balance of 1000" in output
    assert "User user123 authenticated successfully." in output
    assert (
        "Money transfer of $200 (regular transfer) from user123 to user456 "
        "processed successfully." in output
    )


def test_banking_system_authenticate_then_reject_duplicate_login(capsys):
    banking_system = BankingSystem()

    assert banking_system.authenticate("user123", "pass123") is True
    assert banking_system.authenticate("user123", "pass123") is False

    output = capsys.readouterr().out
    assert "User user123 authenticated successfully." in output
    assert "User already logged in." in output


def test_banking_system_transfer_requires_authenticated_user(capsys):
    banking_system = BankingSystem()

    assert banking_system.transfer_money("user123", "user456", 200, "regular") is False

    output = capsys.readouterr().out
    assert "Sender not authenticated." in output


def test_banking_system_transfer_supports_express_and_scheduled(capsys):
    banking_system = BankingSystem()

    assert banking_system.authenticate("user123", "pass123") is True
    assert banking_system.transfer_money("user123", "user456", 200, "express") is True
    assert banking_system.transfer_money("user123", "user456", 200, "scheduled") is True

    output = capsys.readouterr().out
    assert "Money transfer of $200 (express transfer)" in output
    assert "Money transfer of $200 (scheduled transfer)" in output


def test_banking_system_transfer_invalid_type_and_insufficient_funds(capsys):
    banking_system = BankingSystem()

    assert banking_system.authenticate("user123", "pass123") is True
    assert banking_system.transfer_money("user123", "user456", 200, "invalid") is False
    assert banking_system.transfer_money("user123", "user456", 1000, "regular") is False

    output = capsys.readouterr().out
    assert "Invalid transaction type." in output
    assert "Insufficient funds." in output


def test_product_view_and_shopping_cart_checkout_integration(capsys):
    cart = ShoppingCart()
    notebook = Product("Notebook", 20)
    pen = Product("Pen", 5)

    assert notebook.view_product() == "The product Notebook has a price of 20"

    cart.add_product(notebook, 2)
    cart.add_product(pen, 3)
    cart.view_cart()
    cart.checkout()

    output = capsys.readouterr().out
    assert "The product Notebook has a price of 20" in output
    assert "2 x Notebook - $40" in output
    assert "3 x Pen - $15" in output
    assert "Total: $55" in output
    assert "Checkout completed. Thank you for shopping!" in output


def test_shopping_cart_accumulates_quantity_for_same_product():
    cart = ShoppingCart()
    notebook = Product("Notebook", 20)

    cart.add_product(notebook, 1)
    cart.add_product(notebook, 2)

    assert cart.items == [{"product": notebook, "quantity": 3}]


def test_shopping_cart_remove_product_reduces_quantity_then_removes_item():
    cart = ShoppingCart()
    notebook = Product("Notebook", 20)

    cart.add_product(notebook, 3)
    cart.remove_product(notebook, 1)

    assert cart.items == [{"product": notebook, "quantity": 2}]

    cart.remove_product(notebook, 2)

    assert cart.items == []


def test_book_store_add_and_display_books_integration(capsys):
    store = BookStore()
    book = Book("Clean Code", "Robert C. Martin", 35.5, 4)

    store.add_book(book)
    store.display_books()

    output = capsys.readouterr().out
    assert "Book 'Clean Code' added to the store." in output
    assert "Books available in the store:" in output
    assert "Title: Clean Code" in output
    assert "Author: Robert C. Martin" in output
    assert "Price: $35.5" in output
    assert "Quantity: 4" in output


def test_book_store_display_books_when_empty(capsys):
    store = BookStore()

    store.display_books()

    output = capsys.readouterr().out
    assert "No books in the store." in output


def test_book_store_search_book_case_insensitive_with_multiple_matches(capsys):
    store = BookStore()
    first_book = Book("Dune", "Frank Herbert", 25, 3)
    second_book = Book("DUNE", "Another Author", 30, 1)

    store.add_book(first_book)
    store.add_book(second_book)
    store.search_book("dune")

    output = capsys.readouterr().out
    assert "Found 2 book(s) with title 'dune':" in output
    assert "Title: Dune" in output
    assert "Title: DUNE" in output


def test_book_store_search_book_not_found(capsys):
    store = BookStore()
    store.add_book(Book("1984", "George Orwell", 19.99, 5))

    store.search_book("Brave New World")

    output = capsys.readouterr().out
    assert "No book found with title 'Brave New World'." in output


def test_book_store_main_exit_immediately(monkeypatch, capsys):
    responses = iter(["4"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    main()

    output = capsys.readouterr().out
    assert "1. Display all books" in output
    assert "Exiting..." in output


def test_book_store_main_invalid_choice_then_exit(monkeypatch, capsys):
    responses = iter(["9", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    main()

    output = capsys.readouterr().out
    assert "Invalid choice. Please try again." in output
    assert "Exiting..." in output


def test_book_store_main_add_display_search_and_exit(monkeypatch, capsys):
    responses = iter(
        [
            "3",
            "Clean Architecture",
            "Robert C. Martin",
            "45.0",
            "2",
            "1",
            "2",
            "clean architecture",
            "4",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    main()

    output = capsys.readouterr().out
    assert "Book 'Clean Architecture' added to the store." in output
    assert "Books available in the store:" in output
    assert "Title: Clean Architecture" in output
    assert "Author: Robert C. Martin" in output
    assert "Price: $45.0" in output
    assert "Quantity: 2" in output
    assert "Found 1 book(s) with title 'clean architecture':" in output
    assert "Exiting..." in output
