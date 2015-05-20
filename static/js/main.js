$(document).ready(function(){
	$('.event_elem').each(function(){
		var today = new Date();
		today.setHours(0, 0, 0, 0);
		var ymd = $(this).find('.event_container').attr('data-date').split("/");
		var that_day = new Date(ymd[0], ymd[1]-1, ymd[2]);

		var one = 24*60*60*1000;
		var diff = Math.abs((today.getTime() - that_day.getTime())/(one));

		if(diff < 1) {
			diff = "NOW";
		}
		else {
			diff = "D-" + diff;
		}

		$(this).find('.d_day').text(diff);
	});
});
