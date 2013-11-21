var MenuView = Backbone.View.extend({
     
    initialize: function() {
        
        this._inputUsername = null;

        this.emailAlertCollection = this.options.emailAlertCollection;
        this.recentSearchCollection = this.options.recentSearchCollection;
        this.savedJobCollection = this.options.savedJobCollection;

        this._renderMode = 'main';

        this._editEmailAlertsMode = false;
        this._editRecentSearchesMode = false;
        this._editSavedJobsMode = false;

        this.emailAlertCollection.on('all', this.onEmailAlertsChanged, this);
        this.recentSearchCollection.on('all', this.onRecentSearchesChanged, this);
        this.savedJobCollection.on('all', this.onSavedJobCollectionChanged, this);
    },

    events: {
        'click .cancel-button': 'onCancelButtonClicked',
        'click .goto-signup-button': 'onGoToSignUpButtonClicked',
        'click .goto-signin-button': 'onGoToSignInButtonClicked',
        'click .signout-button': 'onSignOutButtonClicked',
        'click .menu-signin .submit-button': 'onSignInButtonClicked',
        'click .menu-signup .submit-button': 'onSignUpButtonClicked',
        'click .edit-email-alerts-button': 'onDeleteEmailAlertButtonClicked',
        'click .edit-recent-searches-button': 'onDeleteRecentSearchButtonClicked',
        'click .edit-saved-jobs-button': 'onDeleteSavedJobButtonClicked',
        'click .resend-confirmation-link': 'onResendConfirmationLinkClicked',
        'click #edit-recent-searches-button': 'onClickEditRecentSearches',
        'click #edit-saved-jobs-button': 'onClickEditSavedJobs',
        'click #edit-email-alerts-button': 'onClickEditEmailAlerts',
        'blur input.email': 'onUsernameInputBlurred'
    },

    _errorMessages: {
        'blank-email': 'Missing email address.',
        'blank-password': 'Missing password.',
        'email-taken': 'Sorry! Someone has already created an account with that email address.',
        'error-login': 'We were unable to log you in. Please check that your email address and password are correct.',
        'error-no-account': 'We were unable to log you in. Please check that your email address and password are correct.',
        'error-no-response': 'It looks like we\'ve run into some technical difficulty. Please try returning at a later time!',
        'invalid-email': 'Please enter a valid email address.',
        'invalid-password': 'Please enter a password containing at least one letter and one number.',
        'short-password': 'Sorry! Your password is too short.',
        'generic-error': 'It looks like we\'ve run into some technical difficulty. Please try returning at a later time!'
    },

    //
    // PUBLIC
    //

    show: function() {
        this._editEmailAlertsMode = false;
        this._editRecentSearchesMode = false;
        this._editSavedJobsMode = false;

        // Default the first argument (i.e., renderState) to 'main' if not
        // specified.
        //
        var args = arguments;
        if (args.length === 0) {
            args[0] = 'main';
        }

        this.render.apply(this, args);
        
        // HACK: The CSS rule "-webkit-overflow-scrolling:touch" prevents Chrome on
        // Android from scrolling, so we use this nasty hack to apply the rule only to
        // iOS devices.
        //
        // The cause of this, according to someone on StackOverflow, is that support for
        // this property was removed from Chrome with the fix for bug 172481:
        //
        // http://stackoverflow.com/questions/15906508/chrome-browser-for-android-no-longer-supports-webkit-overflow-scrolling-is-the
        //
        // Longer-term, a better solution would be to use Modernizr or an iOS-specific
        // CSS file (like Wikimedia does here: https://gerrit.wikimedia.org/r/#/c/5442/).
        //
        if (navigator.userAgent.indexOf('iPhone') !== -1) {
            this.$el.css('-webkit-overflow-scrolling', 'touch');
        }

        this.$el.show();

        // Scroll to the top to make sure that the menu is visible when opened.
        //
        document.body.scrollTop = 0;
    },

    render: function(renderMode, username) {
        if (!!renderMode) {
            this._renderMode = renderMode;
        }

        // If specified, override the username
        //
        if (!!username) {
            this._inputUsername = username;
        }

        switch (this._renderMode) {
            case 'signin':
                this.$el.html(JST.menu_signin({
                    username : this._inputUsername,
                    just_confirmed: false,
                    needs_confirmation: false
                }));
                break;
            case 'signin-confirmed':
                this.$el.html(JST.menu_signin({
                    username: this._inputUsername,
                    headline: 'Activation email sent',
                    just_confirmed: true,
                    needs_confirmation: false
                }));
                break;
            case 'signin-unconfirmed':
                this.$el.html(JST.menu_signin({
                    username: this._inputUsername,
                    headline: 'Activation email sent',
                    just_confirmed: false,
                    needs_confirmation: true
                }));
                break;
            case 'signup':
                this.$el.html(JST.menu_signup({ username : this._inputUsername }));
                break;
            case 'signup-unconfirmed':
                this.$el.html(JST.menu_signup_unconfirmed({
                    email : this._inputUsername,
                    headline: 'You’re almost done!',
                    include_resend_link: true
                }));
                break;
            case 'signup-unconfirmed-resent':
                this.$el.html(JST.menu_signup_unconfirmed({
                    email: this._inputUsername,
                    headline: 'Activation email sent',
                    include_resend_link: false
                }));
                break;
            case 'main':
                // The list of email alerts is filtered here, since newly created email
                // alerts are immediately added to the collection, but don't
                // immediately have an ID until // the AJAX call returns. If a user
                // tries to delete an email alert in this state, they'll get a
                // Javascript error.
                //
                var emailAlerts = _.filter(
                    this.emailAlertCollection.models,
                    function(model) { return model.id !== null; }
                );

                this.$el.html(JST.menu_main({
                    isLoggedIn : this.model.get('isLoggedIn'),
                    username : this.model.get('username'),
                    savedJobs : _.map(this.options.savedJobCollection.models, function(model) {
                        return { 
                            title: model.get('title'), 
                            location: model.get('location'), 
                            path: model.get('mobilePermalinkUrl'), 
                            refindkey: model.get('refindkey'), 
                        };
                    }),
                    editEmailAlertsMode : this._editEmailAlertsMode,
                    editRecentSearchesMode : this._editRecentSearchesMode,
                    editSavedJobsMode : this._editSavedJobsMode,
                    recentSearches : _.map(
                        this.recentSearchCollection.models,
                        function(model) {
                            return {
                                title: model.get('title'),
                                path: '/a/mobile-jobs/list/' + model.get('query'),
                                query: model.get('query')
                            };
                        }),
                    emailAlerts : _.map(
                        emailAlerts,
                        function(model) {
                            return {
                                id: model.get('id'),
                                title: model.get('title'),
                                path: '/a/mobile-jobs/list/' + model.get('query')
                            };
                        })
                }));
                break;
        }

        return this;
    },

    //
    // PRIVATE
    //

    _getErrorMessage: function(errorCode) {
        if (!this._errorMessages[errorCode]) {
            errorCode = 'generic-error';
        }

        return this._errorMessages[errorCode];
    },

    //
    // EVENT HANDLERS
    //

    onCancelButtonClicked: function(e) {
        this.render('main');
    },

    onGoToSignInButtonClicked: function(e) {
        this.render('signin');
    },

    onGoToSignUpButtonClicked: function(e) {
        this.render('signup');
    },

    onResendConfirmationLinkClicked: function(e) {
        e.preventDefault();

        var resendHandler = function() {
            self.render('signup-unconfirmed-resent');
        };

        var self = this;
        this.model.resendConfirmation(
            this._inputUsername,
            resendHandler,
            resendHandler // For some reason, the call returns generic-error on success
        );
    },

    onSignInButtonClicked: function(e) {
        e.preventDefault();

        var self = this;
        this.model.login(
            this.$('.menu-signin .email').val(),
            this.$('.menu-signin .password').val(),
            function() {
                self.render('main');
            },
            function(errorCode) {
                if (errorCode === 'error-unconfirmed') {
                    self.render('signin-unconfirmed');
                } else {
                    var errorMessage = self._getErrorMessage(errorCode);
                    self.$('.menu-signin .error-message').html(errorMessage);
                }
            }
        );
    },

    onSignOutButtonClicked: function(e) {
        var self = this;
        this.model.logout(function() {
            self.render('main');
        });
    },

    onSignUpButtonClicked: function(e) {
        e.preventDefault();

        var self = this;
        var email = this.$('.menu-signup .email').val();
        var password = this.$('.menu-signup .password').val();
        this.model.create(
            email,
            password,
            function() {
                self.render('signup-unconfirmed');
            },
            function(errorCode) {
                self.$('.menu-signup .error-message').html(self._getErrorMessage(errorCode));
            }
        );
    },

    onEditAccountItems: function(e) {
            this._editEmailAlertsMode = false;
            this._editRecentSearchesMode = false;
            this._editSavedJobsMode = false;
            var editButton = e.target,
             featureToEdit = editButton.getAttribute("id"),
             deleteButtons = editButton.getAttribute("listType");
             //toggle the Edit button
             this.$('#' + featureToEdit).toggleClass('active');
             //toggle the individual delete buttons
             this.$('.' + featureToEdit).toggleClass('active');
             this['_edit' + deleteButtons + 'Mode'] = true;
        },

        onDeleteEmailAlertButtonClicked: function(e) {
            var alertId = $(e.target).data('id');
            this.emailAlertCollection.get(alertId).destroy({ wait: true });
        },

        onDeleteRecentSearchButtonClicked: function(e) {
            var query = $(e.target).data('query');
            this.recentSearchCollection.get(query).destroy();
        },

        onDeleteSavedJobButtonClicked: function(e) {
            var target = e.target,
                refindkey = target.getAttribute('refindkey');
            this.savedJobCollection.get(refindkey).destroy({ wait: true });
        },

        onClickEditRecentSearches: function(e) {
            this.$('.edit-email-alerts-button').removeClass('active');
            this.$('.edit-saved-jobs-button').removeClass('active');
            this.$('#edit-saved-jobs-button').removeClass('active');
            this.$('#edit-email-alerts-button').removeClass('active'); 
            this.onEditAccountItems(e);
        },

        onClickEditSavedJobs: function(e) {
            this.$('.edit-email-alerts-button').removeClass('active');
            this.$('.edit-recent-searches-button').removeClass('active');
            this.$('#edit-recent-searches-button').removeClass('active');
            this.$('#edit-email-alerts-button').removeClass('active');
             this.onEditAccountItems(e);
        },

        onClickEditEmailAlerts: function(e) {
            this.$('.edit-recent-searches-button').removeClass('active');
            this.$('.edit-saved-jobs-button').removeClass('active');
            this.$('#edit-saved-jobs-button').removeClass('active');
            this.$('#edit-recent-searches-button').removeClass('active'); 
            this.onEditAccountItems(e);
        },

    //TODO: these should all be combined
    onEmailAlertsChanged: function() {
        this.render();
    },

    onRecentSearchesChanged: function() {
        this.render();
    },

    onSavedJobCollectionChanged: function() {
        this.render();
    },

    onUsernameInputBlurred: function(e) {
        this._inputUsername = $(e.target).val().trim();
    }
});
