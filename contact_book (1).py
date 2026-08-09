import os

FILE_NAME = "contacts.txt"


# Create the file if it doesn't exist
if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()


def menu():
    print("\n" + "=" * 40)
    print("        CONTACT BOOK")
    print("=" * 40)
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Exit")
    print("=" * 40)


def add_contact():
    print("\n----- Add Contact -----")

    name = input("Enter Name : ").strip()
    phone = input("Enter Phone Number : ").strip()
    email = input("Enter Email : ").strip()

    # Check duplicate phone number
    with open(FILE_NAME, "r") as file:
        for line in file:
            data = line.strip().split(",")

            if len(data) == 3:
                if phone == data[1]:
                    print("\nContact with this phone number already exists!")
                    return

    with open(FILE_NAME, "a") as file:
        file.write(f"{name},{phone},{email}\n")

    print("\nContact Added Successfully!")


def view_contacts():
    print("\n----- Contact List -----")

    with open(FILE_NAME, "r") as file:
        contacts = file.readlines()

        if not contacts:
            print("No Contacts Found.")
            return

        for i, contact in enumerate(contacts, start=1):
            name, phone, email = contact.strip().split(",")

            print(f"\nContact {i}")
            print("-" * 25)
            print(f"Name  : {name}")
            print(f"Phone : {phone}")
            print(f"Email : {email}")


def search_contact():
    print("\n----- Search Contact -----")

    search = input("Enter Name : ").strip().lower()

    found = False

    with open(FILE_NAME, "r") as file:
        for contact in file:
            name, phone, email = contact.strip().split(",")

            if search == name.lower():

                print("\nContact Found")
                print("-" * 25)
                print(f"Name  : {name}")
                print(f"Phone : {phone}")
                print(f"Email : {email}")

                found = True
                break

    if not found:
        print("\nContact Not Found.")


def main():

    while True:

        menu()

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            view_contacts()

        elif choice == "3":
            search_contact()

        elif choice == "4":
            print("\nThank you for using Contact Book!")
            break

        else:
            print("\nInvalid Choice! Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()