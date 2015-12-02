var SyncManager = function(socket, appEvents) {
  this.socket = socket;
  this.events = appEvents;
};

SyncManager.prototype.init = function() {
  var that = this;
  this.socket.on('receiveDraw', function(data) {
    that.events.emit('draw', data);
  });
  this.events.on('uiDraw', function(data) {
    that.sendDraw(data);
  });
};

SyncManager.prototype.sendDraw = function(data) {
  // TODO: push a timer until X milliseconds of user inactivity to prevent pinning server
  // TODO: reduce payload size
  this.socket.emit('draw', data);
};
