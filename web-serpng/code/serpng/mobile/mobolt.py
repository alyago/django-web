import json
import os.path
import requests
import traceback
from django.conf import settings

class MoboltClient(object):
    """
    Mobolt API wrapper
    """
    def __init__(self, api_key, logger):
        """
        Initializes the MoboltClient
        """
        self.api_key = api_key
        self.logger = logger
        self.wta_endpoint = 'https://{host}:{port}/{client_id}/wta' \
            '?key={api_key}&sync=true'.format(
                host=settings.MOBOLT_API_HOST,
                port=settings.MOBOLT_API_PORT,
                client_id=settings.MOBOLT_API_CLIENT_ID,
                api_key=settings.MOBOLT_API_KEY)

        self.upload_endpoint = 'https://{host}:{port}/{client_id}/uploadfile' \
            '?key={api_key}&sync=true'.format(
                host=settings.MOBOLT_API_HOST,
                port=settings.MOBOLT_API_PORT,
                client_id=settings.MOBOLT_API_CLIENT_ID,
                api_key=settings.MOBOLT_API_KEY)

    def submit_application(self, mobolt_job_id, answers):
        """
        Submits a job application.

        Args:
            mobolt_job_id: Mobolt ID of the job being applied to
            answers: a dict containing a question ID to answer mapping

        Returns:
            True on success, otherwise False

        Raises:
            IOError: A network error occurred while submitting the form
        """
        try:
            data = {
                'id': mobolt_job_id,
                'answers': answers,
            }

            self.logger.debug('Calling Mobolt WTA endpoint with payload: {0}' \
                .format(data))

            response = requests.post(
                self.wta_endpoint,
                data=json.dumps(data),
                headers={ 'Content-Type': 'application/json' },
                verify=False)

            self.logger.debug('Mobolt WTA endpoint responded with status code '
                '{0} and a payload of: {1}'.format(response.status_code, response.text))

            if response.status_code == 200:
                return True
            else:
                return False
        except:
            msg = 'Error attempting to submit an application to Mobolt:\n{0}' \
                .format(traceback.format_exc())

            self.logger.error(msg)
            raise IOError(msg)

    def upload_file(self, filename, contents):
        """
        Synchronously uploads a file (e.g., a resume or cover letter) to Mobolt.

        Args:
            filename: the name of the file
            contents: the contents of the file

        Returns:
            The Mobolt file ID

        Raises:
            IOError: A network or HTTP error occurred while uploading the file.
        """
        # Figure out MIME type and subtype, so that we can write the Content-Type header.
        #
        file_extension = os.path.splitext(filename)[1][1:]
        mime_type = settings.EXTENSION_TO_MIME_MAPPING.get(file_extension)
        if not mime_type:
            raise ValueError('Unsupported file type.')

        try:
            response = requests.post(
                self.upload_endpoint,
                files={
                    'file': (
                        filename,
                        contents,
                        mime_type,
                    )
                },
                headers={
                    'Accept': 'application/json',
                },
                verify=False)

            self.logger.debug('Mobolt file upload endpoint responded with status code '
                '{0} and a payload of: {1}'.format(response.status_code, response.text))

            if response.status_code == 200:
                self.logger.info('File was successfully uploaded to Mobolt.')

                # On success, response looks like this:
                #
                # { "<filename>" : "<mobolt id>" }
                #
                return response.json()[filename]
            else:
                msg = 'File upload to Mobolt failed with response {0}.'.format(
                    response.status_code)

                self.logger.error(msg)
                raise IOError(msg)

        except:
            msg = 'Encountered an error while attempting to upload a file to Mobolt:\n{0}' \
                .format(traceback.format_exc())

            self.logger.error(msg)
            raise IOError(msg)
