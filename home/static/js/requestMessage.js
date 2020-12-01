let Notification = window.Notification || window.mozNotification || window.webkitNotification;
Notification.requestPermission((permission) => {
  console.log(permission);
});

if (typeof EventSource !== "undefined") {
  let source = new EventSource("stream/");
  source.onmessage = function (event) {
    if (event.data == "hi") {
      new Notification("메세지 알림", {
        body: "요청이 도착했습니다.",
      });
    } else {
      console.log(event.data);
    }
  };
} else {
  console.log("Sorry, your browser does not support server-sent events...");
}
