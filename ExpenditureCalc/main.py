from pay import Pay
from datetime import datetime

def main():
    start_new_session = input("Start new session (Y/N)? ").strip().lower() == 'y'
    session = Pay(start_new_session=start_new_session)

    while True:
        print("\nOptions:")
        print("1. Add Item")
        print("2. Update Item")
        print("3. Delete Item")
        print("4. View Items")
        print("5. View Total Expenditure")
        print("6. Save and Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            item = input("Enter item name: ")
            category = input("Enter item category: ")
            price = float(input("Enter item price: "))
            date = input("Enter item date (YYYY-MM-DD, leave empty for today): ").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            session.addItem(item, category)
            session.addPrice(item, price)

        elif choice == '2':
            item = input("Enter item name to update: ")
            new_category = input("Enter new category (leave empty to skip): ").strip()
            new_price = input("Enter new price (leave empty to skip): ").strip()
            if new_category:
                session.updateCategory(item, new_category)
            if new_price:
                session.addPrice(item, float(new_price))

        elif choice == '3':
            item = input("Enter item name to delete: ")
            session.deleteItem(item)
        
        elif choice == '4':
            items = session.expenditures()
            print("Items:")
            for item, details in items.items():
                print(f"Item: {item}, Category: {details['category']}, Price: {details['price']}")
        
        elif choice == '5':
            total = session.calculateTotal()
            print(f"Total Expenditure: {total}")

        elif choice == '6':
            session.printAddedItemsToFile()
            session.close()
            print("Data saved. Exiting.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
