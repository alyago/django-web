from django import forms

class JobApplicationForm(forms.Form):
    """
    Job application Django form for mobile apply.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form by dynamically adding any desired fields based
        upon the "questions" argument.

        Args:
            questions: a list of questions in JSON format
        """
        # Assign a local variable to the "questions" argument, and remove it
        # from the argument list (it needs to be removed since the base class
        # will fail since it doesn't know what the argument means).
        #
        questions = kwargs['questions']
        del kwargs['questions']

        forms.Form.__init__(self, *args, **kwargs)

        for question in questions:
            field_id = str(question['id'])
            field_is_required = question['is_required']
            field_answer = question.get('answer')
            field_label = question['label']

            # TODO: Use translation strings here
            field_kwargs = {
                'error_messages': {
                    'required': 'This field is required.'
                },
                'initial': field_answer,
                'label': field_label,
                'required': bool(field_is_required),
            }

            if question['input_type'] == 'SELECT':
                field_type = forms.ChoiceField
                field_kwargs['choices'] = [(str(index), value)
                    for (index, value) in enumerate(question['input_options'])]

            elif question['input_type'] == 'FILE':
                field_type = forms.FileField

                # TODO: Use translation strings here
                field_kwargs['error_messages'].update({
                    'invalid': 'File is invalid.',
                    'missing': 'File is missing.',
                    'empty': 'File is empty.',
                })
            else:
                field_type = forms.CharField

            self.fields[field_id] = field_type(**field_kwargs)

    def get_answers(self):
        """
        Gets the completed list of answers.

        Returns:
            A dict that maps the question id to the answer.
        """
        return { field.id_for_label[3:] : field.data for field in self }
