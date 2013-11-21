"""User Data."""


class UserData:
    """User Data Object."""
    def __init__(self, json_response):
        """
        Initialize attributes from the JSON response obtained from the bridge.

        Args:
            json_response: JSON response from bridge, decoded into a dictionary
                object.
        """
        user_data_from_bridge = json_response.get('user_data', {})

        self.recent_searches = user_data_from_bridge.get('recent_searches')
        self.user_email = user_data_from_bridge.get('user_email')

        # Saved jobs needs extra processing.
        saved_jobs = {}
        saved_jobs_from_bridge = user_data_from_bridge.get('saved_jobs')

        # When there are no saved jobs, the saved_jobs field is an empty array.
        # However, when there are saved jobs, the saved_jobs field is a dictionary.
        if saved_jobs_from_bridge and isinstance(saved_jobs_from_bridge, dict):
            # Do extra processing for saved job to convert null comments to
            # empty strings.
            for job_key, job_value in saved_jobs_from_bridge.iteritems():
                saved_jobs[job_key] = (
                    '' if job_value['comment'] is None
                    else job_value['comment'].encode('utf-8'))

        self.saved_jobs = saved_jobs
