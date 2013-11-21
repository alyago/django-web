var AppViewBase = Backbone.View.extend({

    events: {
        'click .menu-btn': 'onMenuButtonClicked',
        'click #menu-overlay': 'onMenuOverlayClicked',
        'click #search-overlay': 'onSearchOverlayClicked',
        'click .search_placeholder_text': 'onSearchBoxClicked',
        'click #locate-me': 'onClickLocateMeClicked',
        'click a': 'onAnchorElementClicked'
    },

    constructor: function() {
        this.events = _.extend(this.events, AppViewBase.prototype.events);
        Backbone.View.prototype.constructor.apply(this, arguments);
    },

    initialize: function() {

        var self = this;

        // Preload the loading spinner offscreen some time after page load.
        //
        setTimeout(function() {
            self.$('#image-preloader').addClass('loading-spinner');
        }, 500);

        // Attempt to remove the address bar on iOS.
        //
        window.scrollTo(0, 1);

        $('html').css('min-height', $(window).height() + 'px');

        this._installHeartbeat();

        window.onpageshow = window.onpagehide = function(e) {
            if (e.persisted) {
                self._lastHeartbeatTime = new Date().getTime();
                self._updateState();
            }
        };

        window.addEventListener('load', function() {
            new FastClick(document.body);
        }, false);

        // Instantiate models and collections
        //
        this.recentSearchCollection = new RecentSearchCollection();
        this.emailAlertCollection = new EmailAlertCollection();
        this.savedJobCollection = new SavedJobCollection(_.map(
            !!this.options.initialSavedJobs ? this.options.initialSavedJobs : null,
            function(saved_job) { return new SavedJobModel(saved_job);
        }));

        if (this.model.get('isLoggedIn')) {
            this.recentSearchCollection.fetch();
            this.emailAlertCollection.fetch();
    
            if (typeof(this.options.initialSavedJobs) == 'undefined') {
                this.savedJobCollection.fetch();
            }
        }

        this.model.on('change:isLoggedIn', this.onLoginStateChanged, this);

        // Instantiate child views
        //
        this.headerView = new HeaderView();
        this.menuView = new MenuView({
            el: '#menu',
            model: this.model,
            savedJobCollection: this.savedJobCollection,
            recentSearchCollection: this.recentSearchCollection,
            emailAlertCollection: this.emailAlertCollection
        });

        // The "loading" event triggers the loading overlay to appear.
        //
        this.on('loading', this.onLoading, this);
        this.headerView.on('loading', this.onLoading, this);
    },

    //
    // VIEW EVENT HANDLERS
    //

    onAnchorElementClicked: function(e) {
        e.preventDefault();
        this.trigger('loading');
        window.location = e.currentTarget.href;
    },

    onSearchBoxClicked: function(e) {
        this.showSearchBox();
    },

    onMenuButtonClicked: function(e) {
        this.showMenu('main');
    },

    onMenuOverlayClicked: function(e) {
        this.hideMenu();
    },

    onSearchOverlayClicked: function(e) {
        this.hideSearchBox();
    },

    onClickLocateMeClicked: function(e) {
        this.updateLocationInput();
    },

    //
    // MODEL EVENT HANDLERS
    //

    onLoginStateChanged: function() {
        if (this.model.get('isLoggedIn')) {
            this.recentSearchCollection.fetch();
            this.emailAlertCollection.fetch();
            this.savedJobCollection.fetch();
        } else {
            this.recentSearchCollection.reset();
            this.emailAlertCollection.reset();
            this.savedJobCollection.reset();
        }
    },

    onLoading: function(e) {
        this.hideMenu();
        this.hideSearchBox();
        this.showLoadingOverlay();
    },

    //
    // PUBLIC METHODS
    //

    showMenu: function() {
        this.menuView.show.apply(this.menuView, arguments);
        this.$('#menu-overlay').show();

        // HACK: Android has issues with scrollable divs. When a user tries to scroll
        // the menu, it's actually the content that gets scrolled. This means that if
        // the content height is less than the menu height, a user can't scroll to the
        // bottom of the menu.
        //
        // To avoid this issue, we simply make the content heigh equal to the menu
        // height when the menu is opened.
        //
        var $content = this.$('#content');
        var contentHeight = $content.height();
        var menuHeight = this.menuView.$el.height();
        var maxHeight = Math.max(contentHeight, menuHeight);
        this.$el.css('height', maxHeight + 'px');
        $content.css('height', maxHeight + 'px');
        this.menuView.$el.css('height', maxHeight + 'px');

        $content.addClass('open');
    },

    hideMenu: function() {
        this.$('#content').removeClass('open');
        this.$('#menu-overlay').hide();
    },

    showSearchBox: function() {
        this.$('#search-overlay').css('opacity', '0.4').show();
        this.headerView.expandSearchForm();
    },

    hideSearchBox: function() {
        this.headerView.collapseSearchForm();
        this.$('#search-overlay').hide();
    },

    hideLoadingOverlay: function() {
        this.$('#loading-overlay').hide();
    },

    showLoadingOverlay: function() {
        this.$('#loading-overlay').show();
    },

    updateLocationInput: function() {
        var self = this;
        this.getCurrentLocation(function(city, state) {
            self.$('#f_location').val(city + ', ' + state);
            self.headerView.updatePlaceholderText();
        });
    },

    // Called by job-detail.js when a confirm prompt needs to be shown.
    // In addition, this function resets the heartbeat to prevent updateState being called and closing the menu,
    // which occurred because dialogs pause the JS on the page (preventing the heartbeat from updating while the dialog was open).
    // Fixes bug 4320.
    showConfirmDialog: function(message) {
        var dialogResult = confirm(message);
        this._lastHeartbeatTime = Date.now();
        return dialogResult;
    },

    // Called by native iOS app when location and geocoder information is available
    updateLocationInputByiOSApp: function(position, city, state) {
        var self = this;
        self.$('#f_location').val(city + ', ' + state);
        self.headerView.updatePlaceholderText();
    },

    getCurrentLocation: function(locationCallback) {
        if (typeof(navigator.geolocation) === 'undefined')
            return;

        // If coming from the iOS native app, use a custom redirect and return
        // the iOS will call updateLocationInputByiOSApp when the native location is available.
        if (window.appView.options.userAgent.indexOf("SimplyHiredApp-iOS") !== -1) {
          window.location = "shapp:getLocation";
          return;
        }

        var self = this;
        var geolocationCallback = function(position) {
            self._getLocationFromPosition(position, function(city, state) {
                locationCallback(city, state);
            });
        };

        var mapsApiLoadedCallback = function() {
          // This will prompt the user for permission to use their location.
          navigator.geolocation.getCurrentPosition(geolocationCallback);
        };
        self._loadGoogleMapsApi(mapsApiLoadedCallback);
    },

    _installHeartbeat: function() {

        this._lastHeartbeatTime = Date.now();

        // Install a heartbeat so that we can update the user's state periodically.
        // We particularly need this since the user's state is cached for each page
        // when navigating through the browser history.
        //
        var self = this;
        window.setInterval(function(e) {
            var now = Date.now();

            // If the Javascript engine has been paused for more than 3 seconds, then
            // the page was probably frozen, and the user was on another page.
            //
            if (now-self._lastHeartbeatTime > 3000)
            {
                self._updateState();
            }

            self._lastHeartbeatTime = now;
        }, 1000);
    },

    _loadGoogleMapsApi: function(callback) {
        google.load("maps", "3", {
            other_params: 'sensor=false',
            callback: callback
        });
    },

    _getLocationFromPosition: function(position, callback) {
        var geocoder = new google.maps.Geocoder();
        if (!geocoder)
            return;
      
        var latLng = new google.maps.LatLng(
            position.coords.latitude,
            position.coords.longitude
        );

        geocoder.geocode(
            { 'latLng': latLng },
            function (results, geocoderStatus) {
                if (geocoderStatus != google.maps.GeocoderStatus.OK)
                    return;
    
                if (!results[0])
                    return;
    
                var reverse_geo = results[0];
                var city = '';
                var state = '';
                for (var i=0; i < reverse_geo.address_components.length; i++) {
                    var type = reverse_geo.address_components[i].types[0];
                    switch (type) {
                        case 'locality': 
                            city = reverse_geo.address_components[i].long_name;
                            break;
                        case 'administrative_area_level_1':
                            state = reverse_geo.address_components[i].short_name;
                            break;
                    }
                }
                    
                if (city && state) {
                    callback(city, state);
                }
            }
        );
    },

    _updateState: function() {
        this.hideLoadingOverlay();
        this.hideMenu();
        this.hideSearchBox();

        // Before performing a fetch, set isLoggedIn to null, so that when
        // the change handler will be invoked when we do the fetch.
        //
        this.model.set('isLoggedIn', null, { silent: true });
        this.model.fetch();
    }
});

var AppRouter = Backbone.Router.extend({
    routes: {
        'signin': 'signin',
        'signin/:username': 'signin',
        'signin-account-confirmed': 'signinAccountConfirmed',
        'signin-account-confirmed/:username': 'signinAccountConfirmed'
    },

    signin: function(username) {
        window.appView.showMenu('signin', username);

        // Strip off the hashtag
        Backbone.history.navigate('', { replace: true });
    },

    signinAccountConfirmed: function(username) {
        window.appView.showMenu('signin-confirmed', username);

        // Strip off the hashtag
        Backbone.history.navigate(null, { replace: true });
    }
});
