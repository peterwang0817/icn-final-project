var ctx = document.getElementById("canvas").getContext('2d');
var img = new Image();
var started = false;
img.src = "{{ url_for('video_feed') }}";

// need only for static image
//img.onload = function(){   
//    ctx.drawImage(img, 0, 0);
//};

// need only for animated image
function refreshCanvas() {
    ctx.drawImage(img, 0, 0);
};
//window.setInterval("refreshCanvas()", 50);

function setupPlayer() {
    fetch('setup')
}

function playPlayer() {
    fetch('play')
    started = true;
}

function pausePlayer() {
    fetch('pause')
}

function teardownPlayer() {
    fetch('teardown')
}