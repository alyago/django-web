// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class Global navigation service object.
 */
SH.NavigationService = {
  /**
   * Navigate to passed-in searchUrl.
   * 
   * @param {string} searchUrl Url to navigate to.
   */
  navigateTo: function(searchUrl) {
    document.location = searchUrl;
  }
};


/**
 * @class Global cookie service object.
 */
SH.CookieService = {
  /**
   * Return document.cookie.
   */
  readCookie: function() {
    return document.cookie;
  },
  
  /**
   * Write to document.cookie.
   * 
   * @param {string} cookieString String to replace document.cookie.
   */
  writeCookie: function(cookieString) {
    document.cookie = cookieString;
  }
};


SH.LocalStorageService = {
  set: function(key, value) {
    value = JSON.stringify(value);

    if (window.Modernizr && Modernizr.localstorage) {
      localStorage.setItem(key, value);
    } else {

      // Use userData for IE7, if available.
      var userDataElementID = 'js-ie7-user-data-' + key;
      var userDataElement = document.getElementById(userDataElementID);

      if (!!userDataElement.addBehavior) {
        userDataElement.setAttribute(key + 'Attr', value);
        userDataElement.save(key);
      }
    }
  },

  get: function(key) {
    var val = null;

    if (window.Modernizr && Modernizr.localstorage) {

      if (!!localStorage[key]) {
        val = localStorage.getItem(key);
      }
    } else {

      // Use userData for IE7, if available.
      var userDataElementID = 'js-ie7-user-data-' + key;
      var userDataElement = document.getElementById(userDataElementID);

      if (!!userDataElement.addBehavior) {
        userDataElement.load(key);
        val = userDataElement.getAttribute(key + 'Attr');
      }
    }

    if (!!val) {
      return JSON.parse(val);
    } else {
      return null;
    }
    return null;
  },

  remove: function(key) {
    if (window.Modernizr && Modernizr.localstorage) {
      localStorage.removeItem(key);
    } else {

      // Use userData for IE7, if available.
      var userDataElementID = 'js-ie7-user-data-' + key;
      var userDataElement = document.getElementById(userDataElementID);

      if (!!userDataElement.addBehavior) {
        userDataElement.removeAttribute(key + 'Attr');
        userDataElement.save(key);
      }
    }    
  }

};