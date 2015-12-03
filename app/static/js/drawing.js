(function() {

  window.iodrawing = window.iodrawing || { };

  var BRUSH_WIDTH = 5;
  var BRUSH_HEIGHT = 5;
  var WIDTH = 800;
  var HEIGHT = 600;
  var Drawing = window.iodrawing.Drawing = function() {
    this.context = undefined;
    this.mouseDown = false;
    this.canvasEvents = {};
    this.lastX = this.lastY = undefined;
  };

  Drawing.prototype.build = function() {
    console.log('in buildDrawing');
    var canvas = document.createElement('canvas');
    canvas.setAttribute('width', WIDTH);
    canvas.setAttribute('height', HEIGHT);
    canvas.setAttribute('id', 'drawing');
    canvas.setAttribute("class", "drawing");

    this.context = canvas.getContext("2d");
    var that = this;
    $(canvas).mousedown(function(e) {
      that.lastX = e.pageX - this.offsetLeft;
      that.lastY = e.pageY - this.offsetTop; 
      that.mouseDown = true;
    });

    $(canvas).mousemove(function(e) {
      if(that.mouseDown) {
	var x = e.pageX - this.offsetLeft;
	var y = e.pageY - this.offsetTop;
	var from = { x: that.lastX || x, y: that.lastY || y};
	var to = { x: x, y: y};
	that.draw(from, to);
	window.iodrawing.appEvents.emit('uiDraw', { from: from, to: to });
	that.lastX = x;
	that.lastY = y;
      }
    });

    window.iodrawing.appEvents.on('draw', function(data) {
      that.draw(data.from, data.to);
    });
    
    $(canvas).mouseup(function(e) {
      that.mouseDown = false;
      that.lastX = that.lastY = undefined;
    });

    return canvas;
  };

  Drawing.prototype.init = function(wrapper) {
    if (this.context) {
      this.context.clearRect(0, 0, WIDTH, HEIGHT);
    } else {
      var canvas = this.build(wrapper);
      wrapper.appendChild(canvas);
    }

  };

  Drawing.prototype.draw = function(from, to) {
    this.context.beginPath();
    this.context.moveTo(from.x, from.y);
    this.context.lineTo(to.x, to.y);
    this.context.stroke();
  };

  Drawing.prototype.getCanvas = function() {
    return this.canvas;
  };

})();
