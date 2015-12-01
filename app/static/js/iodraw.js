$(document).ready(function() {
  console.debug("loading socketio.js");
  
  var appEvents = new EventEmitter();

  var namespace = '/draw';
  var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

  socket.on('joinResponse', function(data) {
    $('#startPanel').hide();
    $('#drawPanel').show();
    console.log('data = ', data);
    $('#drawingRoom').text(data['room']);
    appEvents.emit('state#join');
  });

  $('#go').click(function() {
    console.log("form#go clicked");
    socket.emit('joinRequest', { room: $('#room').val() });
  });
  console.debug("END loading socketio.js");

  var BRUSH_WIDTH = 5;
  var BRUSH_HEIGHT = 5;
  var Drawing = function() {
    this.mouseDown = false;
    this.canvasEvents = {};
    this.lastX = this.lastY = undefined;
  };
  
  Drawing.prototype.init = function() {
    console.log('in createDrawing');
    var canvas = document.createElement('canvas');
    canvas.setAttribute('width', 800);
    canvas.setAttribute('height', 600);
    canvas.setAttribute('id', 'drawing');
    canvas.setAttribute("class", "drawing");

    var that = this;
    var context = canvas.getContext("2d");
    $(canvas).mousedown(function(e) {
      console.log("in mousedown");
      that.lastX = e.pageX - this.offsetLeft;
      that.lastY = e.pageY - this.offsetTop; 
      that.mouseDown = true;
    });

    $(canvas).mousemove(function(e) {
      console.log("in mousemove", that.mouseDown);
      if(that.mouseDown) {
	var x = e.pageX - this.offsetLeft;
	var y = e.pageY - this.offsetTop; 
	context.beginPath();
	context.moveTo(that.lastX || x, that.lastY || y);
	context.lineTo(x, y);
	context.stroke();
	that.lastX = x;
	that.lastY = y;
      }
    });
    
    $(canvas).mouseup(function(e) {
      that.mouseDown = false;
      that.lastX = that.lastY = undefined;
    });
    this.canvas = canvas;
  };

  Drawing.prototype.getCanvas = function() {
    return this.canvas;
  };

  appEvents.addListener('state#join', function() {
    var wrapper = document.getElementById('drawing-wrapper');
    var drawing = new Drawing();
    drawing.init();
    wrapper.appendChild(drawing.getCanvas());
  });
  
});
