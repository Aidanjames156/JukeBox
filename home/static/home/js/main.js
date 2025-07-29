// Custom JavaScript for JukeBox

document.addEventListener('DOMContentLoaded', function() {
    // Add click effects to music control buttons
    const musicButtons = document.querySelectorAll('.music-control-btn');
    
    musicButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add a temporary class for visual feedback
            this.classList.add('clicked');
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 200);
            
            // You can add actual music functionality here later
            console.log('Button clicked:', this.textContent.trim());
        });
    });
    
    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
        });
    });
});

// Add CSS for clicked effect
const style = document.createElement('style');
style.textContent = `
    .music-control-btn.clicked {
        transform: scale(0.95);
        transition: transform 0.1s ease;
    }
`;
document.head.appendChild(style);
