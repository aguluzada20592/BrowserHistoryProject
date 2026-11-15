from advanced_history import AdvancedBrowserHistory
browser = AdvancedBrowserHistory("google.com", max_capacity=3)
browser.visit("youtube.com")
browser.visit("github.com")
browser.visit("stackoverflow.com")
browser.display_history()
print("Current:", browser.current_page())
print("Back 100:", browser.back(100))