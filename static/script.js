// Add a scrolling text effect

var text = "FUTURISTIC WEBSITE";
var el = document.getElementById("scrolling-text");


setInterval(function() {
    el.innerHTML = text;
    text = text.substring(1) + text.substring(0,1);
}, 100);


// Add a particle effect
particlesJS.load('particles-js', 'path/to/particles.json', function() {
    console.log('callback - particles.js config loaded');
});
