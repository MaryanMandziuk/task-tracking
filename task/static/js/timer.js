function _timer(id)
{
    var time = 0;
    var timer_id;
    this.tracking = false;
    this.id = id;
    this.start = function()
    {
        interval =  1000;
        this.tracking = true;
            timer_id = setInterval(function()
            {
                time++;
                generateTime(id);
            }, interval);
            $('#button-timer-' + this.id + ' button i').html('stop');

    }

    this.stop = function() {
        clearInterval(timer_id);
        this.tracking = false;
        if(this.id !== 'undefined') {
            $('#button-timer-' + this.id + ' button i').html('play_arrow');
        }
    }


    function generateTime(id)
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
}


var map = {};
function timing(id) {
    id = $(id).parent().attr("id");
    var pos = id.lastIndexOf("-");
    id = id.slice(pos+1);
    if(id in map) {
        if (map[id].tracking) {
            map[id].stop();
        } else {
            stop_all();
            map[id].start();
        }

    } else {
        stop_all();
        ob = new _timer(id);
        ob.start();
        map[id] = ob;
    }
}

function stop_all() {
    for (var property in map) {
        map[property].stop();
    }
}
