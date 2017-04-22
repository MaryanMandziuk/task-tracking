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
                 var menu_button = create_button_menu(data[i]);
                 var menu_list = create_menu(data[i]);
                 $('#card-title-'+data[i].pk).append(menu_button);
                 $('#card-title-'+data[i].pk).append(menu_list);

                 componentHandler.upgradeElement(menu_button, "MaterialButton");
                 componentHandler.upgradeElement(menu_list, 'MaterialMenu');
             }
             offset += paginate_by
         }

         timers_refresh();

        },
    error: function(err) {
        console.log("ERRR");
    }
    });
}


var $window = $(window);
function pagination() {
    var path = window.location.pathname;
    var pos = path.indexOf("search");
    if (pos == -1 && $('#main').innerHeight()+$('#main').scrollTop() >= $('#main').prop("scrollHeight")) {
        pagination_ajax();
    }
}


function get_filter() {
    var path = window.location.pathname;
    var pos = path.lastIndexOf("/");
    var filter = path.slice(pos+1);
    return filter;
}


function generate_task(task) {
    var card_div = document.createElement('div');
    card_div.className = "mdl-cell mdl-card mdl-shadow--6dp";
    var card_title = document.createElement('div');
    card_title.className = "mdl-card__title mdl-color--indigo-300";
    card_title.id = "card-title-" + task.pk;
    var card_title_text = document.createElement('h2');
    card_title_text.className = "mdl-card__title-text";
    card_title_text.textContent = task.name;
    var spacer = document.createElement('div');
    spacer.className = "mdl-layout-spacer";
    var created = document.createElement('div');
    created.className = "mdl-color-text--blue-grey-50 created-finished";
    created.textContent = "created: " + task.created;
    var finished = document.createElement('div');
    finished.className = "mdl-color-text--blue-grey-50 created-finished";
    finished.textContent = "finished: " + task.finished;
    var div_dates = document.createElement('div');



    var card_description = document.createElement('div');
    card_description.className = "mdl-card__supporting-text";
    card_description.textContent = task.description;

    var card_action = document.createElement('div');
    card_action.className = "mdl-card__actions mdl-card--border";
    card_action.style = "margin-top: auto;";
    var card_action_container = document.createElement('div');
    card_action_container.className = "card-action-container";
    var inner_div = document.createElement('div');
    var checkbox_label = document.createElement('label');
    checkbox_label.className = "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect";
    checkbox_label.for = "checkbox-" + task.pk;
    var checkbox_input = document.createElement('input');
    checkbox_input.className = "mdl-checkbox__input";
    checkbox_input.type = "checkbox";
    checkbox_input.id = "checkbox-" + task.pk;
    checkbox_input.onclick = function() {is_done(this);};
    if(task.done == "True") {
        checkbox_input.checked = true;
    }
    var checkbox_span = document.createElement('span');
    checkbox_span.className = "mdl-checkbox__label";
    checkbox_span.textContent = "Done";

    var timer = document.createElement('div');
    timer.className = "timer";
    timer.id = "timer-" + task.pk;
    timer.innerHTML = timer.innerHTML + "<span class=\"hour\">00</span>:<span class=\"minute\">00</span>:<span class=\"second\">00</span>";

    var timer_button_div = document.createElement('div');
    timer_button_div.id = "button-timer-" + task.pk;

    var timer_button = document.createElement('button');
    timer_button.className = "mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--mini-fab mdl-button--colored";
    timer_button.onclick = function() {timing(this);};
    if (task.done=="True") {
        timer_button.disabled = true;
    }
    var timer_icon = document.createElement('i');
    timer_icon.className = "material-icons";
    timer_icon.textContent = "play_arrow";





    card_title.appendChild(card_title_text);
    card_title.appendChild(spacer);
    div_dates.appendChild(created);

    if(task.finished != ""){
        div_dates.appendChild(finished);
    }
    card_title.appendChild(div_dates);





    // card_title.appendChild(menu_button);
    // menu_link_edit.appendChild(menu_edit);
    // menu_link_remove.appendChild(menu_remove);


    // card_title.appendChild(menu_list);





    card_div.appendChild(card_title);
    card_div.appendChild(card_description);

    card_action.appendChild(card_action_container);
    card_action_container.appendChild(inner_div);
    checkbox_label.appendChild(checkbox_input);
    checkbox_label.appendChild(checkbox_span);
    componentHandler.upgradeElement(checkbox_label);
    inner_div.appendChild(checkbox_label);

    card_action_container.appendChild(timer);
    timer_button.appendChild(timer_icon);
    componentHandler.upgradeElement(timer_button);

    timer_button_div.append(timer_button);
    card_action_container.appendChild(timer_button_div);
    card_div.appendChild(card_action);

    componentHandler.upgradeElement(card_div);

    return card_div;
}
function create_button_menu(task) {
    var menu_button = document.createElement('button');
    menu_button.className = "mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon";
    menu_button.id = "menu_list-" + task.pk;
    var icon_for_menu_button = document.createElement("i");
    icon_for_menu_button.className = "material-icons";
    icon_for_menu_button.textContent = "more_vert";

    menu_button.appendChild(icon_for_menu_button);


    return menu_button;
}

function create_menu(task) {
    var menu_list = document.createElement("ul");
    menu_list.className = "mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right";
    menu_list.setAttribute("for", "menu_list-" + task.pk);
    menu_list.id = "menu_list-" + task.pk;
    var menu_link_edit = document.createElement('a');
    menu_link_edit.className = "link-button";
    menu_link_edit.href = "edit/"+task.pk;
    var menu_edit = document.createElement('li');
    menu_edit.className = "mdl-menu__item";
    menu_edit.id = "edit" + task.pk;
    menu_edit.textContent = "Edit";
    var menu_link_remove = document.createElement('a');
    menu_link_remove.className = "link-button";
    menu_link_remove.href = "remove/" + task.pk;
    var menu_remove = document.createElement('li');
    menu_remove.className = "mdl-menu__item";
    menu_remove.textContent = "Remove";

    menu_link_edit.appendChild(menu_edit);
    menu_link_remove.appendChild(menu_remove)
    menu_list.appendChild(menu_link_edit);
    menu_list.appendChild(menu_link_remove);

    return menu_list;
}

$(document).ready(function() {
        // console.log($('.mdl-grid').height());
        $('.mdl-grid').height($('.mdl-grid').height() * 1.25);
        // console.log($('.mdl-grid').height());
})
