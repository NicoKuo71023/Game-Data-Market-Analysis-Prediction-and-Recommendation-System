window.addEventListener('mousemove', function (evt) {
    let position_X = evt.pageX;
    let position_Y = evt.pageY;

    let crossElement = document.getElementById('cross');
    let squareElement = document.getElementById('square');
    let circleElement = document.getElementById('circle');
    let triangleElement = document.getElementById('triangle');

    crossElement.style.left = position_X + 50 + 'px';
    crossElement.style.top = position_Y + 50 + 'px';
    squareElement.style.left = position_X + 100 + 'px';
    squareElement.style.top = position_Y + 60 + 'px';
    circleElement.style.left = position_X + 150 + 'px';
    circleElement.style.top = position_Y + 50 + 'px';
    triangleElement.style.left = position_X + 200 + 'px';
    triangleElement.style.top = position_Y + 60 + 'px';
});