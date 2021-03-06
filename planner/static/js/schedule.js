window.onload = function () {
    reset()
}

function sidebar_open(open) {
    var x = document.getElementById('sidebar')
    var y = document.getElementById('menu_button')
    if (open == true) {
        x.style.width = '15rem'
        y.style.width = '0'


    } else {
        y.style.width = '5rem'
        x.style.width = '0'

    }

}
window.addEventListener('click', function (e) {
    if (!e.target.matches('.sidebar')) {
        sidebar_open(false)
    }
})
function form_pop_up(open) {
    var y = document.getElementById('rotate')
    var x = document.getElementById('form_pop_up')
    if (open == false) {
        x.style.height = "3.5rem";
        x.style.width = "3.5rem";
        y.style.transition = '.5s all'
        y.style.transform = 'rotate(90deg)';
        y.setAttribute('onclick', 'javascript:form_pop_up(true);')

    } else {
        y.style.transition = '.5s all'
        y.style.transform = 'rotate(45deg)';
        y.setAttribute('onclick', 'javascript:form_pop_up(false);')
        x.style.width = "15rem";
        x.style.height = "35rem";
    }
}



function show() {
    var x = document.getElementById('calendar')
    var y = document.getElementById('show_cal')
    if (x.style.opacity == "0") {
        console.log('here')
        x.style.opacity = "100%";
        y.style.backgroundColor = 'pink';
        y.innerHTML = '<i class="fas fa-times"></i>';
    } else {
        y.style.backgroundColor = 'lightslategrey';
        x.style.opacity = "0";
        y.innerHTML = '<i class="fas fa-calendar-alt">';

    }

}
function create(start, end) {
    const y = document.getElementById('start')
    const z = document.getElementById('end')

    if (/Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor)) {
        if (start.split(' ')[1] < 10) {
            start = start.split(' ')
            start[1] = '0' + start[1]
            start = start[0] + ' ' + start[1]
        }
        y.setAttribute('value', start.replace(/\s/g, 'T') + ':00')
    } else {
        start = start + ':00';
        y.setAttribute('value', start)
    }
    if (/Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor)) {
        if (end.split(' ')[1] < 10) {
            end = end.split(' ')
            end[1] = '0' + end[1]
            end = end[0] + ' ' + end[1]
        }
        z.setAttribute('value', end.replace(/\s/g, 'T') + ':00')

    } else {
        end = end + ':00';
        z.setAttribute('value', end)
    }
}

const week = document.getElementById('week')
var now = new Date();
function take_out_single(x) {
    if (x < 10) {
        return '0' + x
    }
    else {
        return x
    }
}
var preset = [now.getFullYear() + '-' + take_out_single(Number(now.getMonth() + 1)) + '-' + take_out_single(now.getDate()), Number(now.getHours())]
function reset() {
    const reset = document.getElementsByClassName('hour')
    for (var i = 25; i < reset.length; i++) {
        if (i != '') {
            reset[i].style.backgroundColor = "";
            reset[i].style.border = "";

            if (new Date(reset[i].id.split(' ')[0]) < new Date(preset[0])) {
                document.getElementById(reset[i].id).style.backgroundColor = '#7788993d';
            }
            if (reset[i].id.split(' ')[0] == preset[0]) {
                if (Number(reset[i].id.split(' ')[1]) < Number(preset[1])) {
                    document.getElementById(reset[i].id).style.backgroundColor = '#7788993d'

                }
            }
        }
    }
}
week.addEventListener("mousedown", function (down) {
    let moved
    let downListener = () => {
        moved = false
    }
    week.addEventListener('mousedown', downListener)
    let moveListener = () => {
        moved = true
    }
    week.addEventListener('mousemove', moveListener)
    let upListener = () => {
        if (moved) {
            form_pop_up(true)

        } else {
            form_pop_up(false)
        }
    }
    reset()
    week.addEventListener('mouseup', upListener)
    if (down.target.parentNode.parentNode.parentNode.className == 'week' && !down.target.classList.contains('event')) {
        document.getElementById(down.target.id).className = 'hour event_title'
        document.getElementById(down.target.id).style.backgroundColor = 'pink';
        document.getElementById(down.target.id).style.borderRight = '.1rem solid #0b181e';
        document.getElementById(down.target.id).style.borderLeft = '.1rem solid #0b181e';
        document.getElementById(down.target.id).style.borderTop = '.1rem solid #0b181e';
        const reset = document.getElementsByClassName('hour')
        for (var i = 0; i < reset.length; i++) {
            reset[i].style.borderRadius = "";
        }
        week.onmouseover = function (move) {
            if (Number(down.target.id.split(' ')[1]) < Number(move.target.id.split(' ')[1]) && down.target.id.split(' ')[0] == move.target.id.split(' ')[0]) {
                document.getElementById(move.target.id).style.backgroundColor = 'pink';
                document.getElementById(move.target.id).style.borderLeft = '.1rem solid #0b181e';
                document.getElementById(move.target.id).style.borderRight = '.1rem solid #0b181e';
                document.getElementById(move.target.id).style.borderTopLeftRadius = ' 0';
            }
        };
        week.addEventListener("mouseup", function (up) {
            create(down.target.id, up.target.id)
            document.getElementById(up.target.id).style.borderRight = '.1rem solid #0b181e';
            document.getElementById(up.target.id).style.borderLeft = '.1rem solid #0b181e';
            document.getElementById(up.target.id).style.borderBottom = '.1rem solid #0b181e';
            const reset = document.getElementsByClassName('hour')
            for (var i = 0; i < reset.length; i++) {
                reset[i].style.borderRadius = "";
            }
            document.getElementById(down.target.id).style.borderRadius = '.4rem .4rem 0 0';
            document.getElementById(up.target.id).style.borderRadius = '0 0 .4rem .4rem ';
            week.onmouseover = null
        });
    }

});