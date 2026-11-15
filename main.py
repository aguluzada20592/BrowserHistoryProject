
from advanced_history import AdvancedBrowserHistory


def show_menu():
    print("\n========== BROWSER HISTORY MANAGER ==========")
    print("1. Visit a new website")
    print("2. Go Back")
    print("3. Go Forward")
    print("4. Show Current Page")
    print("5. Display Full History")
    print("6. Delete a URL")
    print("7. Restore Deleted URL")
    print("8. Delete All History")
    print("9. Export History")
    print("10. Import History")
    print("0. Exit")
    print("=============================================")


def main():
    print("Welcome to Browser History Management System!")

    homepage = input("Enter homepage URL: ").strip()

    if not homepage:
        homepage = "https://google.com"

    browser = AdvancedBrowserHistory(homepage)

    while True:
        show_menu()
        choice = input("Choose an option (0-10): ").strip()

        if choice == "1":
            url = input("Enter website URL: ").strip()

            if url:
                browser.visit(url)
                print("Visited:", url)
            else:
                print("URL cannot be empty.")

        elif choice == "2":
            try:
                steps = int(input("How many steps back? "))
                print("Current page:", browser.back(steps))
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            try:
                steps = int(input("How many steps forward? "))
                print("Current page:", browser.forward(steps))
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            page = browser.current_page()

            if page is None:
                print("No active page.")
            else:
                print("Current page:", page["url"])
                print("Position:", page["position"])
                print("Total pages:", page["total_pages"])

        elif choice == "5":
            browser.display_history()

        elif choice == "6":
            url = input("Enter URL to delete: ").strip()
            browser.delete_url(url)

        elif choice == "7":
            browser.restore()

        elif choice == "8":
            confirm = input(
                "Delete all history? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                browser.delete_history()
            else:
                print("Deletion cancelled.")

        elif choice == "9":
            filename = input(
                "Export filename (default: history.txt): "
            ).strip()

            if not filename:
                filename = "history.txt"

            browser.export_history(filename)

        elif choice == "10":
            filename = input(
                "Import filename (default: history.txt): "
            ).strip()

            if not filename:
                filename = "history.txt"

            browser.import_history(filename)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 0-10.")


if __name__ == "__main__":
    main()