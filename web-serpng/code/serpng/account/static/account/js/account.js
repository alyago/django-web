if (typeof SH == 'undefined' || !SH) {
    var SH = {};
}

AppView = Backbone.View.extend({

    events: {
        'click .navbar li': 'clickToJump'
    },

    initialize: function() {
        //account drop-down
        $('.dropdown-toggle').dropdown();

        $(window).scroll(this.fixedNavbar);
        var emailAlertsView = new EmailAlertsView({ el: $('#l_alert'), model: new EmailAlertsModel });
        var savedJobsView = new MyJobsView({ el: $('#l_jobs'), model: new ViewedJobsModel });
        var mySearchesView = new MySearchesView({ el: $('#l_searches'), model: new RecentSearchesModel });
        var profileView = new ProfileView({ el: $('#l_account'), model: new ProfileModel });
    },

    fixedNavbar: function() {
        if (!$('.navbar').attr('data-top')) {
            if ($('.navbar').hasClass('sh-navbar-fixed')) {
                // navbar is at fixed top position
                return;
            }
            //store original top position in 'data-top'
            var offset = $('.navbar').offset()
            $('.navbar').attr('data-top', offset.top);
        }

        if ($('.navbar').attr('data-top') <= $(this).scrollTop()) {
            $('.navbar').addClass('sh-navbar-fixed');
            $('body').css('padding-top', $('.navbar').outerHeight() + 20);
        } else {
            $('.navbar').removeClass('sh-navbar-fixed');
            $('body').css('padding-top', '0');
        }
    },

    clickToJump: function(e) {
        var target = e ? e.target : '';
        var jump_location = '';
        if (typeof target === 'string') {
            jump_location = target.replace(/^.*?#/,'#');
        } else if ('hash' in target) {
            jump_location = target.hash;
        }
        if ($(jump_location).offset()) {
            var scroll_to = $(jump_location).offset().top - 50;
            $(window).scrollTop(scroll_to);
            return false;
        }
    }

});

EmailAlertsModel = Backbone.Model.extend({
    defaults: {
        cancelAction: null,  //cancel_alert or cancel_all
        alertId: null
    }
});

EmailAlertsView = Backbone.View.extend({

    modalSelector: '#cancel_alert_modal',

    events: {
        'click .modal .confirm_cancel': 'confirmCancel',
        'click a.cancel_all': 'openModal',
        'click a.cancel_alert': 'cancelAlert',
        'click .frequency a': 'updateFrequency'
    },

    render: function() {
        var noAlertsHtml = window.JST.email_alerts({});
        this.$el.html(noAlertsHtml);
    },

    confirmCancel: function() {
        var cancelAction = this.model.get('cancelAction');
        if (cancelAction === 'cancel_all') {
            this.clearAllAlerts();
        } else {
            this.cancelAlertConfirmed();
        }
    },

    clearAllAlerts: function() {
        //TODO - refactor
        var self = this;
        $.post('/account/api/user-profile/', {cancelAlerts:true}, function(data) {
            self.render();
        }, 'json');
        $(this.modalSelector).modal('hide');
    },

    cancelAlert: function(e) {
        var alertId = e.target.id;
        this.model.set({alertId: alertId});
        this.openModal(e);
        return false;
    },

    cancelAlertConfirmed: function() {
        // 'OK' button in modal dialog is clicked
        var cancelUrl = '/a/email-alerts/cancel?id=';
        var alertId = this.model.get('alertId');
        var self = this;
        $.post(cancelUrl+this.model.get('alertId'), {}, function() {
            $('#'+alertId).closest('tr').remove();
            if ($('#c_email_alerts tr').length == 1) {
                // no alerts, render default view
                self.render();
            }
        }, 'json');
        $(this.modalSelector).modal('hide');
    },

    cancel_messages: {
        'cancel_alert': 'Are you sure you want to stop this alert?',
        'cancel_all': 'Are you sure you want to stop all of your alerts?'
    },

    openModal: function(e) {
        var link = e.target.className;
        if (link) {
            $(this.modalSelector).addClass(link);
            $('#cancel_alert_modal .message').html(this.cancel_messages[link]);
        } else {
            return false;
        }
        $(this.modalSelector).modal('show');

        this.model.set({cancelAction: link});

        return false;
    },

    updateFrequency: function(e) {
        var currentFrequency = $(e.target).html();
        var frequencyHtml = window.JST.email_alert_frequency({});

        var dropdownView = new EmailAlertFrequencyView({
            el: $(e.target).closest('.frequency'),
            alertId: e.target.href.replace(/^.*?#/, '')
        });

        return false;
    }

});

//subview of EmailAlertsView
EmailAlertFrequencyView = Backbone.View.extend({

    events: {
        'change select': 'updateFrequency'
    },

    alertId: null,

    initialize: function() {
        this.render();
    },

    render: function() {
        var $frequencyHtml = $(window.JST.email_alert_frequency({}));

        //select index
	for (var i=0,n=$frequencyHtml[0].length; i<n; i++) {
            var option = $frequencyHtml[0].options[i];
            if (option.innerHTML == this.$('a').html()) {
		$frequencyHtml[0].selectedIndex = i;
		break;
            }
	}

        //render dropdown
        this.$el.html($frequencyHtml);
    },

    updateFrequency: function(e) {
        var option = e.target.options[e.target.selectedIndex];
        var selectedValue = option.value;

        //update email alert frequency
        var updateUrl = '/a/email-alerts/update?id=' + this.options.alertId;
        $.post(updateUrl, {frequency: selectedValue}, null, 'json');

        //replace dropdown
        $(e.target).replaceWith('<a href="#'+this.options.alertId+'">'+selectedValue+'</a>');
    }

});

ViewedJobsModel = Backbone.Model.extend({
    url: '/account/api/viewed-jobs/',

    defaults: {
        viewedJobs: null
    },

    getViewedJobs: function() {
        if (!this.get('viewedJobs')) {
            this.fetch({
                success: function(model, response) {
                    if (response.results){
                        model.set({ 'viewedJobs': response.results });
                    }
                }
            });
        }
    }

});

MyJobsView = Backbone.View.extend({

    events: {
        'click .clear_saved': 'clearSavedJobs',
        'click a.t_viewed_jobs': 'getViewedJobs',
        'click .unsave_all': 'removeViewedJobs',
        'click .unsave': 'removeSavedJob',
        'click .job_notes_edit_link': 'displayJobNotesEditArea',
        'click .job_notes_edit_cancel_link': 'displayJobNotes',
        'click .job_notes_edit_save_btn': 'saveJobNotes'
    },

    initialize: function() {
        this.model.bind('change:viewedJobs', this.renderViewedJobs, this);
    },

    renderViewedJobs: function() {
        var viewedJobs = this.model.get('viewedJobs');
        var viewedJobsHtml = _.template(window.JST.viewed_jobs( {'viewedJobs': viewedJobs} ));
        this.$('#t_viewed_jobs').html(viewedJobsHtml);
    },

    clearSavedJobs: function() {
        // calling php application for now
        var self = this;
        $.get('/a/saved-jobs/clear/', function(r) {
            if (r && r.ret_id) {
              self.$('.saved_jobs_results').hide();
              self.$('.expired_saved_jobs').hide();
              self.$('.empty_saved_jobs').show();
            }
        });
        return false;
    },

    getViewedJobs: function() {
        this.model.getViewedJobs();
    },

    removeViewedJobs: function() {
        //remove all viewed jobs
        //calling php application for now
        var self = this;
        $.get('/a/viewed-jobs/clear', function(r) {
            if (r && r.ret_id) {
                self.model.set('viewedJobs', null);
            }
        });
        return false;
    },

    removeSavedJob: function(e) {
        //calling php application for now
        var job = $(e.target).closest('li');
        var rk = $(job).attr('id');
        var self = this;
        $.post('/a/saved-jobs/delete/'+encodeURIComponent(rk),{}, function(r) {
            if(r && r.ret_id) {
                //remove a row
                $(job).slideUp(400, function(){
                    $(this).remove();
                });
            }
        },'json');
        return false;
    },

    displayJobNotesEditArea: function(e) {
        e.preventDefault();

        // Hide "Edit Notes" link and notes
        $(e.target).parent('div').hide();

        // Display the notes in an editable text area
        $('div.job_notes_edit', $(e.target).parent('div').parent('div')).show();
    },

    displayJobNotes: function(e) {
        e.preventDefault();
        
        // Hide the text area
        $(e.target).parent('div').hide();

        // Display the "Edit Notes" link and notes
        var $job_notes_display = $('div.job_notes_display', $(e.target).parent('div').parent('div'));
        $job_notes_display.show();
    },

    displayNewJobNotes: function(e, newNote) {
        // Hide the text area
        $(e.target).parent('div').hide();

        // Display the "Add/Edit notes" link and notes
        var $job_notes_display = $('div.job_notes_display', $(e.target).parent('div').parent('div'));
        if (newNote) { 
            $('a', $job_notes_display).html('Edit Notes:');
            $('span.job_notes_text', $job_notes_display).html(newNote); 
        } else {
            $('a', $job_notes_display).html('Add Notes');
            $('span.job_notes_text', $job_notes_display).html('');
        }
        $job_notes_display.show();
    },

    saveJobNotes: function(e) {
        var job = $(e.target).closest('li');
        var rk = $(job).attr('id');
        var note = $('textarea', $(e.target).parent('div')).val();

        var self = this;
        $.post('/a/saved-jobs/comment/'+encodeURIComponent(rk), 
            {'comment': note}, 
            function(r) {
                if (r && r.ret_id) {
                    self.displayNewJobNotes(e, note);
                };
            },
            'json');
        return false;
    }

});

RecentSearchesModel = Backbone.Model.extend({
    recentSearchesUrl: '/a/my-searches/get-recent/',

    defaults: {
        recentSearches: null
    },

    getRecentSearches: function(pageNum) {
        var recentSearchesUrl = this.recentSearchesUrl;
        if (pageNum) {
            recentSearchesUrl += 'pn-' + pageNum;
        }
        var self = this;
        $.get(recentSearchesUrl, function(r) {
            if (r && r.data) {
                self.set('recentSearches', r.data);
            }
        });
    },

    updateRecentSearches: function() {
        if (!this.get('recentSearches')) {
            this.getRecentSearches();
        }
    }

});

MySearchesView = Backbone.View.extend({

    events: {
        // saved searches
        'click .clear_saved': 'clearSavedSearches',
        'click .remove_saved': 'removeSavedSearch',
        // recent searches
        'click a.t_recent_searches': 'updateRecentSearches',
        'click .clear_recent': 'clearRecentSearches',
        'click .remove_recent': 'removeRecentSearch',
        'click .pagination a': 'paginate'
    },

    initialize: function() {
        this.model.bind('change:recentSearches', this.renderRecentSearches, this);
    },

    renderRecentSearches: function() {
        var recentSearches = this.model.get('recentSearches');
        var templateAttr = {'recentSearches': null};
        if (recentSearches) {
            var currentPageFirstHit = recentSearches.offset + 1;
            var currentPageLastHit = recentSearches.offset + recentSearches.current_hits;
            templateAttr = {
                'recentSearches': recentSearches.rs,
                'currentHits': recentSearches.current_hits,
                'totalHits': recentSearches.total_hits,
                'currentPage': recentSearches.current_page,
                'totalPages': recentSearches.total_pages,
                'firstHit': currentPageFirstHit,
                'lastHit': currentPageLastHit
            }
        }
        var recentSearchesHtml = _.template(window.JST.recent_searches(templateAttr));
        this.$('#t_recent_searches').html(recentSearchesHtml);
    },

    updateRecentSearches: function() {
        this.model.updateRecentSearches();
    },

    clearRecentSearches: function() {
        // calling php application for now
        var self = this;
        $.get('/a/recent-searches/clear/', function(r) {
            if (r && r.ret_id) {
                self.model.set('recentSearches', null);
            }
        });
        return false;
    },

    removeRecentSearch: function(e) {
        //calling php application for now
        var row = $(e.target).closest('tr');
        var searchId = e.target.href.match(/#delete(.*)/)[1];
        var self = this;
        $.post('/a/recent-searches/delete/'+searchId,{}, function(r) {
            if(r && r.ret_id) {
                //remove a row
                $(row).remove();
            }
        },'json');
        return false;
    },

    paginate: function(e) {
        var pageNum = $(e.target).html();
        this.model.getRecentSearches(pageNum);
        return false;
    },

    renderSavedSearches: function() {
        // TODO
        this.$('#t_saved_searches').html("<h4>Saved Searches</h4><div>Hey, we're all looking for something. Save your favorite searches here, then set up an email alert or RSS feed, and we'll notify you when new jobs you might like become available. (<a href=\"/a/jobs/list/q-part+time\">Good idea! I'd like to go and save a search...</a>)</div>");
    },

    removeSavedSearch: function(e) {
        //calling php application for now
        var row = $(e.target).closest('tr');
        var searchId = e.target.href.match(/#delete(.*)/)[1];
        var self = this;
        $.post('/a/saved-searches/delete/'+searchId,{}, function(r) {
            if(r && r.ret_id) {
                //remove a row
                $(row).remove();
            }
        },'json');
        return false;
    },

    clearSavedSearches: function() {
        // calling php application for now
        var self = this;
        $.get('/a/saved-searches/clear/', function(r) {
            if (r && r.ret_id) {
                self.renderSavedSearches();
            }
        });
        return false;
    }

});

ProfileModel = Backbone.Model.extend({
});

ProfileView = Backbone.View.extend({

    passwordMinLength: 6,

    // TODO (bryan): Replace these with gettext() calls for localization.
    errorMessages: {
        'blank-new-email': 'Please enter your new email address.',
        'mismatch-email': 'Emails do not match.',
        'email-already-exists': 'An account using this email has already been created.',

        'blank-current-password': 'Please enter your current password.',
        'blank-new-password': 'Please enter your new password.',
        'mismatch-password': 'Passwords do not match.',
        'bad-length': 'Passwords need to be at least 6 characters.',
        'invalid-char': 'Password contains an invalid character.',

        'incorrect-password': 'Incorrect password'
    },

    events: {
        'submit #f_profile': 'updateProfile',
        'submit #f_email': 'updateEmail',
        'submit #f_password': 'updatePassword',
        'submit #f_close': 'closeAccount'
    },

    updateProfile: function(e) {
        e.preventDefault();

        var firstName = $('#f_first').val();
        var lastName = $('#f_last').val();
        var zipcode = $('#f_zipcode').val();

        $.post('/account/api/user-profile/', {fn:firstName, ln:lastName, zc:zipcode}, function() {
            $('#f_profile .messages').html('<div class="alert alert-success">Updated!</div>');
        });

    },

    updateEmail: function(e) {
        e.preventDefault();
        var currentEmail = $('#f_current_email').val();
        var newEmail1 = $('#f_new_email').val();
        var newEmail2 = $('#f_confirm_email').val();

        var errorCode;
        var errorMessage;
        if (newEmail1 === '' || newEmail2 === '') {
            errorCode = 'blank-new-email';
        } else if (newEmail1 !== newEmail2) {
            errorCode = 'mismatch-email';
        }
        // TODO - refactor
        try {
            ValidateEmail(newEmail1);
        } catch(ex) {
            errorMessage = ex.message;
            $('#f_email .messages').html('<div class="alert alert-error">'+ errorMessage+'</div>');
            return false;
        }

        if (errorCode) {
            $('#f_email .messages').html('<div class="alert alert-error">'+ this.errorMessages[errorCode]+'</div>');
            return false;
        }

        var self = this;
        $.post('/account/api/user-profile/', {email:newEmail1}, function(data) {
            if (data && !data.error_code) {
                $('#f_email .messages').html('<div class="alert alert-success">Updated!</div>');
            } else {
                $('#f_email .messages').html('<div class="alert alert-error">'+ self.errorMessages[data.error_code]+'</div>');
            }
        });
    },

    updatePassword: function(e) {
        e.preventDefault();

        // Clear any messages from a previous attmept.
        $('.messages').empty();

        var currentPassword = $('#f_current_password').val();
        var newPassword1 = $('#f_new_password').val();
        var newPassword2 = $('#f_confirm_password').val();

        // Allow only UTF-8 characters \x21 to \x7E.
        var validPasswordChars = /^[\x21-\x7E]*$/;

        var errorCode;
        if (newPassword1 === '' || newPassword2 === '') {
            errorCode = 'blank-new-password';
        } else if (currentPassword === '') {
            errorCode = 'blank-current-password';
        } else if (newPassword1.length < this.passwordMinLength) {
            errorCode = 'bad-length';
        } else if (newPassword1 !== newPassword2) {
            errorCode = 'mismatch-password';
        } else if (!validPasswordChars.test(newPassword1)) {
            errorCode = 'invalid-char';
        }

        if (errorCode) {
            $('#f_password .messages').html('<div class="alert alert-error">'+ this.errorMessages[errorCode]+'</div>');
            return false;
        }

        var self = this;
        $.post('/account/api/user-profile/', {currentPassword:currentPassword, newPassword:newPassword1}, function(data) {
            if (data && !data.error_code) {
                $('#f_password .messages').html('<div class="alert alert-success">Updated!</div>');
            } else if (data && data.error_code) {
                $('#f_password .messages').html('<div class="alert alert-error">'+ self.errorMessages[data.error_code]+'</div>');
            } else {
                $('#f_password .messages').html('<div class="alert alert-error">Something went wrong.</div>');
            }
        }, 'json');
    },

    closeAccount: function(e) {
        e.preventDefault();
        var password = $('#f_close_password').val();

        //TODO - refactor
        var self = this;
        $.post('/account/api/user-profile/', {closePassword:password}, function(data) {
            if (data && !data.error_code) {
                $.get('/a/accounts/logout', function() {
                    window.location.replace('http://www.simplyhired.com');
                });
            } else if (data && data.error_code) {
                $('#f_close .messages').html('<div class="alert alert-error">'+ self.errorMessages[data.error_code]+'</div>');
            }
        }, 'json');
    }

});

$(function() {
    var appView = new AppView({ el: $('body') });

    SH.tracker.ga();
    SH.tracker.q();
});

$(window).load(function(){
    // adjust resume iframe height
    var iframe_height = $('.resume_iframe').contents().height();
    if ($('.resume_iframe').contents().find('div.msg div.note') && iframe_height == '150') {
        iframe_height = '80';
    }
    $('.resume_iframe').css('height', iframe_height+'px');
});

/*
 * Tracking
 */
SH.tracker = function() {

    return{

        /*
         * google analytics
         * load ga.js and call tracking
         * sets global sh_pageTracker
         */
        ga: function() {
            $.getScript((("https:"==document.location.protocol)?"https://ssl.":"http://www.")+('google-analytics.com/ga.js'),function(e){
                sh_pageTracker = _gat._getTracker(sh_pageAccount);
                sh_pageTracker._initData();
                sh_pageTracker._trackPageview();
            });
        },

        //call quantcast tracking quant.js
        q: function() {
            $.getScript('http://edge.quantserve.com/quant.js', function(e){
                _qacct="p-32oLU8PZtWAwo";
                quantserve();
            });
        }
    };

}();

/**
* test for js-capable bots
*/
SH.challenge = function() {
    var alpha = Math.floor(Math.random()*11) + 1;
    var beta = Math.floor(Math.random()*11) + 1;
    var x = $.post('/a/job/check/', { 'a': alpha, 'b': beta, 'c': alpha+beta }, function(data) {
      $.post(data);
    });
}();  // SH.challenge()
