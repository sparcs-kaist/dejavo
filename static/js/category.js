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

	$('#category_list button').click(function(){
		var category_name = this.innerText;
		$.get("/category/"+this.value+"/?accept=application/json", function(data){
			$main_list.empty();
			var elems = [],
				now = Date.now();
			if(data && data.articles){
				elems = data.articles.map(function(article){
					var i, d = null;
					$main_elem = $("<div class='elem'/>");
					$main_elem.append($("<img/>").attr('src', article.poster));
					
					for(i=0; i<article.timeslot.length; i++){
						d = new Date(article.timeslot[i].start_time);
						if(d.getTime() >= now) break;
					}

					$main_elem.append($("<dl>").append([
						$("<dt/>").text(category_name),
						$("<dd/>").text(article.title),
						$("<dt/>").text('시간'),
						$("<dd/>").text(toDisplayDate(d))
					]));
					return $main_elem;
				});
			}
			$main_list.append(elems);
		});
	});
});
