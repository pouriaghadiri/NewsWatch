window.onscroll = function(){
    myfixedheader();
}
var header = document.getElementById("my-header");
var distanceheader = header.offsetTop;
function myfixedheader() {
    if(window.pageYOffset > distanceheader){
        header.classList.add("header-fixed");
    }
    else{
        header.classList.remove("header-fixed");
    }
}

