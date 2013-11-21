// Balloon / tooltip manager.
SH.balloon = function() {
  return {
    /*
     * Initialize balloon.
     * @param {Object} $target target jQuery object.
     * @param {Object} $content content to display inside balloon.
     * @param {Object=} opt_css Optional css overrides.
     * @param {string=} opt_position Optional position override (default is bottom).
     * @param {number=} opt_offset_x Optional x-offset (default is 0).
     * @param {number=} opt_offset_y Optional y-offset (default is 0).
     */
    init: function($target, $content, opt_css, opt_position, opt_offset_x, opt_offset_y, opt_delay, opt_min_lifetime) {
      // Default style.
      var css = {
        backgroundColor: '#fff',
        border: 'solid 1px #999',
        borderRadius: '2px',
        boxShadow: '2px 2px 4px #999',
        minWidth: '110px',
        opacity: 1,
        padding: '7px'
      };

      // Mixin optional css overrides.
      $.extend(css, opt_css);

      var $balloon = $target.balloon({
        css: css,
        contents: $content,
        hideAnimation: function (d) { this.fadeOut(d); },
        minLifetime: opt_min_lifetime || 750,
        position: opt_position || 'bottom',
        showAnimation: function (d) { this.fadeIn(d); },
        offsetX: opt_offset_x || 0,
        offsetY: opt_offset_y || 0,
        delay: opt_delay || 0
      }).click(function() {
        // Always show on click.
        $content.show();
        $(this).showBalloon();
      }).hover(
        // Handle mouse enter.
        function() {
          $content.show();
          // Send an explicit mouseover event to force centering logic to fire. (wat?)
          $content.mouseover();
        },
        // Handle mouse exit.
        function() {
        }
      );

      // Hide the balloon on window resize.
      $(window).resize(function() {
        $balloon.hideBalloon();
      });
    }
  };
}();
