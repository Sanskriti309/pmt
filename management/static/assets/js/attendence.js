  //For Current Time And Date.
  const formattedDateElement = document.getElementById("formattedDate");
  const currentDate = new Date();
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  const day = String(currentDate.getDate()).padStart(2, "0");
  const monthIndex = currentDate.getMonth();
  const month = months[monthIndex];
  const year = currentDate.getFullYear();
  const formattedDateString = `${day}-${month}-${year}`;
  formattedDateElement.textContent = `${formattedDateString}`;

  //auto upadte on every sec..
  const customDateTimeElement = document.getElementById("customDateTime");
  function updateDateTime() {
    const currentDate = new Date();

    const options = {
      weekday: "short",
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      hour12: true,
    };

    const formattedDateTimeString = new Intl.DateTimeFormat(
      "en-US",
      options
    ).format(currentDate);
    customDateTimeElement.textContent = `${formattedDateTimeString}`;
  }

  setInterval(updateDateTime, 1000);
  updateDateTime();


// Punch In Punch Out Button code
let startTime = parseInt(localStorage.getItem("startTime")) || 0;
let running = JSON.parse(localStorage.getItem("timerRunning")) || false;
let interval;
const timestamp = 0; //Set Start Timer Second According to need.

const punchinbtn = document.getElementById("punchinbtn");
const punchActivity = document.getElementById("punchActivity");
const punchInDataDiv = document.getElementById("punchInData");

function startTimer() {
  interval = setInterval(updateTimer, 1000);
  running = true;
  localStorage.setItem("timerRunning", JSON.stringify(running));
}

function stopTimer() {
  clearInterval(interval);
  localStorage.setItem("elapsedTime", Date.now() - startTime);
  localStorage.setItem("timerRunning", JSON.stringify(false));
  running = false;
}

function resumeTimer() {
  if (running) {
    startTime = Date.now() - parseInt(localStorage.getItem("elapsedTime")) || 0;
    startTimer();
    punchinbtn.textContent = "Punch Out";
    punchinbtn.classList.remove("btn-primary");
    punchinbtn.classList.add("btn-success");
    const punchInTime = `Punch IN Time: ${new Date(startTime).toLocaleTimeString()}`;
    addPunchTime(punchInTime);
    punchInDataDiv.textContent = punchInTime;
  }
  
}

punchinbtn.addEventListener("click", function () {
  if (!running) {
    startTime = Date.now() - timestamp; 
    startTimer();
    this.textContent = "Punch Out";
    this.classList.remove("btn-primary");
    this.classList.add("btn-success");
    const punchInTime = `Punch IN Time: ${new Date().toLocaleTimeString()}`;
    addPunchTime(punchInTime);
    punchInDataDiv.textContent = punchInTime;
  } else {
    stopTimer();
    this.textContent = "Punch In";
    this.classList.remove("btn-success");
    this.classList.add("btn-primary");
    addPunchTime(`Punch Out Time: ${new Date().toLocaleTimeString()}`);
  }
});

function addPunchTime(text) {
  const li = document.createElement("li");
  li.textContent = text;
  punchActivity.appendChild(li);
}

function updateTimer() {
  const elapsedTime = Date.now() - startTime;
  const formattedTime = new Date(elapsedTime).toISOString().substr(11, 8);
  document.getElementById("timer").textContent = formattedTime;
}

window.addEventListener("beforeunload", function () {
  if (running) {
    localStorage.setItem("elapsedTime", Date.now() - startTime);
  }
  localStorage.setItem("startTime", startTime);
  localStorage.setItem("timerRunning", JSON.stringify(running));
});

window.onload = function () {
  resumeTimer();
};