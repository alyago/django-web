$(function(e) { //document.ready

  // Load header links via Ajax call for SEO purposes
  SH.get_links('/base/api/header_links', function(data) {
    if (data) {
      $('.user_login').attr('href', data['signin-link']);
    }
  });

  // US account dropdown 'balloon' function
  SH.balloon.init(
    $('.account_menu', '.js_sh_header'),
    $('.account_menu_content', '.js_sh_header'));

  // Search options dropdown 'balloon' function
  SH.balloon.init(
      $('.options_menu', '.js_sh_header'),
      $('.options_menu_content', '.js_sh_header'));
});

