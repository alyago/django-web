// Make sure SH namespace is defined.
var SH = SH || {};


/**
 * @class Cookie handler.
 */
SH.cookies = function() {
  // Private variables

  // Configuration for SH cookies.
  // See: https://redmine.apple.sh.pie/projects/dev/wiki/WWW_Cookies
  var cookieProperties = {

    // 'shua' cookie
    'shua': {
      'delimiter': ',',
      'keyValueDelimiter': '=',
      'path': '/',
      'domain': document.location.hostname.replace(/^.*(\.simplyhired.*)$/, '$1'),
      'expires': function() {
        var expDate = new Date();
        expDate.setFullYear(expDate.getFullYear() + 2);
        return expDate;
      }
    }
  };

  // Private functions

  /**
   * Return the value of a cookie's property, as configured in
   * cookieProperties.
   *
   * @param {string} name Name of the cookie.
   * @param {string} property Property name of the cookie.
   * @return {*} Value of the property, or null if the property was
   *     not configured.
   */
  var getCookieProperty = function(name, property) {
    return (!!cookieProperties[name] && !!cookieProperties[name][property]
        ? cookieProperties[name][property]
        : null);
  };

  /**
   * Parse cookie with passed-in name and returns its subcookies.
   *
   * @param {string} name Name of the cookie with subcookies.
   * @return {Object.<string, string>} Key-value pairs of subcookies.
   */
  var getAllSubcookies = function(name) {
    var cookieName = encodeURIComponent(name) + '=';
    var documentCookie = SH.CookieService.readCookie();
    var cookieValue = getCookiePublic(name);

    if (!!cookieValue) {
      if (cookieValue.length > 0) {
        cookieValue = decodeURIComponent(cookieValue);

        if (cookieProperties[name]) {
          var subcookies = cookieValue.split(
            cookieProperties[name]['delimiter']);

          var result = {};
          for (var i = 0, len = subcookies.length; i < len; i++) {
            var parts = subcookies[i].split(
                cookieProperties[name]['keyValueDelimiter']);
            result[parts[0]] = parts[1];
          }

          return result;
        }
      }
    }
                            
    return null;
  };

  /**
   * Write cookie with passed-in name with the passed-in subcookies.
   *
   * @param {string} name Name of the cookie with subcookies.
   * @param {Object.<string, string>} subcookies Key-value pairs of subcookies.
   * @param {Date=} opt_expires Expiration date to set.
   * @param {string=} opt_path Path to set.
   * @param {string=} opt_domain Domain to set.
   */
  var setAllSubcookies = function(name, subcookies, opt_expires, opt_path, opt_domain) {
    var cookieText = encodeURIComponent(name) + '=';
    var subcookieParts = new Array();
    var subname;

    if (!cookieProperties[name]) {
      return null;
    }

    for (subname in subcookies) {
      if (subname.length > 0 && subcookies.hasOwnProperty(subname)) {
        subcookieParts.push(encodeURIComponent(
            subname + cookieProperties[name]['keyValueDelimiter'] + subcookies[subname]));
      }
    }

    if (subcookieParts.length > 0) {
      cookieText += subcookieParts.join(encodeURIComponent(cookieProperties[name]['delimiter']));

      // Optionally add expires part of cookie.
      var cookieExpires = (opt_expires && (opt_expires instanceof Date)) || 
          (!!getCookieProperty(name, 'expires')
           ? getCookieProperty(name, 'expires')().toGMTString()
           : null);
      if (!!cookieExpires) { 
        cookieText += '; expires=' + cookieExpires; 
      }

      // Optionally add path part of cookie.
      var cookiePath = opt_path || getCookieProperty(name, 'path');
      if (!!cookiePath) {
        cookieText += '; path=' + cookiePath;
      }

      // Optionally add domain part of cookie.
      var cookieDomain = opt_domain || getCookieProperty(name, 'domain');
      if (!!cookieDomain) {
        cookieText += '; domain=' + cookieDomain;
      }

      SH.CookieService.writeCookie(cookieText);
    }
  };

  // Public functions (revealed)

  /**
   * Read cookie with passed-in name and return its value.
   *
   * @param {string} name Name of the cookie to read.
   * @return {?string} Value of cookie or null if the cookie does not exist.
   */
  var getCookiePublic = function(name) {
    var cookieName = encodeURIComponent(name) + '=';
    var documentCookie = SH.CookieService.readCookie();
    var cookieStart = documentCookie.indexOf(cookieName);
    var cookieValue = null;
                        
    if (cookieStart > -1) {
      cookieEnd = documentCookie.indexOf(';', cookieStart);

      if (cookieEnd === -1) {
        cookieEnd = documentCookie.length;
      }

      cookieValue = documentCookie.substring(
          cookieStart + cookieName.length,
          cookieEnd
        );
    }

    return cookieValue;
  };

  /**
   * Read subcookie with passed-in subname that is part of cookie with
   * the passed-in name, and return its value.
   *
   * @param {string} name Name of the cookie to read.
   * @param {string} subname Name of the subcookie to read.
   * @return {?string} Value of subcookie or null if the cookie does not exist.
   */
  var getSubcookiePublic = function(name, subname) {
    var subcookies = getAllSubcookies(name);

    if ((subcookies !== null) && subcookies[subname]) {
      return subcookies[subname];
    } 

    return null;
  };

  /**
   * Update cookie with passed-in name with a subcookie with the passed-in
   * subname and passed-in value.
   *
   * @param {string} name Name of the cookie with subcookies.
   * @param {string} subname Name of the subcookie to be updated.
   * @param {*} value Value of the subcookie to be updated.
   * @param {Date=} opt_expires Expiration date to set.
   * @param {string=} opt_path Path to set.
   * @param {string=} opt_domain Domain to set.
   */
  var setSubcookiePublic = function(name, subname, value, opt_expires, opt_path, opt_domain) {
    var subcookies = getAllSubcookies(name) || {};
    subcookies[subname] = value;
    setAllSubcookies(name, subcookies, opt_expires, opt_path, opt_domain);
  };

  return {
    // Public variables
    enabled: !!getCookiePublic('gc'),

    // Reveal public pointers to functions.
    getCookie: getCookiePublic,
    getSubcookie: getSubcookiePublic,
    setSubcookie: setSubcookiePublic
  };   

}();
