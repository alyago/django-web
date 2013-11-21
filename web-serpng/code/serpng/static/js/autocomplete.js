/*
 * Autocomplete, keywords and location suggestion.
 */

(function() {
  // Remove layerX and layerY.
  var all = $.event.props,
      len = all.length,
      res = [];
  while (len--) {
    var el = all[len];
    if (el != 'layerX' && el != 'layerY') {
      res.push(el);
    }
  }
  $.event.props = res;
}());

// Make sure SH namespace is defined.
var SH = SH || {};

// Make sure SH.autocomplete namespace is defined.
SH.autocomplete = {};

var current = 0;

SH.autocomplete.search = function() {
  var base_catalog_url = 'http://'+window.location.hostname+'/suggest/';
  var catalog_url = '';
  var geoip_info_url = 'http://'+window.location.hostname+'/a/catalog/geoipinfo';
  var kw_name = 'q';
  var lc_name = 'l';
  var dropdown_highlight_idx = 0;
  var atc_clk = false;

  return{
    bind: function($el) {
      if (kw_ac == true) {
        $('.id_f_keywords', $el).bind("click keyup", function(a) {
            SH.autocomplete.search.ac($(this), a);
          });
      }
      if (lc_ac == true) {
        $('.id_f_location', $el).bind("click keyup", function(a) {
            SH.autocomplete.search.ac($(this), a);
          });
      }
    },

    unbind: function($el) {
      if (kw_ac == true) {
        $('.id_f_keywords', $el).unbind("click keyup");
      }
      if (lc_ac == true) {
        $('.id_f_location', $el).unbind("click keyup");
      }
    },

    ac: function(e, a) {
      if (a.keyCode != 40 && a.keyCode != 38 && a.keyCode != 13) {
        current++;
        if (e.attr('name') == kw_name) {
          catalog_url = encodeURI(base_catalog_url+'keyword?term='+e.val());
          this.create_dropdown(e);
        }
        if (e.attr('name') == lc_name) {
          catalog_url = base_catalog_url + 'location?';	
          var area = e.data('atc_area');
          if (area == undefined) {
            $.get(geoip_info_url, function(result) {
                area = result;
                e.data('atc_area',result);
              });
          }
          catalog_url += encodeURI('ll=' + area + '&term=' + e.val());
          this.create_dropdown(e);
        }   
      } else {
        if (a.keyCode == 40) {
          this.nav_dropdown(e, 1); // Go down
        }
        if (a.keyCode == 38) {
          this.nav_dropdown(e, -1); // Go up
        }
        if (a.keyCode == 13) { 
          e.blur();
        }
      }
      
      // Use focusout after jQuery updated.
      e.blur(function() {
          if (!atc_clk) {
            $('#' + e.attr('name') + '_atc_dropdown').remove();
            dropdown_highlight_idx = 0;
          }
        });
    },

    nav_dropdown: function(e, offset) {
      var dd_items = $('.dropdown_item');

      if ($('.dropdown_item_hover').length == 0) {
        dropdown_highlight_idx = -1;
      }
      if (offset < 0 && dropdown_highlight_idx != -1) {
        if (dropdown_highlight_idx != 0) {
          dropdown_highlight_idx--;
        }
      } else if (offset > 0) {
        if (dropdown_highlight_idx != dd_items.length-1) {
          dropdown_highlight_idx++;
        }
	    }
      
      dd_items.removeClass('dropdown_item_hover');
	    dd_items.eq(dropdown_highlight_idx)
              .addClass('dropdown_item_hover');
	    e.val(dd_items.eq(dropdown_highlight_idx).text());
    },

    create_dropdown: function(e) {
    	var e_name = e.attr('name');
    	var dropdown_id = e_name + '_atc_dropdown';
    	var dropdown = $('#' + dropdown_id);
    	var box_width = e.outerWidth();
    	if ($.trim(e.val()) == '' && dropdown.length != 0) {
        dropdown.hide();
      } else if ($.trim(e.val())!='') {
        $.ajax({
          url: catalog_url,
          data: { current:current },
          success: function(result) {
            if (result[0] == current) {
              if (result[1].length > 0) {
                var html = [];
                // The extra enclosing <div> fixes absolute positioning issues in IE7.
                html.push('<div><div id="' + dropdown_id + '" class="atc_dropdown" style="width:' + box_width + 'px;">');
                $.each(result[1], function(i) {
                  html.push('<div class="dropdown_item" name="' + i + '"><a>' + result[1][i] + '</a></div>');
                });
                html.push('</div></div>');
                html = html.join('');
                if (dropdown.length == 0) {
                  e.after(html);
                } else {
                  dropdown.replaceWith(html);
                }
          
                $('.dropdown_item').hover(
                  function() {
                    $(".dropdown_item_hover").removeClass("dropdown_item_hover");
                    $(this).addClass("dropdown_item_hover");
                    //use $(this).index() after jquery version updated, remove div name
                    //dropdown_highlight_idx = $(this).index();
                    dropdown_highlight_idx = parseInt($(this).attr('name'));
                  },
                  function() { 
                    $(this).removeClass("dropdown_item_hover");
                  }
                );
                $('.dropdown_item').mousedown(function() { 
                    atc_clk = true;
                  }
                );
                $('.dropdown_item').mouseup(function() {
                    e.val($(this).text());
                    $(this).parent().hide();
                    atc_clk = false;
                    e.focus();
                  }
                );
              } else if (dropdown.length != 0) {
                dropdown.hide();
              }
            }   
          },
          dataType:'json'
        });
      }     
    }
  }
}();
