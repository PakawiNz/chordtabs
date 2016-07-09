$(function(){
    //Handles menu drop down

    var csrf = $('meta[name="csrf"]').attr('content')
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        }
    });

    window.doajax = function(data){
        data.dataType = 'json';
        data.type = "POST";
        // if (!data.sendform) {
        //     data.data = JSON.stringify(data.data);
        //     data.contentType = "application/json; charset=utf-8";
        // }
        $.ajax(data);
    }
});

$(document).ready(function() {

	var debug_on_server = function(object){
    	var strobj = []
    	for (key in object){
    		strobj.push('' + key + ' : '+object[key]);
    	}
		doajax({
			url: '/print/',
			data: {logger:strobj},
			success:function(){},
		});
		return;
	}

	var get_playlist = function(){
		var song = $('#playlist-song').val();
		doajax({
		    url: '/get-playlist/',
		    data: {'song':song},
		    success: function(result) {
				var list = $('#playlist .playlist-list')
				list.find('.playlist-link-group').remove();
				result.playlists.forEach(function(item){
					var button = list.append(playlist_template(item.id,item.name,item.isin));
					list.find('.playlist-link-group').fadeIn();
				})
				$('.playlist-link').click(function (event){
					add_to_playlist(event.target);
				});
		    },
		});
	}
	var add_to_playlist = function(target){
		var song = $('#playlist-song').val();
		var playlist = target.value;
		doajax({
		    url: '/add-to-playlist/',
		    data: {'song':song,'playlist':playlist},
		    success: function(result) {
		    	get_playlist();
		    },
		});
	}

	var playlist_template = function(id,name,isin){
		var color;
		if (isin) color = 'warning';
		else color = 'default';

		var string = '';
		string += '<div class="playlist-link-group" style="display:none;">';
		string += '<div class="btn-group" style="width:100%;">';
		string += '<button class="btn btn-' + color + ' playlist-link" ';
		string += 'name="playlist" ';
		string += 'style="width:100%;" ';
		string += 'value="' + id + '">' + name + '</button>';
		// string += '<button class="btn btn-danger" style="width:40px;">';
		// string += '<span class="glyphicon glyphicon-trash"></span>'
		// string += '</button>';
		string += '</div>';
		string += '</div>';

		return string
	}
    $('[data-fav]').on('click', function (event) {
		var button = $(event.delegateTarget) // Button that triggered the modal

		var song = button.data('song');
		var fav = button.data('fav');
		var type = fav ? 'unset_favorite':'set_favorite' ;
		
		doajax({
		    url: '/' + type + '/' + song + '/',
		    success: function(result) {
	    		var star = button.find('.glyphicon')
		    	if (fav) {
		    		button.data('fav',false);
		    		button.switchClass('btn-warning','btn-default');
		    		star.switchClass('glyphicon-star','glyphicon-star-empty');
		    	} else {
		    		button.data('fav',true);
		    		button.switchClass('btn-default','btn-warning');
		    		star.switchClass('glyphicon-star-empty','glyphicon-star');
		    	}
		    },
		});
    });
    $('[data-request]').on('click', function (event) {
		var button = $(event.delegateTarget) // Button that triggered the modal

		var song = button.data('song');
		
		doajax({
		    url: '/request_song/' + song + '/',
		    success: function(result) {
	    		var star = button.find('.glyphicon')
	    		button.switchClass('btn-default','btn-danger');
	    		setTimeout(function(){
		    		button.switchClass('btn-danger','btn-default');
	    		},500);
		    },
		});
    });
    $('#playlist').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget) // Button that triggered the modal
		var song = button.data('song') 
		$(this).find('.modal-body #playlist-song').val(song);
		get_playlist();
	})
    $('#create-playlist-open').on('click', function (event) {
		$('#create-playlist-panel').slideToggle();
	})
    $('#create-playlist-done').on('click', function (event) {
		$('#create-playlist-panel').slideUp();
		doajax({
		    url: '/new-playlist/',
		    sendform: true,
		    data: $('#create-playlist-form').serialize(),
		    success: function(result) {
				$('#playlist .playlist-link').fadeOut(null,get_playlist);
		    },
		});
	})
});