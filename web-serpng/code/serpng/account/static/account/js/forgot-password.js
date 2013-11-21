String.prototype.endsWith = function(suffix) {
  return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

ForgotPasswordFormModel = Backbone.Model.extend({
  defaults: {
    email: null,
    error: null
  }
});

ForgotPasswordFormView = FormView.extend({
  _errors: {
    'default-error': 'Sorry! There was an problem contacting the server. Please try again later.'
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
      EventLog.accounts.forgot_password_failed('blank-email');
      this.model.set('error', ex.message);
      return false;
    }

    return true;
  },

  submit: function() {

    // Hide all existing error messages.
    this.model.set('error', null);

    // Disable the form.
    this.disable();

    // Submit request.
    var email = this.model.get('email');
    var postParams = { 'email' : email };

    var self = this;
    var request = $.post('/a/member/forgot-password', postParams);
    request.fail(function() {
      EventLog.accounts.forgot_password_failed('ajax-failure');
      self.$('#error-message').text('Sorry! Something went wrong! Please try again.');
      self.$('#error-message').show();
      self.enable();
    });
    request.done(function(json_response, success) {
      if (json_response != null && json_response.data != null) {

        self.$('.success-message').show();

        var email_provider = _.find(self.email_providers, function(email_provider) {
          return email.endsWith(email_provider.suffix);
        });

        if (email_provider != null) {
          self.$('#email-button').attr('data-href', email_provider.url);
          self.$('#email-button').text('Go to ' + email_provider.name + ' now!');
          self.$('#email-button').show();
          self.$('#email-button').removeAttr('disabled');
        }

        self.$('*').css('cursor', 'auto');
        self.$('.form-inputs').hide();

        EventLog.accounts.forgot_password_succeeded();
      } else {

        // Display some kind of user-friendly error.
        var error_code = (json_response.data == null ? 'default-error' : json_response.data.error);
        EventLog.accounts.forgot_password_failed(error_code);
        self.$('#error-message').text(self._errors[error_code]);
        self.$('#error-message').show();
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
      this.$('#error-message').hide();
    } else {
      this.$('#error-message').text(this.model.get('error'));
      this.$('#error-message').show();
    }
  },

  openEmailWindow: function() {
    window.location.replace(this.$('#email-button').attr('data-href'));
  }
});

AppView = Backbone.View.extend({

  initialize: function() {
    this.forgotPasswordFormModel = new ForgotPasswordFormModel({
      'email' : this.$('#email').val()
    });

    this.forgotPasswordFormView = new ForgotPasswordFormView({
      el: this.$('#forgot-password-form'),
      model: this.forgotPasswordFormModel,
      appModel: this.model
    });

    this.forgotPasswordFormModel.bind('change:email', this.updateSignInAndSignUpLinks, this);

    this.updateSignInAndSignUpLinks();
  },

  updateSignInAndSignUpLinks: function() {
    var paramDict = {
      'email' : this.forgotPasswordFormModel.get('email')
    };

    if ('f' in this.model.queryParams) {
      paramDict['f'] = this.model.queryParams['f'];
    }

    this.$('#signin-link').attr('href', MakeUri('/account/signin', paramDict));
    this.$('#signup-link').attr('href', MakeUri('/account/signup', paramDict));
  }
});

$(function() {
  var appView = new AppView({
    el: $('body'),
    model: new AppModel()
  });
});
