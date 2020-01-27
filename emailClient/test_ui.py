from unittest import TestCase
from PyQt5.QtWidgets import QApplication
import unittest
import sys
import ui

app = QApplication(sys.argv)

class TestEmailClient(TestCase):
    def test_load(self):
        client = ui.EmailClient()
        # self.assertEqual(client.mail_list)



# if __name__ == '__main__':
#     unittest.main()
