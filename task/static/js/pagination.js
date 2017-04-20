var offset = 9;
var paginate_by = 9
function pagination_ajax() {
    $.ajax({
    type: 'GET',
    url: 'pagination_ajax/',
    data: {
    'offset': offset,
    'filter': get_filter(),
    },
    // async: false,
    success: function (data) {
        if (data.length > 0) {
             for (var i = 0, total = data.length; i < total; i++) {
                 $('.mdl-grid').append(generate_task(data[i]));
             }
             offset += paginate_by
         }
        },
    error: function(err) {
        console.log("ERRR");
    }
    });
}


var $window = $(window);
function pagination() {
    var distance = $window.scrollTop() + $window.height();
    // console.log($('#main').innerHeight(), $('#main').scrollTop(), $('#main').prop("scrollHeight"));
    if ($('#main').innerHeight()+$('#main').scrollTop() >= $('#main').prop("scrollHeight")) {
        pagination_ajax();
        // console.log("get");
    }
}


function get_filter() {
    var path = window.location.pathname;
    var pos = path.lastIndexOf("/");
    var filter = path.slice(pos+1);
    return filter;
}

function generate_task(task) {
    var done = "";
    var finished = "";
    if(task.finished != "") {
        finished = "<div class=\"mdl-color-text--blue-grey-50 created-finished\">finished: "+task.finished+"</div>"
    }
    if (task.done=="True") {
        done="<input onclick=\"is_done(this);\" type=\"checkbox\" id=\"checkbox-"+task.pk+"\" class=\"mdl-checkbox__input\" checked>\ ";
    } else {
        done="<input onclick=\"is_done(this);\" type=\"checkbox\" id=\"checkbox-"+task.pk+"\" class=\"mdl-checkbox__input\" >\ ";
    }
    var button = "";
    if (task.done=="True") {
        button = "<button  onClick=\"timing(this);\" class=\"mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--mini-fab mdl-button--colored\" disabled>\
          <i class=\"material-icons\">play_arrow</i>\
        </button>";
    } else {
        button = "<button  onClick=\"timing(this);\" class=\"mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--mini-fab mdl-button--colored\">\
          <i class=\"material-icons\">play_arrow</i>\
        </button>";
    }
    var data ="\
    <div class=\"mdl-cell mdl-card mdl-shadow--6dp\">\
        <div  class=\"mdl-card__title mdl-color--indigo-300\">\
            <h2 class=\"mdl-card__title-text\">"+task.name+"</h2>\
            <div class=\"mdl-layout-spacer\"></div>\
            <div>\
                <div class=\"mdl-color-text--blue-grey-50 created-finished\">created: "+task.created+"</div>\
                "+finished+"\
            </div>\
            <button class=\"mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon\" id="+task.pk+">\
              <i class=\"material-icons\">more_vert</i>\
            </button>\
            <ul class=\"mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right\" for="+task.pk+">\
              <a href=\"\" class=\"link-button\">\
                  <li class=\"mdl-menu__item\" id=\"edit"+task.pk+"\">Edit</li>\
              </a>\
              <a href=\"\" class=\"link-button\">\
                  <li class=\"mdl-menu__item\">Remove</li>\
              </a>\
            </ul>\
        </div>\
        <div class=\"mdl-card__supporting-text\">\
             "+task.description+" \
        </div>\
        <div style=\"margin-top: auto;\" class=\"mdl-card__actions mdl-card--border\">\
            <div class=\"card-action-container\">\
                <div>\
                    <label class=\"mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect \" for=\"checkbox-"+task.pk+"\">\
                        "+done+"\
                      <span class=\"mdl-checkbox__label\">Done</span>\
                    </label>\
                </div>\
                <div class=\"timer\" id=\"timer-"+task.pk+"\"><span class=\"hour\">00</span>:<span class=\"minute\">00</span>:<span class=\"second\">00</span></div>\
                <div id=\"button-timer-"+task.pk+"\">\
                    "+button+"\
                </div>\
            </div>\
        </div>\
    </div>\
    "

    return data;
}
$(document).ready(function() {
        // console.log($('.mdl-grid').height());
        $('.mdl-grid').height($('.mdl-grid').height() * 1.25);
        // console.log($('.mdl-grid').height());
})
