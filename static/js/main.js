$(document).ready(function(){
	$('.event_elem').each(function(){
		var today = new Date();
		today.setHours(0, 0, 0, 0);
		var ymd = $(this).find('.event_container').attr('data-date').split("/");
		var that_day = new Date(ymd[0], ymd[1]-1, ymd[2]);

		var one = 24*60*60*1000;
		var diff = Math.abs((today.getTime() - that_day.getTime())/(one));
		var d_day = $(this).find('.d_day');

		if(diff < 1) {
			diff = "NOW";
			d_day.addClass('now');
		}
		else {
			diff = "D-" + diff;
		}

		d_day.text(diff);
	});
});
