let angle = -90;
let direction = 1;
let animationId;
let isRunning = false;
let currentPlayer = 1;
let scores = { 1: 0, 2: 0 };

const needle = document.getElementById('needle');
const player1Btn = document.getElementById('player1Btn');
const player2Btn = document.getElementById('player2Btn');
const player1Score = document.getElementById('player1Score');
const player2Score = document.getElementById('player2Score');
const winnerText = document.getElementById('winner');

function startSwing() {
  isRunning = true;
  animateNeedle();
}

function animateNeedle() {
  angle += direction * 2;
  if (angle >= 90 || angle <= -90) {
    direction *= -1;
  }
  needle.style.transform = `rotate(${angle}deg)`;
  animationId = requestAnimationFrame(animateNeedle);
}

function stopSwing() {
  if (!isRunning) return;
  cancelAnimationFrame(animationId);
  isRunning = false;
  const score = calculateScore(angle);
  scores[currentPlayer] = score;
  updateScores();
  if (currentPlayer === 1) {
    currentPlayer = 2;
    startSwing();
  } else {
    determineWinner();
  }
}

function calculateScore(angle) {
  const diff = Math.abs(angle - 90);
  const score = Math.max(0, Math.round(100 - diff));
  return score;
}

function updateScores() {
  player1Score.textContent = scores[1];
  player2Score.textContent = scores[2];
}

function determineWinner() {
  if (scores[1] > scores[2]) {
    winnerText.textContent = 'Player 1 Wins!';
  } else if (scores[2] > scores[1]) {
    winnerText.textContent = 'Player 2 Wins!';
  } else {
    winnerText.textContent = "It's a Tie!";
  }
}

player1Btn.addEventListener('click', () => {
  if (currentPlayer === 1) {
    stopSwing();
  }
});

player2Btn.addEventListener('click', () => {
  if (currentPlayer === 2) {
    stopSwing();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'a' && currentPlayer === 1) {
    stopSwing();
  }
  if (e.key.toLowerCase() === 'l' && currentPlayer === 2) {
    stopSwing();
  }
});

// Start the game
startSwing();
