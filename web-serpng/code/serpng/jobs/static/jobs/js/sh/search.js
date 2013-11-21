// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class Search form handler.
 */
SH.search = function() {
  // Private variables.
  // Search url path base.
  var search_base_url = '/a/jobs/list';

  // Private functions.
  /**
   * Return value of the input field in the top search form
   * with class equal to the passed-in string.
   * 
   * @param {string} class_name Name of class of input field.
   * @return {string|undefined} Value of the input field.
   */
  var get_input_value = function(class_name, $form) {
    var input_value = $(class_name, $form).val();
    if (input_value) {
      return urlencode(input_value);
    }
  };

  /**
   * Handle submits in search forms.
   *
   * @param {Event} e jQuery event object for the submit event.
   */
  var submit = function(e) {
    e.preventDefault();

    var $form = $(e.target).closest('.search_form');
    if (!$form) {
      return false;
    }

    // Remove any placeholder fallback text in the search boxes.
    $('.id_f_keywords', $form).placeholderFallback('remove');
    $('.id_f_location', $form).placeholderFallback('remove');

    // Get keywords, location, and miles radius.
    var keywords = get_input_value('.id_f_keywords', $form);
    var location = get_input_value('.id_f_location', $form);
    var miles = get_input_value('.id_f_miles', $form);

    // Build new search url.
    var search_url_parts = [SH.search.url];
    if (keywords) {
      search_url_parts.push('q-' + keywords);
    }
    if (location) {
      search_url_parts.push('l-' + location);
    }
    if (miles && location) {
      search_url_parts.push('mi-' + miles);
    }
    var search_url = search_url_parts.join('/');

    // Navigate to the new search url.
    SH.NavigationService.navigateTo(search_url);
  };

  /**
   * Custom urlencode.
   *
   * @param {string} value String to be url encoded.
   * @return {string} Url-encoded string.
   */
  var urlencode = function(value) {
    if (!value) {
      return '';
    }

    // Remove leading/trailing whitespace.
    value = value.replace(/(^\s+|\s+$)/g,''); 

    // Collapse multiple whitespace.
    value = value.replace(/\s+/g,' ');

    // Call encodeURIComponent().
    value = encodeURIComponent(value);

    // Convert "%20" to "+".
    value = value.replace(/%20/g,'+');

    return value;
  };

  return {
    // Public variables.
    // TODO(yiping): when the rest of serp.js has been refactored with
    //   unit tests, move SH.search.url into a SH.globals object that 
    //   contains constants like these that are used by multiple SH objects.
    //   SH.search.url is currently used by several other SH objects.
    url: search_base_url,

    // Public functions.
    /**
     * Initialize event handler for top search form submit.
     */
    init: function() {
      $('.search_form').each(function() {
        $(this).submit(submit);
      });
    }
  };

}();
