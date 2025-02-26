const video = document.getElementById("videoPlayer");

video.addEventListener("pause", () => video.play());

let lastTime = 0;
setInterval(() => {
  if (Math.abs(video.currentTime - lastTime) > 0.5) {
    video.currentTime = lastTime;
  }
  lastTime = video.currentTime;
}, 100);
