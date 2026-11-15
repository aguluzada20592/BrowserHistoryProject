
import unittest
import os
import tempfile

from advanced_history import AdvancedBrowserHistory


class TestBrowserHistory(unittest.TestCase):

    def test_homepage(self):
        browser = AdvancedBrowserHistory("google.com")
        self.assertEqual(browser.current_page()["url"], "google.com")
        self.assertEqual(browser.size, 1)

    def test_visit(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.visit("github.com")

        self.assertEqual(browser.current_page()["url"], "github.com")
        self.assertEqual(browser.size, 3)

    def test_back_forward(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.visit("github.com")

        self.assertEqual(browser.back(1), "youtube.com")
        self.assertEqual(browser.forward(1), "github.com")

    def test_back_boundary(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")

        self.assertEqual(browser.back(100), "google.com")

    def test_forward_boundary(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.back(1)

        self.assertEqual(browser.forward(100), "youtube.com")

    def test_branching(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.visit("github.com")
        browser.back(1)
        browser.visit("stackoverflow.com")

        self.assertEqual(browser.size, 3)
        self.assertEqual(browser.current_page()["url"], "stackoverflow.com")
        self.assertIsNone(browser.current.next)

    def test_capacity(self):
        browser = AdvancedBrowserHistory("home.com", max_capacity=3)

        for i in range(5):
            browser.visit(f"page{i}.com")

        self.assertEqual(browser.size, 3)
        self.assertEqual(browser.head.url, "page2.com")
        self.assertEqual(browser.current.url, "page4.com")

    def test_delete_url(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.visit("github.com")

        self.assertTrue(browser.delete_url("youtube.com"))
        self.assertEqual(browser.size, 2)
        self.assertEqual(browser.head.next.url, "github.com")

    def test_restore(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.visit("github.com")

        browser.delete_url("youtube.com")
        self.assertTrue(browser.restore())

        self.assertEqual(browser.size, 3)
        self.assertEqual(browser.head.next.url, "youtube.com")

    def test_restore_stack_lifo(self):
        browser = AdvancedBrowserHistory("a.com")
        browser.visit("b.com")
        browser.visit("c.com")

        browser.delete_url("b.com")
        browser.delete_url("c.com")

        self.assertTrue(browser.restore())
        self.assertEqual(browser.tail.url, "c.com")

        self.assertTrue(browser.restore())
        self.assertEqual(browser.head.next.url, "b.com")

    def test_delete_all(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")

        browser.delete_history()

        self.assertEqual(browser.size, 0)
        self.assertIsNone(browser.head)
        self.assertIsNone(browser.current)
        self.assertIsNone(browser.tail)

    def test_visit_after_delete_all(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.delete_history()
        browser.visit("new.com")

        self.assertEqual(browser.current.url, "new.com")
        self.assertEqual(browser.size, 1)

    def test_import_export(self):
        browser = AdvancedBrowserHistory("google.com")
        browser.visit("youtube.com")
        browser.visit("github.com")
        browser.back(1)

        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "history.txt")
            browser.export_history(filename)

            loaded = AdvancedBrowserHistory("temporary.com")
            loaded.import_history(filename)

            self.assertEqual(loaded.size, 3)
            self.assertEqual(loaded.current.url, "youtube.com")
            self.assertEqual(loaded.tail.url, "github.com")

    def test_import_capacity(self):
        browser = AdvancedBrowserHistory("home.com", max_capacity=3)

        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "large_history.txt")

            with open(filename, "w", encoding="utf-8") as file:
                file.write("CURRENT_POSITION:4\n")
                for i in range(6):
                    file.write(f"page{i}.com\n")

            browser.import_history(filename)

            self.assertEqual(browser.size, 3)
            self.assertEqual(browser.head.url, "page3.com")
            self.assertEqual(browser.current.url, "page3.com")

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            AdvancedBrowserHistory("google.com", max_capacity=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
