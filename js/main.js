(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);
    
    // Initiate WOW.js for entrance animations
    new WOW().init();

    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        items: 1,
        smartSpeed: 1000,
        dots: true,
        loop: true,
        margin: 25,
        nav: true,
        navText: [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

    // Facts counter with CounterUp
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 1500
    });

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }

        // Active Navigation Scrollspy effect
        var scrollPos = $(document).scrollTop() + 200;
        $('.navbar-nav .nav-link').each(function () {
            var currLink = $(this);
            var refElement = $(currLink.attr("href"));
            if (refElement.length) {
                if (refElement.position().top <= scrollPos && refElement.position().top + refElement.outerHeight() > scrollPos) {
                    $('.navbar-nav .nav-link').removeClass("active");
                    currLink.addClass("active");
                }
            }
        });
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1000, 'easeInOutExpo');
        return false;
    });

    // Smooth scrolling for navigation anchors
    $('.navbar-nav a[href^="#"]').on('click', function (e) {
        var target = $($(this).attr('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 20
            }, 800, 'easeInOutExpo');
            $('.navbar-nav .nav-link').removeClass('active');
            $(this).addClass('active');
        }
    });

})(jQuery);
