$(document).ready(function(){
	$('.event_container').click(function(){
		window.location.href = "/article/" + $(this).attr('article-id');
	});
});
