// Make sure SH namespace is defined.
var SH = SH || {};

SH.feedback_survey = function() {
  return {
    openSurveyWindow: function(surveyUrl) {
      var windowWidth = $(window).width();
      var windowHeight = $(window).height();

      var surveyWidth = windowWidth / 3; // Popup window 1/3 the window width.
      var surveyHeight = windowHeight * (3 / 4); // Popup window 3/4 the window height.

      var screenLeft = (windowWidth - surveyWidth) / 2;
      var screenTop = windowHeight / 5;

      if(typeof window.screenLeft !== 'undefined') {
        screenLeft += window.screenLeft;
        screenTop += window.screenTop;
      } else if(typeof window.screenX !== 'undefined') {
        screenLeft += window.screenX;
        screenTop += window.screenY;
      }

      var windowFeatures = 'left=' + screenLeft + ', top=' + screenTop + ', width=' + surveyWidth + ', height=' + surveyHeight + ', resizable, scrollbars'; 
      var surveyWindow = window.open(surveyUrl, 'persistentFeedbackSurveyWindow', windowFeatures);
      return false;
    }
  };
}();
