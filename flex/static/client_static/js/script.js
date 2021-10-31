/* global initMap:true */

initMap = false;

(function (fn) {
    if (typeof jQuery === 'undefined') {
        throw 'Requires jQuery to be loaded first';
    }
    fn(jQuery);
}(function ($) {
    "use strict";

    var $body = $('body');

    // detect animation events
    var animationEnd = (function(el) {
        var animations = {
            animation: 'animationend',
            OAnimation: 'oAnimationEnd',
            MozAnimation: 'mozAnimationEnd',
            WebkitAnimation: 'webkitAnimationEnd',
        };
        for (var t in animations) {
            if (el.style[t] !== undefined) {
                return animations[t];
            }
        }
    })(document.createElement('div'));

    //Toggle main navigation
    $('.navbar-toggler').on('click', function(e){
        e.preventDefault();
        $(this).toggleClass('active')
            .closest('.header').toggleClass('active');
    });
    //Toggle sub navigation
    $('[data-role="nav-toggler"], .nav-arrow').on('click', function(e){
        e.preventDefault();
        $(this).parent().toggleClass('active');
    });
    //Toggle extra navigation
    $('[data-role="nav-self-toggle"]').on('click', function(e){
        e.preventDefault();
        $(this).toggleClass('active');
    });

    // Scroll Top
    var checkScroll = function(){
        if ( $(window).scrollTop() > 0 ) {
            $('.scroll-top').removeClass('disabled');
            if( (window.innerHeight + window.scrollY) >= document.body.offsetHeight ){
                $('.scroll-top').addClass('end');
            }else{
                $('.scroll-top').removeClass('end');
            }
        }else{
            $('.scroll-top').addClass('disabled');
        }
    };
    checkScroll();
    $(window).on('scroll resize orientationchange focus', checkScroll);
    $('.scroll-top').on('click', function(e){
        e.preventDefault();
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    });

    // Magnific Popup
    $('[data-magnific-popup]').each(function(i, el){
        var $el = $(el),
            popType = $el.data('magnificPopup')
        ;
        $el.magnificPopup({
            type: popType === true ? 'image' : popType,
            titleSrc : 'title'
        });
    });

    // Waypoint Counters
    $('[data-waypoint-counter]').each(function(i, el){
        $(el).waypoint({
            handler : function() {
                $(el).prop('CounterValue',0).animate({
                    CounterValue: $(el).data('waypointCounter')
                }, {
                    duration: 2000,
                    step : function (now) {
                        $(this).text(Math.ceil(now));
                    }
                });
                this.destroy();
            },
            offset : 'bottom-in-view'
        });
    });
    
    // Svg loader
    $('[data-svg]').each(function(i, el){
        var $el = $(el);
        $el.load($el.data('svg'));
    });

    // Cover image
    $('[data-image-cover]:not(.cover)').each(function (i, el){
        var $el = $(el);
        $el.addClass('d-none').after(
            $('<span>').addClass('image-cover').css('backgroundImage', "url(" + $el.attr('src') + ")" )
        );
    });

    // Horizontal image
    $('[data-image-horizontal]:not(.horizontal)').each(function (i, el){
        var $el = $(el);
        $el.addClass('d-none').after(
            $('<span>').addClass('image-horizontal').css('backgroundImage', "url(" + $el.attr('src') + ")" )
        );
    });

    // Trigger resize for parallax blocks
    $('[data-parallax]').each(function(i, el){
        new Waypoint({
            element: el,
            handler: function() {
                $(window).trigger('resize');
            },
            offset : '100%'
        });
    });

    // Add show/hide classes to elements to make CSS3 animation
    var showFn = function($el, showSel, hideSel){
            $el.find(hideSel || '[data-hide-class]').trigger(animationEnd);
            $el.find(showSel || '[data-show-class]').each(function(){
                $(this).addClass($(this).data('showClass'));
            });
        },
        hideFn = function($el, showSel, hideSel){
            $el.find(showSel || '[data-show-class]').each(function(){
                $(this).removeClass($(this).data('showClass'));
            });
            $el.find(hideSel || '[data-hide-class]')
                .each(function(){
                    $(this).addClass($(this).data('hideClass'));
                })
                .on(animationEnd, function(){
                    $(this)
                        .off(animationEnd)
                        .removeClass($(this).data('hideClass'))
                    ;
                })
            ;
        }
    ;

    // Element hover with CSS3 animation
    $body
        .on('mouseover', '[data-role="hover-wrap"]', function(){
            showFn($(this));
        })
        .on('mouseleave', '[data-role="hover-wrap"]', function(){
            hideFn($(this));
        })
    ;

    // Slick carousel
    var slickViews = {},
        addSlickView = function (name, data){
            var view = {};
            view.options = data.options || {};
            view.preInit = data.preInit || $.noop;
            view.name = name;
            slickViews[name] = view;
            return view;
        },
        getSlickViews = function (views){
            var list = [],
                ignoreViews = {},
                viewNames, i
            ;
            if(typeof views === 'string'){
                viewNames = views.split(' ');
                for (i = 0; i < viewNames.length; i++) {
                    if( slickViews[viewNames[i]] && !ignoreViews[viewNames[i]] ){
                        ignoreViews[viewNames[i]] = true;
                        list.push(slickViews[viewNames[i]]);
                    }
                }
            }
            return list.length ? list : false;
        },
        getSlick = function (name){
            var $carousel = $('[data-slick-name=' + name + ']');
            if( $carousel.length ){
                var $carouselSlidest = $carousel.find('.slick-slides');
                $carousel = $carouselSlidest.length ? $carouselSlidest : $carousel;
                return $carousel;
            }
            return $([]);
        },
        createSlickView = function ($el, views, options){
            var viewsList = getSlickViews(views),
                opts = options || {},
                viewOpts = [{
                    swipeToSlide : true,
                    infinite : true
                }],
                i
            ;
            for (i = 0; i < viewsList.length; i++) {
                viewOpts.push(viewsList[i].options);
            }
            viewOpts.push(opts);
            opts = $.extend.apply($, viewOpts);
            for (i = 0; i < viewsList.length; i++) {
                viewsList[i].preInit($el, opts, viewsList[i]);
            }
            var $carousel = $el.find('.slick-slides');
            if( !$carousel.length ){
                $carousel = $el;
            }
            if( !opts.asNavFor && $el.data('slickFor') ){
                var $forCarousel = getSlick($el.data('slickFor'));
                if( $forCarousel.length ){
                    opts.asNavFor = $forCarousel;
                    // set asNavFor for the other carousel too, but make sure it's initiated all slick carousels
                    setTimeout(function(){
                        $forCarousel.slick('slickSetOption', 'asNavFor', $carousel);
                    });
                }
            }
            $carousel.slick(opts);
            // reset iframe if any to stop youtube video, etc.
            $carousel.on('beforeChange', function(event, slick, currentSlide){
                var $iframes = slick.$slider.find('.slick-current iframe');
                $iframes.each(function(i, el){
                    var $el = $(el),
                        src = $el.attr('src');
                    $el.attr('src', '');
                    $el.attr('src', src);
                });
            });
        }
    ;

    // Slick autoplay
    addSlickView('autoplay', {
        options : {
            autoplay : true,
            autoplaySpeed : 5000
        }
    });

    // Slick view with custom arrows navigation
    addSlickView('navigation', {
        preInit : function ($el, opts) {
            opts.nextArrow = $el.find('.slick-arrow-next');
            opts.prevArrow = $el.find('.slick-arrow-prev');
        }
    });

    // Slick view with dots navigation
    addSlickView('dots', {
        options : {
            dots: true
        }
    });

    // Slick center mode with no side padding
    addSlickView('center-no-gutters', {
        options : {
            centerMode : true,
            centerPadding : 0
        }
    });

    // Slick focusable slides
    addSlickView('selectable', {
        options : {
            focusOnSelect: true
        }
    });

    // Slick single slide view
    addSlickView('single', {
        options : {
            slidesToShow : 1
        }
    });

    // Slick view with dots navigation
    addSlickView('no-arrows', {
        options : {
            arrows : false
        }
    });

    // Slick responcive views
    addSlickView('responsive-2', {
        options : {
            slidesToShow : 2,
            responsive : [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow : 1
                    }
                }
            ]
        }
    });

    addSlickView('responsive-3', {
        options : {
            slidesToShow : 3,
            responsive : [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow : 1,
                        swipe : true,
                    }
                }
            ]
        }
    });

    addSlickView('responsive-4', {
        options : {
            slidesToShow : 4,
            responsive : [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow : 3
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow : 2
                    }
                },
                {
                    breakpoint: 576,
                    settings: {
                        slidesToShow : 1
                    }
                }
            ]
        }
    });

    addSlickView('responsive-9', {
        options : {
            slidesToShow : 9,
            responsive : [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow : 7
                    }
                },
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow : 5
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow : 3
                    }
                },
                {
                    breakpoint: 576,
                    settings: {
                        slidesToShow : 2
                    }
                },
                {
                    breakpoint: 380,
                    settings: {
                        slidesToShow : 1
                    }
                }
            ]
        }
    });

    addSlickView('responsive-6', {
        options : {
            slidesToShow : 6,
            responsive : [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow : 5
                    }
                },
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow : 5
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow : 3
                    }
                },
                {
                    breakpoint: 576,
                    settings: {
                        slidesToShow : 2
                    }
                },
                {
                    breakpoint: 390,
                    settings: {
                        slidesToShow : 1
                    }
                }
            ]
        }
    });

    // Slick static view, to be controlled over other slick carouse
    addSlickView('controlled', {
        options : {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows : false,
            draggable : false,
            fade: true,
            swipe : false
        }
    });

    // Slick with navigation over draging
    addSlickView('single-drag', {
        options : {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows : false,
            fade: true
        }
    });

    // Slick vertical view
    addSlickView('vertical', {
        options : {
            slidesToShow: 3,
            slidesToScroll: 1,
            vertical : true,
            verticalSwiping : true,
            focusOnSelect: true
        }
    });

    $('.slick-carousel').each(function(i, el){
        var $el = $(el);
        createSlickView($el, $el.data('slickView'));
    });

    /* Google Maps */
    initMap = function (){
        // Create a new StyledMapType object, passing it an array of styles,
        // and the name to be displayed on the map type control.
        var styledMapType = new google.maps.StyledMapType(
            [
                {
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#f5f5f5"
                    }
                    ]
                },
                {
                    "elementType": "labels.icon",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#616161"
                    }
                    ]
                },
                {
                    "elementType": "labels.text.stroke",
                    "stylers": [
                    {
                        "color": "#f5f5f5"
                    }
                    ]
                },
                {
                    "featureType": "administrative.land_parcel",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#bdbdbd"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#757575"
                    }
                    ]
                },
                {
                    "featureType": "poi.park",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#e5e5e5"
                    }
                    ]
                },
                {
                    "featureType": "poi.park",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#9e9e9e"
                    }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#ffffff"
                    }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#757575"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#dadada"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#616161"
                    }
                    ]
                },
                {
                    "featureType": "road.local",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#9e9e9e"
                    }
                    ]
                },
                {
                    "featureType": "transit.line",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#e5e5e5"
                    }
                    ]
                },
                {
                    "featureType": "transit.station",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#c9c9c9"
                    }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#9e9e9e"
                    }
                    ]
                }
            ],
            {name: 'Styled Map'});

        // Create a map object, and include the MapTypeId to add
        // to the map type control.
        $('.gmap').each(function(i, el){
            var $el = $(el),
                data = $el.data(),
                mark = {lat: data.lat, lng: data.lng},
                centredAt = 992,
                offset = $(window).width() >= centredAt ? 0.01 : 0,
                center = {lat: data.centerLat || (mark.lat), lng: data.centerLng || (mark.lng + offset)},
                map = new google.maps.Map(el, {
                    center: center, // map center position
                    zoom: data.zoom || 15,
                    scrollwheel: false,
                    zoomControl: true,
                    zoomControlOptions: {
                      position: google.maps.ControlPosition.LEFT_CENTER
                    },
                    streetViewControl: true,
                    streetViewControlOptions: {
                      position: google.maps.ControlPosition.LEFT_BOTTOM
                    },
                    mapTypeControlOptions: {
                        mapTypeIds: ['roadmap', 'satellite', 'hybrid', 'terrain', 'styled_map']
                    }
                })
            ;

            new google.maps.Marker({
              position: mark,
              map: map,
              icon: data.marker || "./images/parts/map-marker.png"
            });

            // Associate the styled map with the MapTypeId and set it to display.
            map.mapTypes.set('styled_map', styledMapType);
            map.setMapTypeId('styled_map');
            // Center map on resize
            $(window).on('resize', function(){
                google.maps.event.trigger(map, 'resize');
                offset = $(window).width() >= centredAt ? 0.01 : 0;
                center = {lat: data.centerLat || (mark.lat), lng: data.centerLng || (mark.lng + offset)};
                map.setCenter(center);
            });
        });
    };
}));