// DOM Elements
const loginPage = document.getElementById("login-page");
const dashboardPage = document.getElementById("dashboard-page");
const loginForm = document.getElementById("login-form");
const profileBtn = document.getElementById("profile-btn");
const profileMenu = document.getElementById("profile-menu");
const logoutBtn = document.getElementById("logout-btn");
const timerBtn = document.getElementById("timer-btn");
const timerDisplay = document.querySelector(".timer-display");
const timerDuration = document.querySelector(".timer-duration");

// Login handling
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  loginPage.classList.add("hidden");
  dashboardPage.classList.remove("hidden");
});

// Profile dropdown
profileBtn.addEventListener("click", () => {
  profileMenu.classList.toggle("hidden");
});

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
    profileMenu.classList.add("hidden");
  }
});

// Logout handling
logoutBtn.addEventListener("click", () => {
  dashboardPage.classList.add("hidden");
  loginPage.classList.remove("hidden");
});

// Timer functionality
let timerInterval;
let isTimerRunning = false;

function updateTimer(duration) {
  let timeLeft = duration * 60;
  timerDisplay.textContent = formatTime(timeLeft);

  if (timerInterval) clearInterval(timerInterval);

  timerInterval = setInterval(() => {
    timeLeft--;
    timerDisplay.textContent = formatTime(timeLeft);

    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      isTimerRunning = false;
      timerBtn.innerHTML = '<i class="ri-play-line"></i> Start';
    }
  }, 1000);
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

timerBtn.addEventListener("click", () => {
  isTimerRunning = !isTimerRunning;

  if (isTimerRunning) {
    timerBtn.innerHTML = '<i class="ri-pause-line"></i> Pause';
    updateTimer(parseInt(timerDuration.value));
  } else {
    timerBtn.innerHTML = '<i class="ri-play-line"></i> Start';
    clearInterval(timerInterval);
  }
});

timerDuration.addEventListener("change", () => {
  timerDisplay.textContent = `${timerDuration.value}:00`;
  if (isTimerRunning) {
    updateTimer(parseInt(timerDuration.value));
  }
});

// Initialize progress circles
document.querySelectorAll(".progress-circle").forEach((circle) => {
  const value = circle.dataset.value;
  circle.style.setProperty("--progress", `${value}%`);
});

// Sample exercise data
const exercises = [
  { name: "Push-ups", duration: "10 mins", calories: 100 },
  { name: "Squats", duration: "15 mins", calories: 150 },
  { name: "Planks", duration: "5 mins", calories: 50 },
];

// Populate exercise list
const exerciseList = document.querySelector(".exercise-list");
exercises.forEach((exercise) => {
  const exerciseItem = document.createElement("div");
  exerciseItem.className = "exercise-item";
  exerciseItem.innerHTML = `
        <div class="exercise-info">
            <p class="exercise-name">${exercise.name}</p>
            <div class="exercise-stats">
                <span><i class="ri-time-line"></i> ${exercise.duration}</span>
                <span><i class="ri-fire-line"></i> ${exercise.calories} cal</span>
            </div>
        </div>
        <button class="btn btn-outline">Start</button>
    `;
  exerciseList.appendChild(exerciseItem);
});

// Initialize weekly chart
const chartData = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  datasets: [
    {
      label: "Physical Activities",
      data: [65, 70, 60, 75, 80, 85, 70],
      backgroundColor: "#8884d8",
    },
    {
      label: "Sleep Patterns",
      data: [80, 75, 85, 70, 75, 90, 85],
      backgroundColor: "#82ca9d",
    },
    {
      label: "Study Sessions",
      data: [70, 65, 75, 80, 85, 60, 55],
      backgroundColor: "#ffc658",
    },
    {
      label: "Mood Trends",
      data: [85, 80, 75, 90, 85, 95, 90],
      backgroundColor: "#ff7c7c",
    },
  ],
};

const ctx = document.createElement("canvas");
document.querySelector(".chart-container").appendChild(ctx);

new Chart(ctx, {
  type: "bar",
  data: chartData,
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  },
});
