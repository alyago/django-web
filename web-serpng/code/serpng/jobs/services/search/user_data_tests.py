"""User Data Tests."""
from django.test import TestCase

import user_data


# JSON responses from the bridge to be used in the tests.
JSON_RESPONSE_WITH_NO_USER_DATA = {
    'abc': 'I am not user data'
}

JSON_RESPONSE_WITH_GOOD_USER_DATA = {
    'user_data': {
        'recent_searches': ['rs1', 'rs2'],
        'user_email': 'meow@cat.com',
        'saved_jobs': {
            'job1': {'comment': 'abc'},
            'job2': {'comment': 'def'}
        }
    }
}

JSON_RESPONSE_WITH_BAD_USER_DATA = {
    'user_data': {}
}

JSON_RESPONSE_WITH_EMPTY_ARRAY_SAVED_JOBS = {
    'user_data': {
        'saved_jobs': []
    }
}

JSON_RESPONSE_WITH_NULL_COMMENT_SAVED_JOB = {
    'user_data': {
        'saved_jobs': {
            'job1': {'comment': 'abc'},
            'job2': {'comment': None}
        }
    }
}


# Tests
class UserDataTestCase(TestCase):
    """User Data TestCase."""
    # pylint: disable=R0904
    def test_no_user_data_in_json_response(self):
        """Default values should be correct when there is no user data."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_NO_USER_DATA)

        self.assertIsNone(test_user_data.recent_searches)
        self.assertIsNone(test_user_data.user_email)
        self.assertEqual(test_user_data.saved_jobs, {})

    def test_good_recent_searches(self):
        """Attribute 'recent_searches' should be correctly populated."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_GOOD_USER_DATA)
        self.assertEqual(test_user_data.recent_searches[1], 'rs2')

    def test_good_user_email(self):
        """Attribute 'user_email' should be correctly populated."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_GOOD_USER_DATA)
        self.assertEqual(test_user_data.user_email, 'meow@cat.com')

    def test_good_saved_jobs(self):
        """Attribute 'saved_jobs' should be correctly populated."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_GOOD_USER_DATA)
        self.assertEqual(test_user_data.saved_jobs['job1'], 'abc')

    def test_no_recent_searches(self):
        """Attribute 'recent_searches' should have good default value when user_data is empty."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_BAD_USER_DATA)
        self.assertIsNone(test_user_data.recent_searches)

    def test_no_user_email(self):
        """Attribute 'user_email' should have good default value when user_data is empty."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_BAD_USER_DATA)
        self.assertIsNone(test_user_data.user_email)

    def test_no_saved_jobs(self):
        """Attribute 'saved_jobs' should have good default value when user_data is empty."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_BAD_USER_DATA)
        self.assertEqual(test_user_data.saved_jobs, {})

    def test_empty_array_saved_jobs(self):
        """Attribute 'saved_jobs' should have good default value when saved_jobs is empty."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_EMPTY_ARRAY_SAVED_JOBS)
        self.assertEqual(test_user_data.saved_jobs, {})

    def test_null_comment_saved_job(self):
        """Attribute 'saved_jobs' should convert null comments to empty strings."""
        test_user_data = user_data.UserData(JSON_RESPONSE_WITH_NULL_COMMENT_SAVED_JOB)
        self.assertEqual(test_user_data.saved_jobs['job2'], '')
