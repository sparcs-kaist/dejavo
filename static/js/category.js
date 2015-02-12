$(document).ready(function(){
	var $main_list = $('#main_list');
	
	var padZero = function padZero(s, l){
		for(s+=''; s.length<l; s='0'+s); return s;
	};

	var toDisplayDate = function toDisplayDate(d){
		if(!d) return '?/??';
		var s = (d.getMonth()+1)+'/'+padZero(d.getDate());
		var h = d.getHours()%12; if(h==0) h=12;
		s += ' '+h+(d.getHours()>=12?'PM':'AM');
		return s;
	};

	var $current_button = null;

	$('#category_list button').click(function(){
		var category_name = this.innerText;
		if($current_button) $current_button.removeClass('toggled');
		($current_button = $(this)).addClass('toggled');
		$.get("/category/"+this.value+"/?accept=application/json", function(data){
			$main_list.empty();
			var elems = [],
				now = Date.now();
			if(data && data.articles){
				elems = data.articles.map(function(article){
					var i, d=null,
						$main_elem = $("<div class='elem'/>"),
						$poster_div = $("<div class='poster'></div>"),
						$img = $("<img/>").attr({'src':article.poster, 'alt':article.title}).load(function(){;
							var scaled_width = this.width * 317/this.height;
							var cell_size = Math.round(scaled_width/223);
							if(cell_size >= 2) $main_elem.addClass('elem_wide');
							$poster_div.append($img);
						});

					$main_elem.append($poster_div);
					
					for(i=0; i<article.timeslot.length; i++){
						d = new Date(article.timeslot[i].start_time);
						if(d.getTime() >= now) break;
					}

					var today = new Date(86400e3*Math.floor(now/86400e3)),
						thatday = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0);
					var dday = Math.floor((thatday.getTime() - today.getTime())/86400e3);
					var $dday_elem = $("<div class='dday'/>");

					if(dday > 0){
						$dday_elem.text("D-"+dday);
						if(dday <= 7) $dday_elem.addClass('dday_near');
						if(dday == 0) $dday_elem.addClass('dday_today');
					}else{
						$dday_elem.text("D+"+(-dday));
						$dday_elem.addClass('dday_past');
					}

					$main_elem.append([$dday_elem, $("<dl>").append([
						$("<dt class='elem_title'/>").text(category_name),
						$("<dd class='elem_title'/>").text(article.title),
						$("<dt class='elem_time'/>").text('시간'),
						$("<dd class='elem_time'/>").append($("<time/>").attr('datetime', d.toISOString()).text(toDisplayDate(d)))
					])]);
					return $main_elem;
				});
			}
			$main_list.append(elems);
		});
	});
});
