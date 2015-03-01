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

    $(window).resize(function() {
        resizeContent();
    });
});
