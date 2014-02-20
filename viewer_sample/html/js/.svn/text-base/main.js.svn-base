var HOST = '127.0.0.1',
    PORT = '8080';

$(function($) {
    var ws = new WebSocket('ws://' + HOST + ':' + PORT + '/');

    ws.onmessage = function(evt) {
        $.each($.parseJSON(evt.data), function(i, d) {
            $.each(d, function(j, elem) {
                $('#data').append(elem + '<br>');
            });
        });
    }

    ws.onopen = function(evt) {
        $('#status').html('<b>Connected</b>');
    }

    ws.onerror = function(evt) {
        $('#status').html('<b>Error</b>');
    }

    ws.onclose = function(evt) {
        console.log(evt);
        $('#status').html('<b>Closed</b>' + evt);
    }
});
