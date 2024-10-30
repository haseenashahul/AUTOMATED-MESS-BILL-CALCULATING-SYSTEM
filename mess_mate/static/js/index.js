$.fn.jQuerySimpleCounter = function(options) {
    var settings = $.extend({
        start:  0,
        end:    100,
        easing: 'swing',
        duration: 400,
        complete: ''
    }, options );

    var thisElement = $(this);

    $({count: settings.start}).animate({count: settings.end}, {
        duration: settings.duration,
        easing: settings.easing,
        step: function() {
            var mathCount = Math.ceil(this.count);
            thisElement.text(mathCount);
        },
        complete: settings.complete
    });
};

// Get values from the HTML elements rendered by Django
var activeUsersCount = parseInt($('#number1').text(), 10);
var registeredUsersCount = parseInt($('#number2').text(), 10);
var pastUsersCount = parseInt($('#number3').text(), 10);

// Animate counters using the dynamic values
$('#number1').jQuerySimpleCounter({end: activeUsersCount, duration: 3000});
$('#number2').jQuerySimpleCounter({end: registeredUsersCount, duration: 3000});
$('#number3').jQuerySimpleCounter({end: pastUsersCount, duration: 2000});
// $('#number4').jQuerySimpleCounter({end: 246, duration: 2500});  // Keeping this static for the DUES count

/* AUTHOR LINK */
$('.about-me-img').hover(function(){
    $('.authorWindowWrapper').stop().fadeIn('fast').find('p').addClass('trans');
}, function(){
    $('.authorWindowWrapper').stop().fadeOut('fast').find('p').removeClass('trans');
});
