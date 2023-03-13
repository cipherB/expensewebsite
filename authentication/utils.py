"""Import libraries
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    """Token generator class

    Args:
        PasswordResetTokenGenerator (class): class library
    """
    def _make_hash_value(self, user, timestamp):
        """generate token using function 

        Args:
            user (object): user details
            timestamp (string): user registration timestamp

        Returns:
            string: returns a string containing a generated token
        """
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
