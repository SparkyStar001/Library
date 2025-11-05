# Library Subscription System

**Brief**

A simple command-line library subscription and book-rental system written in Python. It manages reader subscriptions (daily/weekly/monthly/yearly), shows an available book list, processes borrow requests, and performs payments against a local `store.json` file (which stores account data and hashed PINs).

> The code you provided is unchanged — this README only explains how to set up test data and run the program.

---

## Project structure (important files)

* `main.py` — your main program (the script you shared).
* `02_Management.json` — subscription records (created by the program).
* `03_Books.json` — book catalog (you can populate this with sample books below).
* `Rents.json` — records of borrowed books (created by the program).
* `store.json` — local accounts file used for payments (must contain bcrypt-hashed PINs).

---

## Quick start

1. Clone the repo or copy files into a folder.
2. Create a Python virtual environment and install the required dependency:

```bash
python -m venv venv
# activate venv (platform dependent)
pip install bcrypt
```

3. Prepare the sample data (see next sections).
4. Run the script:

```bash
python main.py
```

When prompted, choose `A` for admin workflows (add/clear books) or `R` for reader workflows (subscribe, view, and borrow).

---

## Sample books

Save the following JSON array into `03_Books.json` for immediate testing:

```json
[
    {"title": "A Short History of Nearly Everything", "author": "Bill Bryson", "price": "350"},
    {"title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "price": "299"},
    {"title": "Fundamentals of Physics", "author": "Halliday & Resnick", "price": "650"},
    {"title": "Introduction to Algorithms", "author": "Cormen, Leiserson, Rivest, Stein", "price": "1200"}
]
```

The `price` field is used by the borrow routine; the rent cost is calculated as 20% of the price per day.

---

## Sample bank account (for testing)

**Important:** the program expects `store.json` to store account objects whose `Pin` value is a bcrypt hash (string). To create a test account with PIN `237899`, run the small helper script below which builds a `store.json` file containing a single test account.

Create and run a file named `create_test_account.py` with the following contents (run this inside the same project folder):

```python
import json
import bcrypt
from datetime import datetime

# Change these values if you want different test credentials
account_number = 12345678
plain_pin = "237899"
initial_balance = 5000  # ₹

# Generate bcrypt hash of the PIN
hashed = bcrypt.hashpw(plain_pin.encode(), bcrypt.gensalt()).decode()

account = {
    "account_number": str(account_number),
    "Pin": hashed,
    "balance": initial_balance,
    "transactions": [
        {
            "type": "Deposit",
            "amount": initial_balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
}

with open("store.json", "w") as f:
    json.dump([account], f, indent=4)

print("store.json created with test account:", account_number)
print("Test PIN (plain): 237899 — hashed and stored in store.json")
```

Run:

```bash
python create_test_account.py
```

This writes `store.json` with one account. Use `account_number = 12345678` and `PIN = 237899` when the program prompts for payment.

---

## If you prefer a ready-made account or alternate setup

If you already have (or want to create) account-management logic in a separate repository, you can use the repository named **`Bank`** (mentioned earlier) to generate accounts and then copy the produced `store.json` into this library project. The library script expects the same JSON structure (accounts list with `account_number`, `Pin`, `balance`, `transactions`).

---

## Security & GitHub guidance

* **Do not commit real account data** (actual users' PINs or balances) to GitHub.
* Add `store.json` to `.gitignore` so your private test/real accounts are not pushed:

```
store.json
02_Management.json
Rents.json
```

* Keep only `03_Books.json` with sample data (or `03_Books.example.json`) in the repository.

---

## Tips for testing

* Use the `create_test_account.py` helper above to generate test credentials.
* Use the provided `03_Books.json` sample to test borrowing and rent calculation.
* If the program raises bcrypt errors when checking PINs, ensure you installed `bcrypt` in the same Python environment where you run `main.py`.

---

## Troubleshooting

* **`store.json` not found**: copy the generated `store.json` into the same folder as the main script, or update file paths in code.
* **Invalid JSON errors**: open the referenced JSON file and validate its structure (e.g., via an online JSON validator or `python -m json.tool file.json`).

---

## License & contribution

This project is provided as-is for learning and testing. You may modify it for your own use. If you want help extending features (returning books, subscription time display, or automated tests), open an issue or a PR in the repository.

---

If you want, I can also (pick one):

* create the `create_test_account.py` file for you inside the repo, or
* generate a `03_Books.json` sample file and a `.gitignore` entry.

Tell me which one to add next.
