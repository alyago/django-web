/*
 * Placeholder fallback jQuery widget. Used by SH.placeholder_fallbacks.
 */
(function($) {
  $.widget("sh.placeholderFallback", {

    //
    // Default options.
    //

    options: {
      placeholderClass: 'placeholder',
      placeholderText: undefined
    },

    //
    // Private helper methods.
    //

    // Reset text input value to empty string, remove placeholder class.
    _clearInput: function() {
      if (this.element.hasClass(this.options.placeholderClass)) {
        this.element.val('');
        this.element.removeClass(this.options.placeholderClass);
      }
    },

    // Replace text input value with placeholder text, add placeholder class.
    _fillInput: function() {
      if (this.element.val() === '') {
        this.element.val(this.options.placeholderText);
        this.element.addClass(this.options.placeholderClass);
      }
    },

    // jQuery widget constructor.
    _create: function() {
      // Only activate if the browser doesn't support placeholders on input.
      if (window.Modernizr && !Modernizr.input.placeholder) {
        // If the element has a placeholder attribute, use that as the default text.
        // The placeholderText option can be used as an override.
        this.options.placeholderText = this.options.placeholderText || this.element.attr('placeholder') || '';

        // If the form inputs is empty, populate it with placeholder text.
        this._fillInput();

        // On focus, clear instructions
        this.element.bind('focus', $.proxy(this._clearInput, this));

        // On blur, re-display instructions
        this.element.bind('blur', $.proxy(this._fillInput, this));
      }
    },

    //
    // Publicly available methods.
    //

    // Remove any placeholder fallback text. Usually called prior to form submission.
    remove: function() {
      if (window.Modernizr && !Modernizr.input.placeholder) {
        this._clearInput();
      }
    }
  });
})(jQuery);
