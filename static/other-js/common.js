(function(){

	var $slider = $('.l-slider').unslider({
		delay: 5000,
		autoplay: true,
		infinite: true,
        arrows: false
    });

	$('.l-slider .l-prev-btn').click(function(e) { $slider.unslider('prev');  });
	$('.l-slider .l-next-btn').click(function() { $slider.unslider('next'); });

})();
