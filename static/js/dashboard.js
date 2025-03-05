document.addEventListener('DOMContentLoaded', function () {
  const logTaskButtons = document.querySelectorAll('.toast-task-button'); // Get all the buttons that open the toast
  const toastElement = document.getElementById('logTaskToast'); // Get the toast

  const toast = new bootstrap.Toast(toastElement); // Create a new toast instance
  // This is highlighting an issues but as long as we have put the bootstrap cdn in the scripts on base.html it works

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
});
