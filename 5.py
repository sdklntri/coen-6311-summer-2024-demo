# test_subscription.py
import unittest

# Example functions to be tested
def create_subscription_form():
    return "Subscription form created"

def send_verification_email(email):
    if "@" in email:
        return "Verification email sent"
    else:
        return "Invalid email address"

# Unit tests
class TestSubscriptionForm(unittest.TestCase):

    def test_create_subscription_form(self):
        self.assertEqual(create_subscription_form(), "Subscription form created")

    def test_send_verification_email_valid(self):
        self.assertEqual(send_verification_email("user@example.com"), "Verification email sent")

    def test_send_verification_email_invalid(self):
        self.assertEqual(send_verification_email("userexample.com"), "Invalid email address")

if __name__ == '__main__':
    unittest.main()

