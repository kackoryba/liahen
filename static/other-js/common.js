(function(){

	var $slider = $('.l-slider').unslider({
		delay: 10 * 1000, // 10 seconds
		autoplay: true,
		infinite: true,
        arrows: false
    });

	$('.l-slider .l-prev-btn').click(function(e) { $slider.unslider('prev');  });
	$('.l-slider .l-next-btn').click(function() { $slider.unslider('next'); });

	$('#login-dropdown').prepend(" <span class='glyphicon glyphicon-user'></span>");
})();
