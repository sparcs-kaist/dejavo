$(document).ready(function(){
	var $main_list = $('#main_list');
	
	var padZero = function padZero(s, l){
		for(s+=''; s.length<l; s='0'+s); return s;
	};

	var toDisplayDate = function toDisplayDate(d){
		if(!d) return '?/??';
		var s = (d.getMonth()+1)+'/'+padZero(d.getDate());
		var h = d.getHours()%12; if(h==0) h=12;
		s += ' '+h+(d.getHours()>=12?'pm':'am');
		return s;
	};

	var $current_button = null;

	var getArticles = function getArticles(v){
		$.ajax({
			'type' : 'GET',
			'url' : '/category/'+v+'/',
			'dataType' : 'json',
			'success' : function(data){
				$main_list.empty();
				var elems = [],
					today = new Date();
				today.setHours(0);
				today.setMinutes(0);
				today.setSeconds(0);
				today.setMilliseconds(0);

				if(data && data.articles){
					elems = data.articles.map(function(article){
						var i, d=null,
							$main_elem = $("<div class='elem'/>"),
							$poster_div = $("<div class='poster'></div>").addClass('vhmiddle'),
							$anchor = $("<a/>").attr({'href':"/article/"+article.id}),
							$img = $("<img/>").attr({'src':article.poster.category_thumb, 'alt':article.title}).
								load(function(){;
								var scaled_width = this.width * 317/this.height;
								var cell_size = Math.round(scaled_width/223);
								if(cell_size >= 2) {
									$main_elem.addClass('elem_wide');
								}
								$anchor.append($img);
								$poster_div.append($anchor);
								$poster_div.vhmiddle();
							});

						$main_elem.append($poster_div);

						d = new Date(article.date);
						var thatday = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0);

						var dday = Math.floor((thatday.getTime() - today.getTime())/86400e3);
						var $dday_elem = $("<div class='dday'/>");

						if(dday == 0) {
							$dday_elem.addClass('dday_today');
							$dday_elem.text("NOW");
						}
						else if(dday > 0){
							$dday_elem.text("D-"+dday);
							if(dday <= 7) $dday_elem.addClass('dday_near');
						}else{
							$dday_elem.text("D+"+(-dday));
							$dday_elem.addClass('dday_past');
						}

						$main_elem.append([$dday_elem, $("<table/>").append([
							$("<tr/>").append([$("<th class='elem_title'/>").text(article.category), $("<th class='elem_time'>시간</td>")]),
							$("<tr/>").append([$("<td class='elem_title'/>").append([$("<span/>").text(article.title)]), $("<td class='elem_time'>").append($("<time/>").attr('datetime', d.toISOString()).text(toDisplayDate(d)))])
						])]);
						return $main_elem;
					});
				}
				$main_list.append(elems);
			},
			'error' :  function() {
			},
		});
	};

	$('#category_list button').click(function(){
		if($current_button) $current_button.removeClass('toggled');
		($current_button = $(this)).addClass('toggled');
		getArticles(this.value);
	});

	$('#category_list button[value="all"]').click();
});
