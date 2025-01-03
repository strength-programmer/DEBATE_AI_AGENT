// Debate animation effects
function animateDebate() {
    const messages = document.querySelectorAll('.debate-message');
    messages.forEach((msg, index) => {
        msg.style.animationDelay = `${index * 0.2}s`;
    });
}

// Professor card hover effects
function initProfessorCards() {
    const cards = document.querySelectorAll('.professor-card');
    cards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        card.addEventListener('mouseout', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Enhanced topic suggestions with click-to-copy
function initTopicSuggestions() {
    console.log('Initializing topic suggestions...');
    const topicItems = document.querySelectorAll('.topic-item');
    console.log('Found topic items:', topicItems.length);
    
    topicItems.forEach(item => {
        // Remove any existing click listeners
        item.removeEventListener('click', handleTopicClick);
        // Add new click listener
        item.addEventListener('click', handleTopicClick);
    });
}

async function handleTopicClick(event) {
    const item = event.currentTarget;
    const topicText = item.getAttribute('data-topic');
    
    try {
        // Copy to clipboard
        await navigator.clipboard.writeText(topicText);
        
        // Update the input field
        const topicInput = document.querySelector('[data-testid="stTextArea"]');
        if (topicInput) {
            topicInput.value = topicText;
            topicInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        // Show success feedback
        const copyIcon = item.querySelector('.copy-icon');
        if (copyIcon) {
            const originalText = copyIcon.textContent;
            copyIcon.textContent = '✅';
            item.classList.add('topic-clicked');
            
            setTimeout(() => {
                copyIcon.textContent = '📋';
                item.classList.remove('topic-clicked');
            }, 1500);
        }
    } catch (err) {
        console.error('Copy failed:', err);
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = topicText;
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showCopyFeedback(item, true);
        } catch (e) {
            console.error('Fallback copy failed:', e);
            showCopyFeedback(item, false);
        }
        document.body.removeChild(textarea);
    }
}

function fallbackCopy(item, text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    
    try {
        textarea.select();
        document.execCommand('copy');
        showCopyFeedback(item, true);
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showCopyFeedback(item, false);
    } finally {
        document.body.removeChild(textarea);
    }
}

function showCopyFeedback(item, success) {
    const copyIcon = item.querySelector('.copy-icon');
    if (copyIcon) {
        const originalText = copyIcon.textContent;
        copyIcon.textContent = success ? '✅' : '❌';
        item.classList.add('topic-clicked');
        
        setTimeout(() => {
            copyIcon.textContent = originalText;
            item.classList.remove('topic-clicked');
        }, 1000);
    }
}

// Initialize when DOM is loaded
function initializeApp() {
    console.log('Initializing app...');
    try {
        animateDebate();
        initProfessorCards();
        initTopicSuggestions();
    } catch (error) {
        console.error('Error initializing app:', error);
        // Retry after a short delay if elements aren't ready
        setTimeout(initializeApp, 1000);
    }
}

// Multiple initialization points to ensure the script runs
document.addEventListener('DOMContentLoaded', initializeApp);
if (document.readyState === 'complete') {
    initializeApp();
}

// Reinitialize when Streamlit reruns
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length) {
            initializeApp();
        }
    });
});

observer.observe(document.body, { childList: true, subtree: true }); 