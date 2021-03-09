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