String.prototype.endsWith = function(suffix) {
  return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

SignUpFormModel = Backbone.Model.extend({
  defaults: {
    email: null,
    password: null,
    error: null
  }
});

SignUpFormView = FormView.extend({

  errors: {
    'email-taken': 'Sorry! Someone has already created an account with that email address.',
    'error-login': 'We were unable to log you in. Please check that your email adddress and password are correct.',
    'short-password': 'Sorry! Your password is too short.',
    'invalid-password': 'Sorry! That password is invalid.',
    'error-no-response': 'It looks like we\'ve run into some technical difficulty. Please try returning at a later time!'
  },

  events: {
    'click #email-button': 'openEmailWindow',
    'blur #email' : 'onEmailChanged'
  },

  initialize: function() {
    this.baseInitialize();
    this.model.on('change:error', this.onErrorChanged, this);
  },

  validate: function() {
    try {
      ValidateEmail(this.model.get('email'));
    } catch(ex) {
      EventLog.accounts.sign_up_failed('invalid-email');
      this.model.set('error', ex.message);
      return false;
    }

    var password = this.$('#password').val();
    if (password == null || password == '') {
      EventLog.accounts.sign_up_failed('blank-password');
      this.model.set('error', 'Please enter your password.');
      return false;
    }

    this.model.set('password', password);

    return true;
  },

  submit: function() {

    // Hide all existing error messages.
    this.model.set('error', null);
    var forwardUrl = null;

    // Disable the form.
    this.disable();

    // Submit request.
    var email = this.model.get('email');
    var postParams = {
        'email' : email,
        'password' : this.model.get('password')
    };

    if ('f' in this.options.appModel.queryParams) {
        forwardUrl = this.options.appModel.queryParams['f'];
        postParams['f'] = forwardUrl;
    }

    var self = this;
    var request = $.post('/a/member/create-account', postParams);
    request.fail(function() {
      EventLog.accounts.sign_up_failed('ajax-failure');
      self.model.set('error', 'Sorry! Something went wrong! Please try again.');
      self.enable();
    })
    request.done(function(json_response, success) {
      var error_code = json_response['data']['error'];
      if (error_code == null) {

        // Success! Go to the forward URL.
        self.$('.form-fields').hide();
        self.$('.success-message').show();
        self.enable();

        var email_provider = _.find(self.email_providers, function(email_provider) {
          return email.endsWith(email_provider.suffix);
        });

        if (email_provider != null) {
          self.$('#email-button').attr('data-href', email_provider.url);
          self.$('#email-button').text('Go to ' + email_provider.name + ' now!');
          self.$('#email-button').show();
          self.$('#email-button').removeAttr('disabled');
        }

        EventLog.accounts.sign_up_succeeded();
      } else {

        // Display some kind of user-friendly error.
        EventLog.accounts.sign_up_failed(error_code);
        self.model.set('error', self.errors[error_code]);
        self.enable();
      }
    });

    return false;
  },

  onEmailChanged: function() {
    this.model.set('email', this.$('#email').val());
  },

  onErrorChanged: function() {
    var error = this.model.get('error');
    if (error == null) {
      this.$('.error-message').hide();
    } else {
      this.$('.error-message').text(this.model.get('error'));
      this.$('.error-message').show();
    }
  },

  openEmailWindow: function() {
    window.location.replace(this.$('#email-button').attr('data-href'));
  }
});

AppView = Backbone.View.extend({

  initialize: function() {
    this.signUpFormModel = new SignUpFormModel({
      'email' : this.$('#email').val()
    });

    this.signUpFormView = new SignUpFormView({
      el: this.$('#signup-form'),
      model: this.signUpFormModel,
      appModel: this.model
    });

    this.signUpFormModel.bind('change:email', this.updateSignInLink, this);

    this.updateSignInLink();
  },

  updateSignInLink: function() {
    var email = this.signUpFormModel.get('email');

    var paramDict = {
      'email' : email
    };

    if ('f' in this.model.queryParams) {
      paramDict['f'] = this.model.queryParams['f'];
    }

    uri = MakeUri('/account/signin', paramDict);
    this.$('#signin-link').attr('href', uri);
    $('.signup-email').text(email);
  }
});

$(function() {
  var appView = new AppView({
    el: $('body'),
    model: new AppModel()
  });
});
