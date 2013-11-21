AccountModel = Backbone.Model.extend({
    defaults: {
        isLoggedIn: false,
        username: null
    },

    initialize: function() {
        this.resendConfirmation = this.resetPassword;
    },

    create: function(email, password, successCallback, errorCallback) {
        var self = this;
        this._makeLegacyAjaxCall(
            '/a/member/create-account',
            { 'email': email, 'password': password },
            successCallback,
            errorCallback);
    },

    getEmail: function() {
        var username = this.get('username');
        var accountEmail = (username && username.indexOf('@') >= 0 ? username : null);
        var alertEmail = SH.cookies.getSubcookie('shua', 'uaemail');
        
        return accountEmail || alertEmail;
    },

    login: function(email, password, successCallback, errorCallback) {
        var self = this;
        this._makeLegacyAjaxCall(
            '/a/member/login',
            { 'email': email, 'password': password },
            function() {
                self.set('isLoggedIn', true);
                self.set('username', email);
                if (!!successCallback) {
                    successCallback();
                }
            },
            errorCallback);
    },

    logout: function(successCallback, errorCallback) {
        var self = this;
        this._makeLegacyAjaxCall(
            '/a/member/logout',
            null,
            function() {
                self.set('isLoggedIn', false);
                self.set('username', null);
                if (!!successCallback) {
                    successCallback();
                }
            },
            errorCallback);
    },

    resetPassword: function(email, successCallback, errorCallback) {
        this._makeLegacyAjaxCall(
            '/a/member/forgot-password',
            { 'email': email },
            successCallback,
            errorCallback);
    },

    sync: function(method, model, options) {
        if (method === 'read') {
            var url = '/a/member/status';
            var xhr = $.ajax({
                url:url,
                success:function(data, status, xhr) {
                    var json_obj = JSON.parse(data);
                    model.set({
                        'isLoggedIn': json_obj.login,
                        'username': json_obj.username,
                    });
                },
                cache:false
            });
            return xhr;
        } else {
            return Backbone.Model.prototype.sync.apply(this, arguments);
        }
    },

    _makeLegacyAjaxCall: function(url, data, successCallback, errorCallback) {
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            error: function() {
                if (!!errorCallback) {
                    errorCallback('generic-error');
                }
            },
            success: function(response) {
                var jsonResponse = $.parseJSON(response);

                var errorCode = jsonResponse.data.error;
                if (errorCode === null) {
                    if (!!successCallback) {
                        successCallback();
                    }
                } else {
                    if (!!errorCallback) {
                        errorCallback(errorCode);
                    }
                }
            }});
    }
});
