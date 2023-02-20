(function ($) {

  "use strict";

    // PRE LOADER
    $(window).load(function(){
      $('.preloader').fadeOut(1000); // set duration in brackets    
    });


    // ABOUT SLIDER
    $('body').vegas({
        slides: [
            { src: 'static/scrape_engine/images/slide-image01.jpg' },
            { src: 'static/scrape_engine/images/slide-image02.jpg' },
            { src: 'static/scrape_engine/images/slide-image03.jpg' },
        ],
        timer: false,
        transition: [ 'zoomOut', ]
    });

})(jQuery);
