from browser_history import BrowserHistory

browser = BrowserHistory("google.com")

browser.visit("youtube.com")
browser.visit("github.com")

browser.display_history()

print("Back:", browser.back(1))
print("Back again:", browser.back(1))
print("Forward:", browser.forward(1))

print("Current page:", browser.current_page())

browser.visit("stackoverflow.com")

browser.display_history()