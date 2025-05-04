document.addEventListener('DOMContentLoaded', function() {
  // Set the launch date - 30 days from now
  const launchDate = new Date();
  launchDate.setDate(launchDate.getDate() + 30);
  
  // Update countdown every second
  const countdownElement = document.getElementById('countdown');
  
  function updateCountdown() {
      const now = new Date();
      const distance = launchDate - now;
      
      // Calculate days, hours, minutes, and seconds
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
      
      // Display the countdown
      countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
  }
  
  // Update immediately and then every second
  updateCountdown();
  setInterval(updateCountdown, 1000);
  
  // Simple animation effect for the logo
  const logo = document.querySelector('.logo');
  logo.addEventListener('mouseover', function() {
      this.style.transform = 'scale(1.1)';
  });
  
  logo.addEventListener('mouseout', function() {
      this.style.transform = 'scale(1)';
  });
});