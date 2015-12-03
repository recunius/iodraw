$(document).ready(function() {
  console.debug("loading socketio.js");
  
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  var syncManager = new window.iodrawing.SyncManager(socket, window.iodrawing.appEvents);
  syncManager.init();

  var wrapper = document.getElementById('drawing-wrapper');
  var drawing = new window.iodrawing.Drawing();

  socket.on('initRoom', function(data) {
    $('#startPanel').hide();
    $('#drawPanel').show();
    console.debug('data = ', data);
    $('#drawingRoom').text(data['room']);

    drawing.init(wrapper);
    data.pic.forEach(function(line) {
      drawing.draw(line['from'], line['to']);
    });

  });
  
//  socket.on('leaveRoom', function() {
//    appEvents.emit('leaveRoom');
//  });


  var sendJoinRequest = function() {
    socket.emit('joinRequest', { room: $('#room').val() });
  };

  $('#go').click(function() {
    console.debug("#go clicked");
    sendJoinRequest();
  });

  $('#room').keypress(function(e) {
    if (e.which === 13) {
      console.debug("#room enter key pressed");
      sendJoinRequest();
      e.preventDefault();
    }
  });

  $('#leave').click(function() {
    var room = $('#room').val();
    console.debug("#leave clicked, leaving room", room);
    socket.emit('leaveRequest', { room: room }, function() {
      console.debug("leaveRequest response");
      window.iodrawing.appEvents.emit('leaveRoom');
    });
  });
  console.debug("END loading socketio.js");

  window.iodrawing.appEvents.on('leaveRoom', function() {
    console.debug("appEvents.leaveRoom");
    var roomEl = $('#room');
    roomEl.val('');
    $('#drawPanel').hide();
    $('#startPanel').show();
    roomEl.focus();
  });

  
});
