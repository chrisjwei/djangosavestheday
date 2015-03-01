function resizeContent() {
    $height = $(window).height();
    $('body .banner').height($height);
    $('body .banner .overlay').css("top",($height/4 - 100));
}

function indexTransition(){
	$('#one').fadeOut(300, function(){ $(this).remove(); indexTransition2()});
}

function indexTransition2(){
	$('#two').fadeIn(300,function(){});
}

$(document).ready(function(){
		$('#two').hide();
    resizeContent();
    setRandomBackgroundImage();

    $(window).resize(function() {
        resizeContent();
    });

    $('a[href^="#"]').on('click',function (e) {
	    e.preventDefault();

	    var target = this.hash;
	    var $target = $(target);

	    $('html, body').stop().animate({
	        'scrollTop': $target.offset().top
	    }, 900, 'swing', function () {
	        window.location.hash = target;
	    });
	});
});
