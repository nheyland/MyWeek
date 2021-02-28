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
week.addEventListener("mousedown", function (down) {
    const reset = document.getElementsByClassName('hour')
    for (var i = 0; i < reset.length; i++) {
        reset[i].style.backgroundColor = "";
    }
    if (down.target.parentNode.parentNode.parentNode.className == 'week' && !down.target.classList.contains('event')) {
        document.getElementById(down.target.id).style.backgroundColor = 'pink';
        week.onmouseover = function (move) {
            if (Number(down.target.id.split(' ')[1]) < Number(move.target.id.split(' ')[1]) && down.target.id.split(' ')[0] == move.target.id.split(' ')[0]) {
                document.getElementById(move.target.id).style.backgroundColor = 'pink';
            }
        };
        week.addEventListener("mouseup", function (up) {
            create(down.target.id, up.target.id)
            document.getElementById(down.target.id).innerText = '';
            week.onmouseover = null

        });

    }

});

console.log('here!')