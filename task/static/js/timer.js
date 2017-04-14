function timer(time, id)
{
    // var time = 0;
    var timer_id;
    this.tracking = false;
    this.start = function()
    {
        interval =  1000;
        this.tracking = true;
            timer_id = setInterval(function()
            {
                time++;
                generate_time(time, id);
            }, interval);
            $('#button-timer-' + id + ' button i').html('stop');
            send_timer(time, id);

            window.onbeforeunload = function(event)
            {
               return confirm("Confirm refresh");
            };
    }

    this.stop = function() {
        clearInterval(timer_id);
        this.tracking = false;
        if(this.id !== 'undefined') {
            $('#button-timer-' + id + ' button i').html('play_arrow');
        }
        send_timer(time, id);

        window.onbeforeunload = function(event)
        {
        //    return confirm("Confirm refresh");
        };
    }
}

function generate_time(time, id)
{
    var second = time % 60;
    var minute = Math.floor(time / 60) % 60;
    var hour = Math.floor(time / 3600) % 60;

    second = (second < 10) ? '0'+second : second;
    minute = (minute < 10) ? '0'+minute : minute;
    hour = (hour < 10) ? '0'+hour : hour;
    $('#timer-' + id +' span.second' ).html(second);
    $('#timer-' + id +' span.minute').html(minute);
    $('#timer-' + id +' span.hour').html(hour);
}


var map = {};
function timing(id) {

    id = $(id).parent().attr("id");
    var pos = id.lastIndexOf("-");
    id = id.slice(pos+1);
    var time = get_timer(id);
    if(id in map) {
        if (map[id].tracking) {
            map[id].stop();
        } else {
            stop_all();
            map[id].start();
        }

    } else {
        stop_all();
        ob = new timer(time, id);
        ob.start();
        map[id] = ob;
    }
}

function stop_all() {
    for (var property in map) {
        map[property].stop();
    }
}

function send_timer(time, id) {
    $.ajax({
      type: 'GET',
      url: 'timer/',
      data: {
        'id': id,
        'timer': time,
      },
      dataType: 'json',
      success: function (data) {
      }
    });
}

function get_timer(id) {
    var timer = null;
    $.ajax({
      type: 'GET',
      url: 'timer_value/',
      async: false,
      data: {
        'id': id,
      },
      dataType: 'json',
      success: function (data) {
        timer = data["timer"];
      }
    });
    return timer;
}

$(document).ready(function() {
    $(".timer").each(function() {
        var id = $(this).attr("id");
        var pos = id.lastIndexOf("-");
        id = id.slice(pos+1);
        var time = get_timer(id);
        generate_time(time, id);
    });
})
