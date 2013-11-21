$(function(e) { //document.ready
  
  // Load header links via Ajax call for SEO purposes
  SH.get_links('/employer-api-' + emp_link, function(data) {
    if (data) {
      for (var code in data) {
        $('.employer-soc-'+code).attr('href', data[code]);
      }  
    } 
  });
});
