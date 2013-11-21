// Make sure SH namespace is defined.
var SH = SH || {};

// Define SH.tracker namespace.
SH.tracker = {};


/**
 * @class Google Analytics tracker.
 */
SH.tracker.ga = function() {
  // Private variables.
  var DEFAULT_GA_ACCOUNT = 'UA-1039096-6';
  var pageviews = [];

  return {
    /*
     * Load Google analytics ga.js and initialize page tacker for use with .track().
     *
     * @param {string=} opt_trackerAccount Google Analytics tracker account id to use.
     */
    init: function(opt_trackerAccount) {
      var gaUrlPrefix = "https:" == document.location.protocol ? "https://ssl." : "http://www.";
      $.getScript(gaUrlPrefix + 'google-analytics.com/ga.js' , function() {
        // Since this is loading a third party library, be very defensive.
        if (typeof _gat !== "undefined" && typeof _gat._createTracker=== 'function') {
          var trackerAccount = opt_trackerAccount || DEFAULT_GA_ACCOUNT;
          var tracker = _gat._createTracker(trackerAccount);
          if (tracker && typeof tracker._initData === 'function') {
            tracker._initData();
            SH.tracker.ga.tracker = tracker;

            // Track the current page.
            SH.tracker.ga.track();

            // Track any pageviews that were registered before 
            // the Ajax call was returned.
            for (var i = 0; i < pageviews.length; i += 1) {
              SH.tracker.ga.track(pageviews[i]);
            }
          }
        }
      });
    },

    /*
     * Track a page view.
     *
     * @param {string} pageview Url of page to track.
     */
    trackPageview: function(pageview) {
      // If the GA tracker object has already been initialized,
      // track the pageview directly.
      if (!!SH.tracker.ga.tracker) {
        SH.tracker.ga.track(pageview);

      // If the GA tracker has not been initialized, remember the
      // pageview for tracking after GA tracker initialization.
      } else {
        pageviews.push(pageview);
      }
    },

    /*
     * Track a pageview using Google Analytics.
     *
     * @param {string} pageview Page view to track via Google Analytics.
     */
    track: function(pageview) {
      if (SH.tracker.ga.tracker && typeof SH.tracker.ga.tracker._trackPageview === 'function') {
        SH.tracker.ga.tracker._trackPageview(pageview);
      }
    }
  };
}();


/**
 * @class Quantcast tracker.
 */
SH.tracker.q = function () {
  // Private variables.
  var DEFAULT_Q_ACCOUNT = 'p-32oLU8PZtWAwo';

  return {
    /**
     * Load Quantcast quant.js and initialize quantserve.
     */
    init: function(opt_trackerAccount) {
      $.getScript('http://edge.quantserve.com/quant.js', function() {
        _qacct = opt_trackerAccount || DEFAULT_Q_ACCOUNT;

        // Since this is loading a third party library, be very defensive.
        if (typeof quantserve === 'function') {
          quantserve();
        }
      });
    }
  };
}();
