var ListAppView = AppViewBase.extend({

    events: {
        'click .result-save-job': 'onSavedStarClicked',
        'click .email-btn': 'onEmailButtonClicked'
    },

    initialize: function(options) {
        AppViewBase.prototype.initialize.apply(this, arguments);

        this.pageKeywords = this.$('#f_keywords').val();
        this.pageLocation = this.$('#f_location').val();
        this.pageQuery = document.location.pathname.replace('/a/mobile-jobs/list/', '');

        this.emailAlertView = new EmailAlertView({
            el: '.email-box',
            model: this.model,
            collection: this.emailAlertCollection,
            pageKeywords: this.pageKeywords,
            pageLocation: this.pageLocation,
            pageQuery: this.pageQuery
        });

        this.emailAlertView.on('close', this.onEmailAlertViewClosed, this);
        this.savedJobCollection.on('all', this.onSavedJobCollectionChanged, this);
    },

    //
    // EVENT HANDLERS
    //
    
    onEmailButtonClicked: function() {
        this.showEmailBox();
    },

    onSearchBoxClicked: function() {
        this.hideEmailBox();
        this.showSearchBox();
    },

    onSearchOverlayClicked: function() {
        this.hideEmailBox();
        this.hideSearchBox();
    },

    onEmailAlertViewClosed: function() {
        this.hideEmailBox();
        this.hideSearchBox();
    },

    onSavedStarClicked: function(e) {
        if (!this.model.get('isLoggedIn')) {
            var openSignInDialog = confirm('You must sign in before you can save this job. Would you like to sign in now?');
            if (openSignInDialog) {
                this.showMenu();
            }
    
            return;
        }

        var $resultNode = $(e.target).parents('.result');
        var refindkey = this._getRefindKey($resultNode);
  
        if ($(e.target).hasClass('saved')) {
            this.savedJobCollection.get(refindkey).destroy();
        } else {
            var jobModel = new SavedJobModel({
                'company': $('.result-company', $resultNode).html(),
                'location': $('.result-location', $resultNode).html(),
                'mobilePermalinkUrl': 'http://m.simplyhired.com/a/mobile-jobs/view/jobkey-' + refindkey,
                'notes': '',
                'refindkey': refindkey,
                'title': $('.result-title', $resultNode).html()
            });

            this.savedJobCollection.create(jobModel, { at: 0 });
        }
    },

    onSavedJobCollectionChanged: function() {
        var self = this;
        this.$('.result').each(function(index, resultNode) {
            var $resultNode = $(resultNode);

            var refind_key = self._getRefindKey($resultNode);
            var isSaved = !!self.savedJobCollection.get(refind_key);
            $('.result-save-job', $resultNode).toggleClass('saved', isSaved);
        });
    },

    //
    // PUBLIC METHODS
    //

    showEmailBox: function() {
        this.emailAlertView.render();
        this.$('.email-box').toggle();
        this.$('.email-btn').toggleClass('active');
        this.$('#search-overlay').css('opacity', '0').show();
    },

    hideEmailBox: function() {
        this.$('.email-box').hide();
        this.$('.email-btn').removeClass('active');
        this.$('#search-overlay').hide();
    },

    showMenu: function() {
        this.hideEmailBox();
        AppViewBase.prototype.showMenu.apply(this, arguments);
    },

    //
    // PRIVATE METHODS
    //

    _getRefindKey: function($resultNode) {

        // The format of the refind key data attribute is "id:<refindkey>".
        // The "id:" prefix is only present to prevent Zepto from converting
        // the value to a number (some refind keys look like floating point
        // numbers, which will cause trailing zeroes to be truncated).
        //
        return $resultNode.data('refind-key').substring(3);
    }
});
