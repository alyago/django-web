// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class signin lightbox.
 *
 * Lightbox to allow users to signin or create an account.
 */
SH.SigninLightbox = function() {

  // Private variables

  // Messages to display in the dialog.
  var messages = {
    'default': 'To continue you must:',
    'savejob': 'To save this job, please:'
  }

  // jQuery variables.
  var $close_box = $('.dialog_close');
  var $message = $('.dialog_main_msg');
  var $links = $('.dialog_link');


  // Private functions

  /**
   * Closes the Fancybox.
   * @return {boolean} false for some reason probably relating to event handling.
   */
  var close = function() {

    // Make sure the fancybox javascript is loaded.
    if (!!$.fancybox) {
      $.fancybox.close();
    }
    return false;
  };


  // Public functions
  
  /**
   * Public interface to open the lightbox.
   * @param {string} message The message to display.
   * */
  var openPublic = function(messageCode) {
    if (!messageCode || !(messageCode in messages)) {
      messageCode = 'default';
    } else {

      // Set the message parameter in the links.
      $links.each(function() {
        var _href = $(this).attr('href');
        $(this).attr('href', _href + '&m=' + encodeURIComponent(messageCode));
      });
    }

    // Set the message in the lightbox.
    $message.text(messages[messageCode]);

    // Load Fancybox and create dialog.
    SH.fancybox(function() {
      $.fancybox.open([{
        helpers: {
          overlay: {
            closeClick: true,
            locked: false
          }
        },
        href: "#signin_dialog"
      }], {
        padding: 0
      });

      // Delegated event handler for clicks on the close button.
      $close_box.on('click', close); 
      
    });
  };

  return {
    // Reveal public pointers to functions.
    open: openPublic
  };
}();
