/*
 * POM - Creative Coming Soon Template
 * Build Date: June 2015
 * Author: Madeon08
 * Copyright (C) 2015 Madeon08
 * This is a premium product available exclusively here : http://themeforest.net/user/Madeon08/portfolio
 */

/*  TABLE OF CONTENTS
    ---------------------------
    1. Notification / Text / Tone
    2. Loading
    3. Countdown
    4. Newsletter
    5. Photo gallery
    6. Navigation / Slide
*/

/*
 * Notification / Text / Tone
 */

 function checkForChanges() {
    if ($('.content-message').hasClass('active-slide'))
        
        setTimeout(function() {

            $('.notification').addClass('opacity-0').removeClass('fadeIn'),
            $('#text-alert').text('Enjoy your visit...').addClass('fadeIn')

        }, 300);

    else
        setTimeout(checkForChanges, 500);
}

$(window).load(function() {

    $('#text-alert').text('Someone is writing you...');

    $('a.messages').addClass('ion-chatbubble-working').removeClass('');

    setTimeout(function() {
        $('#text-alert').text('Look! You received 1 new message.').addClass('fadeIn');
        $('.notification').addClass('fadeIn').removeClass('opacity-0');
        $('a.messages').addClass('icon-popup').removeClass('ion-chatbubble-working');

        // Uncomment the next lines if you want the waiting before the notification, see below the other commented part.
        // $('a.icon-popup').on('click', function() {
        //     $("#main").fadeOut( "600", "linear" );
        // });

        var audioElement = document.createElement('audio');
        audioElement.setAttribute('src', 'assets/tone/note.m4r');
        audioElement.setAttribute('autoplay', 'autoplay');
        //audioElement.load()

       // $.get();

        audioElement.addEventListener("load", function() {
            audioElement.play();
        }, true);

        audioElement.play();

        // Message can be open only when the notification "1" is appeared if you uncomment the next lines, remove also the lines in $(document).ready(function() {.
        // $("a.messages").click(function() {
        //     $(".content-message").addClass('active-slide');
        //     $(".slider-nav").addClass('active-nav');
        // });

        $(checkForChanges);

    }, 2500);

    /*
    * Loading
    */
    $('.loading-part').fadeOut();

});

$(document).ready(function() {

    /*
    * Countdown
    */

    // Set you end date just below
    $('#countdown_dashboard').countDown({
        targetDate: {
            'day': 31,
            'month': 12,
            'year': 2016,
            'hour': 11,
            'min': 13,
            'sec': 0
        },
        omitWeeks: true
    });

    /*
    * Newsletter
    */
    $("#notifyMe").notifyMe();

    /*
     * Photo gallery
     */
    $('.swipebox').swipebox();

    /* Video */
    $('.swipebox-video').swipebox();

    /*
     * Navigation / Slide
     */

    function prevNavigation() {
        //prev slide function
        var currentSlide = $('.active-slide');
        var prevSlide = currentSlide.prev('.slide');
        $('.slide').animate({ scrollTop:0 }, 'fast');

        // Slide loop, go back to the last
        if (prevSlide.length === 0) {
            prevSlide = $('.slide').last();
        }

        // Disable loop
        // if (prevSlide.length === 0) {
        //     prevSlide = $('.slide').first();
        // }

        currentSlide.removeClass('active-slide');
        prevSlide.addClass('active-slide');
    }

    function nextNavigation() {
        //next slide function
        var currentSlide = $('.active-slide');
        var nextSlide = currentSlide.next('.slide');
        $('.slide').animate({ scrollTop:0 }, 'fast');

        // Slide loop, go back to the first
        if (nextSlide.length === 0) {
            nextSlide = $('.slide').first();
        }

        // Disable loop
        // if (nextSlide.length === 0) {
        //     nextSlide = $('.slide').last();
        // }

        currentSlide.removeClass('active-slide');
        nextSlide.addClass('active-slide');   
    }

    $('.prev-button').click(function() {

        prevNavigation();

     });

    $('.next-button').click(function(e) {

        nextNavigation();

    });

    $('a.icon-popup').on('click', function() {
        $("#main").fadeOut( "600", "linear" );
        $(".slider-nav").addClass('active-nav');
    });

    $("a.messages").click(function() {
        $(".content-message").addClass('active-slide');
    });

    $("a.about").click(function() {
        $(".content-about").addClass('active-slide');
    });

    $("a.photos").click(function() {
        $(".content-photos").addClass('active-slide');
    });

    $("a.close-content").click(function() {
        $(".global-content section").removeClass('active-slide');
        $(".slider-nav").removeClass('active-nav');
        $("#main").fadeIn( "600", "linear" );
        $('.slide').animate({ scrollTop:0 }, 'fast');
    });

    if (window.matchMedia("(min-width: 1025px)").matches) { 
            
        $(function () { $("[data-toggle='tooltip']").tooltip(); });

    }

});