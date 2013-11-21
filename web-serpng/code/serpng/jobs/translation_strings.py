""" Set of all strings used in SERP """
from django.utils.translation import ugettext_lazy as _

# pylint: disable=C0103
# Pylint wants this to be TRANSLATIONS since it's a constant.
translations = {
    #
    # Used in template file: base_email_alert_form.html (and many others).
    #

    # Translators: no comment.
    'OK_text': _("OK"),

    #
    # Used in template file: jobs_base.html
    #

    # Translators: This is the page title, letting the user know they are looking at search results from Simply Hired.
    'page_title_text': _("Job Search with Simply Hired"),

    #
    # Used in template file: bottom_footer.html
    #

    # Translators: This is a link to a page with information about jobs in various cities.
    'local_jobs_link_text': _("Local Jobs"),

    # Translators: This is a link to a page with information about salaries for various jobs.
    'job_salaries_link_text': _("Job Salaries"),

    # Translators: This is a link to a page with information about trends in employment and hiring.
    'job_trends_link_text': _("Job Trends"),

    # Translators: This is a link to the Simply Hired blog, which contains information about employment and hiring.
    'get_hired_blog_link_text': _("Simply Hired Blog"),

    # Translators: This is a link to a page containing information about how advertisers can post jobs on Simply Hired.
    'post_a_job_link_text': _("Post Jobs"),
    
    # Translators: This is a link to our home page
    'find_a_job_link_text': _("Find Jobs"),

    # Translators: This is a link to a page containing information about how advertisers can contact Simply Hired sales.
    'employer_solutions_link_text': _("Employer Solutions"),

    # Translators: This is a link to a page containing information about how web site publishers can contact Simply Hired sales.
    'publisher_solutions_link_text': _("Publisher Solutions"),

    # Translators: This is a link to a page where users can browse jobs by category.
    'browse_jobs_link_text': _("Browse Jobs"),

    # Translators: This is a link to the Simply Hired corporate page that contains information about Simply Hired.
    'about_simply_hired_link_text': _("About Simply Hired"),

    # Translators: This is a link to the Simply Hired support page.
    'help_link_text': _("Help"),

    # Translators: This is a link to a page where the user can upload his resume.
    'upload_resume_link_text': _("Upload Resume"),

    # Translators: This is a link to a page where the user can contact Simply Hired.
    'contact_us_link_text': _("Contact Us"),

    # Translators: This activates a drop-down menu that displays links to Simply Hired's international sites.
    'international_menu_text': _("International"),

    # Translators: This is a link to a page containing information about Simply Hired's privacy policy.
    'privacy_link_text': _("Privacy"),

    # Translators: This is a link to a page containing information about Simply Hired's terms of service.
    'terms_link_text': _("Terms"),

    # Translators: This is the text that accompanies Simply Hired's copyright notice.
    'all_rights_reserved_text': _("All Rights Reserved"),

    # Translators: This a link to Simply Hired's company pages
    'company_page_text': _("Companies"),

    # Translators: This is a link to Simply Hired's "Evergreen Content" (aka articles)
    'articles_text': _("Job Search Advice"),

    # Translators: This is a link to Simply Hired's Community Forums (aka AskBot)
    'askbot_text':_("Q&A"),

    #
    # Used in template files: content_center_email_alert_form.html
    #                         content_left_email_alert_form.html
    #

    # Translators: This text sits right above a form in which users can submit their email addresses.
    'email_alert_form_cta_text': _("Email jobs like this to me"),

    #
    # Used in template file: content_center_pagination.html
    #

    # Translators: This is an abbreviation for "Previous", and links to the previous page of search results.
    'previous_link_text': _("Prev"),

    # Translators: This links to the next page of search results.
    'next_link_text': _("Next"),

    #
    # Used in template file: content_center_results.html
    #

    # Translators: This is the text that shows when a job is newly posted
    'new_job_text': _("NEW"),

    # Translators: This is the text that follows the x days ago in the job entry
    # that tells where the job is from
    'job_from_text': _("from"),

    # Translators: This is the text that says if the job was found from multiple locations
    'multiple_location_text': _("location"),

    # Translators: This is the text that says if the job was found from multiple locations
    'multiple_locations_text': _("locations"),

    # Translators: This is the text of a link next to a short description of a job which, when clicked,
    # allows a user to save the job for viewing later.
    'save_text': _("Save"),

    # Translators: This is a text next to a short description of a job which indicates that the job
    # has been saved for later viewing.
    'saved_text': _("Saved"),

    # Translators: This is the text of a link next to a short description of a job which, when clicked,
    # allows a user to share the job with other people, via email, Facebook, Twitter, or LinkedIn.
    'share_text': _("Share"),

    # Translators: This is the text of a link next to a short description of a job which, when clicked,
    # allows a user to hide the job from the list of jobs displayed.
    'hide_text': _("Hide"),

    # Translators: This is the text of a link next to a short description of a job which, when clicked,
    # allows a user to report problems with the job to Simply Hired.
    'report_text': _("Report"),

    # Translators: This is the text of a link next to a short description of a job which, when clicked,
    # allows a user to view job research tools associated with the job.
    'job_tools_text': _("Job Tools"),

    # Translators: This is the text that immediately precedes "My Jobs", which is a link that a user
    # can click to access a page where all his saved jobs are displayed.  The whole line reads:
    # "Saved To My Jobs".
    'saved_to_text': _("Saved To"),

    # Translators: This is the text that immediately follows "Saved To". "My Jobs" is a link that a user
    # can click to access a page where all his saved jobs are displayed.  The whole line reads:
    # "Saved To My Jobs".
    'my_jobs_text': _("My Jobs"),

    # Translators: This is the text that sits above a box in which the user can edit his notes for
    # a saved job.
    'edit_notes_text': _("Edit Notes:"),

    # Translators: This is the text of a link that, when clicked, shows a box in which the user
    # can add notes for a saved job.
    'add_notes_text': _("Add Notes"),

    # Translators: This is the title of a widget that displays a form that allows the user to
    # email information about a job to a friend.
    'email_text': _("Email"),

    # Translators: This is the text of a link under a job description. When this link is clicked,
    # all jobs from the company associated with the job described above the link will be removed
    # from the list of jobs displayed.
    'hide_jobs_company_text': _("Hide all jobs at this company"),

    # Translators: This is the text of a link under a job description. When this link is clicked,
    # all jobs from the website associated with the job described above the link will be removed
    # from the list of jobs displayed.
    'hide_jobs_site_text': _("Hide all jobs from this site"),

    # Translators: This is the text of a link under a job description. When this link is clicked,
    # the user is taken to a page where he can choose to view previously hidden jobs.
    'view_hidden_jobs_text': _("View all hidden companies and sites."),

    # Translators: Text that appears when the user attempts to hide a job from the list of
    # jobs being displayed.
    'tired_of_jobs_text': _("Tired of seeing jobs from this company or website?"),

    # Translators: Link that takes the user to an account sign-in page.
    'sign_in_link_text': _("Sign in"),

    # Translators: This indicates a choice between alternatives.
    'or_text': _("or"),

    # Translators: Link that takes the user to an account creation page.
    'create_account_link_text': _("create a free account"),

    # Translators: Text that appears when the user attempts to hide a job from the list of
    # jobs being displayed, but has not logged in yet. The full sentence reads:
    # "Sign in or create a free accont to hide their jobs."
    'to_hide_jobs_text': _("to hide their jobs."),

    # Translators: Text that appears when the user attempts to report a problem with ajob
    # to Simply Hired.
    'report_this_job_text': _("Report this job"),

    # Translators: One of several options to choose from when reporting a problem with a job.
    'scam_spam_link_text': _("scam/spam"),

    # Translators: One of several options to choose from when reporting a problem with a job.
    'expired_link_text': _("expired"),

    # Translators: One of several options to choose from when reporting a problem with a job.
    'duplicate_link_text': _("duplicate"),

    # Translators: One of several options to choose from when reporting a problem with a job.
    'inaccurate_link_text': _("inaccurate"),

    # Translators: Summary of job title, employer name, and location (city) of job.
    'job_summary_text': _("Job Summary:"),

    # Translators: This text precedes a link that will take the user to a full description of the job.
    'also_found_at_text': _("Also found at:"),

    # Translators: These are links to information related to the job, useful for the user's research
    # on the job.
    'research_tools_text': _("Research Tools:"),

    # Translators: These are links to information related to the job, useful for the user's research
    # on the job.
    'similar_searches_text': _("Similar Searches:"),

    #
    # Used in template file: content_error.html
    #

    # Translators: "Personalized search" uses a users's resume to search for relevant jobs.
    'personalized_search_signin_heading_text': _("Personalized Search is Great, Isn't It?"),

    # Translators: This text asks the user to sign in to a Simply Hired account.
    # The full text is:
    # Just one catch. You need to sign in to your Simply Hired account first,
    # so we can show you jobs relevant just to you.
    # And not to that guy next to you with the great hair.
    'need_to_sign_in_text': _("Just one catch. You need to "),

    # Translators: This text ask the user to sign in to a Simply Hired account.
    # The full text is:
    # Just one catch. You need to sign in to your Simply Hired account first,
    # so we can show you jobs relevant just to you.
    # And not to that guy next to you with the great hair.
    'sign_in_cta_text': _("sign in to your Simply Hired account"),

    # Translators: This text ask the user to sign in to a Simply Hired account.
    # The full text is:
    # Just one catch. You need to sign in to your Simply Hired account first,
    # so we can show you jobs relevant just to you.
    # And not to that guy next to you with the great hair.
    'sign_in_cta_reason_text': _(" first, so we can show you jobs relevant just to you."),

    # Translators: This text ask the user to sign in to a Simply Hired account.
    # The full text is:
    # Just one catch. You need to sign in to your Simply Hired account first,
    # so we can show you jobs relevant just to you.
    # And not to that guy next to you with the great hair.
    'sign_in_cta_humor_text': _("And not to that guy next to you with the great hair."),

    # Translators: This text appears on a button that, when clicked, takes the user to a sign-in page.
    'sign_in_now_text': _("Sign In Now"),

    # Translators: This is part of a text that asks the user to personalize his search experience
    # by uploading a resume.
    # The full text is:
    # Stumble here by accident? No problem! Now that you're here, why not give that personalized search a try? Choosing keywords is hard, we know.
    # Why not give our secret sauce a try? Get started by uploading your resume.
    'personalized_search_upload_resume_heading_text': _("Stumble here by accident?"),

    # Translators: This is part of a text that asks the user to personalize his search experience
    # by uploading a resume.
    # The full text is:
    # Stumble here by accident? No problem! Now that you're here, why not give that personalized search a try? Choosing keywords is hard, we know.
    # Why not give our secret sauce a try? Get started by uploading your resume.
    'personalization_search_upload_resume_cta_text': _('No problem! Now that you\'re here, why not give that personalized search a try? Choosing keywords is hard, we know.'),

    # Translators: This is part of a text that asks the user to personalize his search experience
    # by uploading a resume.
    # The full text is:
    # Stumble here by accident? No problem! Now that you're here, why not give that personalized search a try? Choosing keywords is hard, we know.
    # Why not give our secret sauce a try? Get started by uploading your resume.
    'personalization_search_upload_resume_cta_reason_text': _("Why not give our secret sauce a try?"),

    # Translators: This is part of a text that asks the user to personalize his search experience
    # by uploading a resume.
    # The full text is:
    # Stumble here by accident? No problem! Now that you're here, why not give that personalized search a try? Choosing keywords is hard, we know.
    # Why not give our secret sauce a try? Get started by uploading your resume.
    'personalization_search_upload_resume_get_started_text': _("Get started by "),

    # Translators: This is part of a text that asks the user to personalize his search experience
    # by uploading a resume.
    # The full text is:
    # Stumble here by accident? No problem! Now that you're here, why not give that personalized search a try? Choosing keywords is hard, we know.
    # Why not give our secret sauce a try? Get started by uploading your resume.
    'personalization_search_upload_resume_link_text': _("uploading your resume."),

    # Translators: This is a heading above job categories.
    'find_by_category_heading_text': _("Find Jobs by Category"),

    # Translators: This is a link that takes a user to a page with job categories.
    'browse_job_listings_text': _("Browse Job Listings"),

    #
    # Used in template file: content_left_filters.html
    #

    # Translators: This describes a toggle switch which, when clicked, will clear all
    # applied filters (to apply a filter to job search
    # results is to view only jobs that meet certain criteria).
    'clear_all_filters_text': _("Clear all"),

    # Translators: This describes a toggle switch which, when clicked, will display more filters
    # that the user can apply to filter job search results (to apply a filter to job search
    # results is to view only jobs that meet certain criteria).
    'more_filters_text': _("More Filters"),

    # Translators: This describes a toggle switch which, when clicked, will display more filters
    # that the user can apply to filter job search results (to apply a filter to job search
    # results is to view only jobs that meet certain criteria).
    'filters_text': _("Filters"),

    #
    # Used in template file: content_left_filters_list.html
    #

    # Translators: This describes a switch that is next to an applied filter. Clicking the
    # switch clears the applied filter (to apply a filter to job search
    # results is to view only jobs that meet certain criteria).
    'clear_filter_text': _("Clear"),

    # Translators: This describes a toggle switch which, when clicked, will allow the user
    # to see more filters that he can apply (to apply a filter to job search
    # results is to view only jobs that meet certain criteria).
    'see_more_filters_text': _("See more"),

    #
    # Used in template file: content_left_save_search_link.html
    #

    # Translators: This describes a link that takes the user to a page where he can view
    # previously saved job searches.
    'see_all_saved_searches_text': _("See all saved searches"),

    # Translators: This describes switch that, when clicked, will save the currently active
    # job search to the user's account.
    'save_this_search_text': _("Save this search"),

    #
    # Used in template file: content_left_sort.html
    #

    # Translators: This label describes two radio buttons that, when clicked, display the
    # job search results in different kinds of sorted order.
    'sort_by_text': _("Sort by"),

    # Translators: This label is next to a radio button that, when clicked, displays a page
    # where the job search results are sorted in order of relevance to the search keywords.
    'sort_by_relevance_radio_button_text': _("Relevance"),

    # Translators: This label is next to a radio button that, when clicked, displays a page
    # where the job search results are sorted in order of date (newest jobs displayed first).
    'sort_by_date_radio_button_text': _("Date"),

    #
    # Used in template file: content_right_wdik.html
    #

    # Translators: This label describes a radio button that, when clicked, will allow the user
    # to sign in with LinkedIn to see their LinkedIn connections.
    'connect_with_linkedin_text': _("Connect with LinkedIn"),

    # Translators: This label is next to a radio button that, if selected, indicates that
    # the user has turned on his LinkedIn connections.
    'linkedin_is_on_text': _("On"),

    # Translators: This label is next to a radio button that, if selected, indicates that
    # the user has NOT turned on his LinkedIn connections.
    'linkedin_is_off_text': _("Off"),

    # Translators: This is the heading for some help text that describes the features of
    # LinkedIn connections.
    'linkedin_tooltip_heading_text': _("Unleash the power of your professional network"),

    # Translators: This describes a reason that a user should turn on his LinkedIn connections.
    'linkedin_tooltip_para1_text': _("See all of your connections to interesting jobs"),

    # Translators: This describes a reason that a user should turn on his LinkedIn connections.
    'linkedin_tooltip_para2_text': _("Target companies where you have connections"),

    # Translators: This describes a reason that a user should turn on his LinkedIn connections.
    'linkedin_tooltip_para3_text': _("Make a personal connection when you apply"),

    #
    # Used in template file: content_survey.html
    #

    # Translators: This is a survey question that asks an user whether he is satisfied with his
    # job search results.
    'survey_question_text': _("Were you satisfied with these results?"),

    # Translators: no comment.
    'yes_text': _("Yes"),

    # Translators: no comment.
    'no_text': _("No"),

    # Translators: This is a thank you that is displayed after an user completes a survey.
    'survey_thank_you_text': _("Thank you for your feedback!"),

    #
    # Used in template file: email_alert_dialog.html
    #

    # Translators: This is the heading in a dialog that is displayed when the user has successfully
    # created an email alert (creating an email alert allows the user to receive daily email notifications of
    # new job openings).
    'email_alert_success_heading_text': _("Email Alert created!"),

    # Translators: This is the body in a dialog that is displayed when the user has successfully
    # created an email alert (creating an email alert allows the user to receive daily email notifications of
    # new job openings).
    'email_alert_success_body_text': _("Congratulations! You have just successfully created a job alert. Please check your inbox for new job matches."),

    # Translators: This precedes a link which, when clicked, takes the user to their personal email page.
    'email_alert_check_email_text': _("Check email at"),

    # Translators: This is a link that, when clicked, exits a dialog and re-displays a page with job search results.
    'return_to_search_results_link_text': _("Return to search results"),

    # Translators: This is informational text in the dialog that is displayed when the user has successfully
    # created an email alert (creating an email alert allows the user to receive daily email notifications of
    # new job openings).
    'email_alert_success_info_text': _("We'll send daily job notifications to"),

    #
    # Used in template file: email_alert_tooltip_content.html
    #

    # Translators: This is the heading for some help text that describes the features of
    # email alerts (creating an email alert allows the user to receive daily email notifications of
    # new job openings).
    'email_alert_tooltip_heading_text': _("Let Simply Hired do the work!"),

    # Translators: This describes a reason that a user should create an email alert (creating
    # an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_tooltip_para1_text': _("New jobs delivered daily"),

    # Translators: This describes a reason that a user should create an email alert (creating
    # an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_tooltip_para2_text': _("Only the jobs you want to see"),

    # Translators: This describes a reason that a user should create an email alert (creating
    # an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_tooltip_para3_text': _("Unsubscribe anytime"),

    #
    # Used in template file: save_search_dialog.html
    #

    # Translators: This is the heading in a dialog where the user can save a job search.
    'saving_search_text': _("Saving your search..."),

    # Translators: This is the text in a dialog in which the user had just saved a job search.
    'saved_search_success_text': _("Your search has been saved."),

    # Translators: This text is displayed before an input box where the user can name his saved search.
    'save_search_name_direction_text': _("Your current search will be saved as:"),

    # Translators: This is text displayed on a submit button which, when clicked, will save the user's search.
    'save_search_button_text': _("Save"),

    #
    # Used in template file: search_form.html
    #

    # Translators: This is the heading for an input field where the user enters keywords for a job search.
    # Example keywords: "nurse", "General Electric", "data entry".
    'keywords_text': _("Keywords"),

    # Translators: This is instructional text for an input field where the user enters keywords for a job search.
    # Example keywords: "nurse", "General Electric", "data entry".
    'keywords_instructions_text': _("job title, skills or company"),

    # Translators: This is the heading for an input field where the user enters location for a job search.
    # Example location: "New York, NY", "Washington", "94043" (postal code).
    'location_text': _("Location"),

    # Translators: This is instructional text for an input field where the user enters location for a job search.
    # Example location: "New York, NY", "Washington", "94043" (postal code).
    'location_instructions_text': _("city, state or zip"),

    # Translators: This is text on a submit button which, when clicked, will perform a search for jobs.
    'search_button_text': _("Search Jobs"),

    #
    # Used in template file: top_header.html
    #

    # Translators: This is the label to inform the user that they can change the site language
    'language_selector_text': _("Language:"),

    # Translators: This is a link in a drop-down menu that takes the user to the email alerts he has
    # created (creating an email alert allows the user to receive daily email notifications of
    # new job openings).
    'menu_email_alerts_text': _("Email Alerts"),

    # Translators: This is a link in a drop-down menu that takes the user to the resume he has uploaded.
    'menu_resume_text': _("Resume"),

    # Translators: This is a link in a drop-down menu that takes the user to a page where he can upload
    # a resume.
    'menu_upload_resume_text': _("Upload Resume"),

    # Translators: This is a link in a drop-down menu that takes the user to a page where he can view
    # the job searches that he has previously saved.
    'menu_saved_searches_text': _("Saved Searches"),

    # Translators: This is a link in a drop-down menu that takes the user to a page where he can view
    # the jobs that he has previously saved.
    'menu_saved_jobs_text': _("Saved Jobs"),

    # Translators: This is a link in a drop-down menu that takes the user to a page where he can view
    # information for his user account.
    'menu_account_text': _("Account"),

    # Translators: This is link in a drop-down menu that, when clicked, signs the user out from his account.
    'menu_sign_out_text': _("Sign Out"),

    # Translators: This is text on a submit button which, when clicked, allows the user to sign in to
    # his account.
    'menu_sign_in_text': _("Sign In"),

    #
    # Used in template file: top_navbar.html
    #

    # Translators: no comment.
    'of_text': _("of"),

    # Translators: no comment.
    'personalized_search_results_text': _("Personalized search results"),

    # Translators: singular form of "job", where job refers to a person's employment/occupation.
    'job_singular_text': _("job"),

    # Translators: plural form of "job", where job refers to a person's employment/occupation.
    'job_plural_text': _("jobs"),

    # Translators: no comment.
    'near_text': _("near"),

    #
    # Used in template file: top_search.html
    #

    # Translators: Informational text for Simply Hired's company logo.
    'logo_alt_text': _("Find Jobs and Careers - SimplyHired.com Job Search"),

    # Translators: This is a link that takes the user to a page where he can perform a more advanced
    # search for jobs where he can specify many specific criteria for the search.
    'advanced_job_search_text': _("Advanced Job Search"),

    # Translators: This is a link that takes the user to a page where he can customize his search
    # (for example, by specifying how many jobs to display on a page).
    'search_options_text': _("Search Options"),

    #
    # Used in template file: content/content_center/jobs_content_center_sponsored_link.html
    #

    # Translators: This text indicates that a job has been sponsored (its listing was paid for by an advertiser).
    'sponsored_text': _("Sponsored"),

    #
    # Used in template file: content/content_left/jobs_content_left_recent_searches.html
    #

    # Translators: This is the heading for a list of job searches that the user has recently performed.
    'recent_searches_heading_text': _("Recent Job Searches"),

    # Translators: This switch, when clicked, will clear the user's history of recently performed searches.
    'recent_searches_clear_text': _("Clear"),

    # Translators: This link, when clicked, will take the user to a page where he can view all of his recent
    # searches (only a few on shown on the original page).
    'recent_searches_see_all_text': _("See all"),

    #
    # Used in template file: content/content_left/jobs_content_left_search_tools.html
    #

    # Translators: This is the heading for a list of useful job search links.
    'job_search_tools_heading_text': _("Job Search Tools"),

    # Translators: This is a link to an RSS feed for a job search.
    'rss_feed_text': _("RSS Feed"),

    #
    # Used in template file: bottom/jobs_bottom_mobile_link.html
    #

    # Translators: This is link to an equivalent page rendered for mobile devices.
    'mobile_link_text': _("Mobile site"),

    #
    # Used in template file: content/content_left/jobs_content_left_email_alerts.html
    # Note: oused for both interstitial email alerts and #email-subscribe functionality.
    #

    # Translators: This is the heading for a dialog box that asks the user to create an email alert.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_interstitial_heading_text': _("Yes, email me job leads like this one."),

    # Translators: This is the text for a button which, when clicked, will allow the user to edit
    # the email alert that he is creating.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_interstitial_edit_text': _("edit"),

    # Translators: This is the text for a submit button that'll save an email alert for the user.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_interstitial_save_text': _("save"),

    # Translators: This text tells a user to enter his email address in an input box.
    'email_alert_interstitial_instruction_text': _("Your email address"),

    # Translators: This text tells a user to enter search keywords an input box.
    "email_alert_interstitial_keywords_text": _("Enter keywords:  job title, skills or company"),

    # Translators: This text tells a user to enter a search location an input box.
    "email_alert_interstitial_location_text": _("Enter a location:  city, state or zip"),

    # Translators: This is the first part of a text for a link that will take the user to a job page
    # without creating an email alert.
    # The full text is: Continue without free email updates
    'email_alert_interstitial_continue_text_1': _("Continue"),

    # Translators: This is the second part of a text for a link that will take the user to a job page
    # without creating an email alert.
    # The full text is: Continue without free email updates
    'email_alert_interstitial_continue_text_2': _("without free email updates"),

    # Translators: no comment.
    'email_alert_interstitial_maintenance_heading_text': _("Maintenance in progress"),

    # Translators: no comment.
    'email_alert_interstitial_maintenance_description_text': _("Our email alert system is currently undergoing routine maintenance. Please try to create or edit your email alert later."),

    # Translators: no comment.
    'email_alert_interstitial_maintenance_apology_text': _("We apologize for any inconvenience."),

    # Translators: no comment.
    'email_alert_interstitial_maintenance_signature_text': _("The Simply Hired Team"),

    # Translators: This is the heading for a dialog box that asks the user to create an email alert.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_subscribe_heading_text': _("Create a Job Email Alert"),

    # Translators: This text tells a user what he'll get when he creates an email alert.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_subscribe_reason_text': _("Get new jobs for this search delivered to your inbox!"),

    # Translators: This text asks a user to create an email alert.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_subscribe_cta_text': _("Create a free job alert by entering your email address:"),

    # Translators: This text tells a user to enter his email address in an input box.
    'email_alert_subscribe_instruction_text': _("Enter email address..."),

    # Translators: This text tells a user that he can unsubscribe from email alerts.
    # (creating an email alert allows the user to receive daily email notifications of new job openings).
    'email_alert_subscribe_info_text': _("You can unsubscribe anytime.  We respect your privacy."),

    #
    # Used in template file: serp_common/serp_content_center_related_searches.html
    #

    # Translators: This is a heading for searches that are similar to and related to the search that the user just performed.
    'related_searches_heading_text': _("Related Searches"),

    # Error Messages
    'SEARCH_RESULT_ERROR_MSGS': {
        'empty-inputs': {
            # Translators: This error heading is displayed when the user did not enter any search terms.
            'heading': _("Oops. Our site thinks you want to see every job we have listed (millions)."),

            # Translators: This error message is displayed when the user did not enter any search terms.
            # Note: please translate the text between the tags, and copy over the tags.
            # A tag is anything between < and >, inclusive.
            # For example, "<p>a girl</p><p>the apples</p>" should translate to
            # "<p>une fille</p><p>les pommes</p>" in French.
            'message': _("<p>In order to receive job results that interest you, please tell us a little something about what you're looking for. Try searching again with a job title, a location or both.</p>")
        },
        'no-results-for-keywords-in-location': {
            # Translators: This error heading is displayed when the user's search has no search results.
            'heading': _("Hmm? This is rare. Your search didn't turn up any results."),

            # Translators: This error message is displayed when the user's search has no search results.
            # Note: please translate the text between the tags, and copy over the tags.
            # A tag is anything between < and >, inclusive.
            # For example, "<p>a girl</p><p>the apples</p>" should translate to
            # "<p>une fille</p><p>les pommes</p>" in French.
            'message': _("<p>Please check the spelling and try again. Often, that solves the problem. If changing the spelling still yields no results, the job you seek might not be available in your search location.</p>")
        },
        'no-results-for-keywords': {
            # Translators: This error heading is displayed when the user's search has no search results.
            'heading': _("Hmm? This is rare. Your search didn't turn up any results."),

            # Translators: This error message is displayed when the user's search has no search results.
            # Note: please translate the text between the tags, and copy over the tags.
            # A tag is anything between < and >, inclusive.
            # For example, "<p>a girl</p><p>the apples</p>" should translate to
            # "<p>une fille</p><p>les pommes</p>" in French.
            'message': _("<p>Please check the spelling and try again. Often, that solves the problem. If changing the spelling still yields no results, the job you seek might not be available in your search location.</p>")
        },
        'invalid-location': {
            # Translators: This error heading is displayed when the user has entered an invalid location in his search.
            'heading': _("We cannot find that location. Let's do something about it."),

            # Translators: This error message is displayed when the user has entered an invalid location in his search.
            # Note: please translate the text between the tags, and copy over the tags.
            # A tag is anything between < and >, inclusive.
            # For example, "<p>a girl</p><p>the apples</p>" should translate to
            # "<p>une fille</p><p>les pommes</p>" in French.
            'message': _("<p>If you entered a location name, please check the spelling. If you entered a ZIP code, perhaps try again with a city, state combination.</p>")
        },
        '404-error': {
            # Translators: This error heading is displayed when the user requests a page that cannot be found.
            'heading': _("Sorry. The page you're looking for either no longer exists or has moved."),

            # Translators: This error message is displayed when the user requests a pages that cannot be found.
            # Note: please translate the text between the tags, and copy over the tags.
            # A tag is anything between < and >, inclusive.
            # For example, "<p>a girl</p><p>the apples</p>" should translate to
            # "<p>une fille</p><p>les pommes</p>" in French.
            'message': _("<p>You may try searching above or clicking the Simply Hired logo to be taken back to our home page.</p>")
        },
        'default-error': {
            # Translators: This error heading is displayed when there has been a non-specific technical error.
            'heading': _("Sorry. We just experienced a momentary technical glitch."),

            # Translators: This error message is displayed when there ahs been a non-specific technical error.
            # Note: please translate the text between the tags, and copy over the tags.
            # A tag is anything between < and >, inclusive.
            # For example, "<p>a girl</p><p>the apples</p>" should translate to
            # "<p>une fille</p><p>les pommes</p>" in French.
            'message': _("<p>You may try searching above or clicking the Simply Hired logo to be taken back to our home page.</p>")
        }
    }
}
