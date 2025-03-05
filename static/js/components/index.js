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


// Run the function when the DOM is ready
document.addEventListener('DOMContentLoaded', function () {

  // for the score bar
  if (document.querySelector('.score_bar')) {
    animateScoreBar();
  }

  // add more if there are other components that need to be initialised when the DOM is ready
});
