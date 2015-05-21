$(document).ready(function(){
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

	$('#content_left').children().children().eq(1).attr('id', 'current');

	$.ajax({
		'type' : 'GET',
		'url' : '/account/articles/',
		'dataType' : 'json',
		'success' : function(data) {
			var elems = [];
			var now = Date.now();
			elems = data.articles.map(function(article) {
				var i = 0, d = null;
				var $main_elem = $("<div class='elem'/>");
				var $poster_div = $("<div class='poster'></div>").addClass('vhmiddle').addClass('vhmiddle-portrait');
				var $anchor = $("<a/>").attr({'href':"/article/"+article.id});
				var $img = $("<img/>").attr({'src':article.poster.category_thumb, 'alt':article.title});
				$anchor.append($img);
				$poster_div.append($anchor);
				$main_elem.append($poster_div);

				for(i=0; i<article.timeslot.length; i++) {
					d = new Date(article.timeslot[i].start_time);
					if(d.getTime() >= now) break;
				}

				$main_elem.append([$("<table/>").append([
						$("<tr/>").append([$("<th class='elem_title'/>").text(article.category), $("<th class='elem_tiem'>시간</td>")]),
						$("<tr/>").append([$("<td class='elem_title'/>").append([$("<span/>").text(article.title)]), $("<td class='elem_time'>").append($("<time/>").attr('datetime', d.toISOString()).text(toDisplayDate(d)))])
						])]);
				$("#content_right").append($main_elem);
				$poster_div.vhmiddle();
			});
		},
		'error' : function() {
		},
	});
});
