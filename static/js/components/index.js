// Run the function when the DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM is ready');
  // for the score bar
  if (document.querySelector('.score_bar')) {
    animateScoreBar();
  }

  if (document.querySelector('.toast-task-button')) {
    toggleTaskToast();
  }

  // add more if there are other components that need to be initialised when the DOM is ready
});

// Score bar animation
const animateScoreBar = () => {
  const dailyRecommendedScore = 50;

  document.querySelectorAll('.score_bar__progress-bar').forEach(bar => {
    const score = parseFloat(bar.getAttribute('data-score-total')) || 0;
    const percent = (score / dailyRecommendedScore) * 100;  // 50 is the daily recommended score
    setTimeout(() => {
      bar.style.width = percent + '%';
    }, 500);  // slight delay so it is seen before the bar animates
  });
};


const toggleTaskToast = () => {
  const logTaskButtons = document.querySelectorAll('.toast-task-button'); // Get all the buttons that open the toast
  const toastElement = document.getElementById('logTaskToast'); // Get the toast

  const toast = new bootstrap.Toast(toastElement); // Create a new toast instance

  // Get the elements inside the toast
  const toastTaskName = document.getElementById('toast-task-name');
  const logTaskForm = document.getElementById('logTaskForm');

  // Add an event listener to each button
  logTaskButtons.forEach(button => {
    button.addEventListener('click', function () {
      // get the id from the data attributes
      const taskId = button.getAttribute('data-task-id');

      // Set the task name inside the toast
      toastTaskName.textContent = button.getAttribute('data-task-name');

      // set action to complete task with the id
      logTaskForm.action = `/ecopoints/task/complete/${taskId}/`;

      // Show the toast
      toast.show();
    });
  });
};
