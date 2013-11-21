$(function(e) { //document.ready

  // Load header links via Ajax call for SEO purposes
  SH.get_links('/base/api/footer_links', function(data) {
    if (data) {
      $('.footer_privacy').attr('href', data.footer_privacy);
      $('.footer_terms').attr('href', data.footer_terms);

      $('#gplus_img').attr('href', data.gplus_img);
      $('#linkedin_img').attr('href', data.linkedin_img);
      $('#facebook_img').attr('href', data.facebook_img);
      $('#twitter_img').attr('href', data.twitter_img);
      $('#youtube_img').attr('href', data.youtube_img);
   
      // Populate international dropdown HTML and initialize drop-up.   
      $('body').append(data.intl_dropdown_html);
      SH.balloon.init($('#l_simplyhired_intl'), $('#c_simplyhired_intl'), {}, 'top', 0, 0, 0, 100);
    }
  });
});
