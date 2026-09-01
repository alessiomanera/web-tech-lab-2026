/**
 * concierge.js
 * ------------
 * AI Cultural Concierge chat controller.
 * Owns message rendering, HTML escaping, in-chat recommendation cards,
 * and live taste-profile updates. No-ops on pages without a chat form.
 */

/**
 * Escapes every HTML-significant character so untrusted text (user input,
 * model output, stored profile text) can never be parsed as markup.
 */
function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/** Applies **bold** and newline formatting to text that is ALREADY escaped. */
function formatEscapedText(escaped) {
    return escaped
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

/** Builds a bookable experience card from a parsed [RECOMMEND: ...] tag. */
function buildRecommendationCard(id, title, city, price) {
    return `
        <div class="chat-exp-card">
            <div class="flex-between-center mb-05">
                <span class="badge badge-yellow">${escapeHtml(city)}</span>
                <span class="font-bold-lg">&euro;${parseFloat(price).toFixed(2)}</span>
            </div>
            <div class="card-heading d-block mb-1 font-bold">${escapeHtml(title)}</div>
            <a href="/booking?exp_id=${encodeURIComponent(id)}" class="cta-button w-100">
                Book This Package &rarr;
            </a>
        </div>`;
}

/**
 * Renders a Concierge reply: recommendation tags become cards, everything
 * around them is escaped first, so no model output can inject markup.
 */
function renderConciergeReply(text) {
    const cardRegex = /\[RECOMMEND:\s*id=(\d+),\s*title="([^"]+)",\s*city="([^"]+)",\s*price=([\d.]+)\]/g;
    let html = '';
    let lastIndex = 0;
    let match;

    while ((match = cardRegex.exec(text)) !== null) {
        html += formatEscapedText(escapeHtml(text.slice(lastIndex, match.index)));
        html += buildRecommendationCard(match[1], match[2], match[3], match[4]);
        lastIndex = cardRegex.lastIndex;
    }
    html += formatEscapedText(escapeHtml(text.slice(lastIndex)));
    return html;
}

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    if (!chatForm) return;

    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const memoryBox = document.getElementById('memory-content-box');
    const resetBtn = document.getElementById('btn-reset-memory');

    chatMessages.scrollTop = chatMessages.scrollHeight;

    document.querySelectorAll('.quick-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            chatInput.value = chip.getAttribute('data-prompt');
            chatForm.requestSubmit();
        });
    });

    if (resetBtn) {
        resetBtn.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to reset your Cultural Taste Profile?')) return;
            try {
                const res = await ApiService.resetMemory();
                if (res.ok) {
                    memoryBox.innerHTML =
                        '<p class="italic-secondary-m-0">Taste profile reset. Chat to rebuild!</p>';
                }
            } catch (e) {
                alert('Error resetting profile.');
            }
        });
    }

    const appendMessage = (variant, headerText, bodyHtml) => {
        const wrapper = document.createElement('div');
        wrapper.className = `chat-msg chat-msg-${variant}`;
        const header = document.createElement('div');
        header.className = `msg-header-${variant}`;
        header.textContent = headerText;
        const body = document.createElement('div');
        body.innerHTML = bodyHtml;
        wrapper.append(header, body);
        chatMessages.appendChild(wrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return wrapper;
    };

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage('user', 'You', formatEscapedText(escapeHtml(message)));
        chatInput.value = '';
        chatInput.disabled = true;
        sendBtn.disabled = true;

        const typing = appendMessage(
            'model', 'Concierge AI',
            '<p class="italic-secondary-m-0">Consulting Italian cultural catalog...</p>'
        );

        try {
            const res = await ApiService.sendChatMessage(message);
            const data = await res.json();
            typing.remove();

            if (res.ok) {
                appendMessage('model', 'Concierge AI', renderConciergeReply(data.response));
                if (data.updated_profile) {
                    memoryBox.textContent = data.updated_profile;
                    memoryBox.classList.add('preserve-lines');
                }
            } else {
                appendMessage('model', 'Concierge AI',
                    `<p class="error-text">Error: ${escapeHtml(data.error || 'Unable to connect to Concierge.')}</p>`);
            }
        } catch (err) {
            typing.remove();
            appendMessage('model', 'Concierge AI',
                '<p class="error-text">Network error. Please try again.</p>');
        } finally {
            chatInput.disabled = false;
            sendBtn.disabled = false;
            chatInput.focus();
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    });
});
