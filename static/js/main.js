window.onload = function () {
    setTimeout(function () {
        getCookyDiv = document.getElementById('clickforsound')
        getCookyDiv.style.display = 'flex';
    }, 2000);
}
let PlayWithSound = () => {
    const video = document.getElementById('myVideo');
    const playButton = document.getElementById('playButton');
    video.muted = false;
    video.currentTime = 0;
    video.play();
    getCookyDiv = document.getElementById('clickforsound')
    getCookyDiv.style.display = 'none';
    setTimeout(function () {
        video.muted = true;
    }, 7000);
}
// Function to get a random integer between min and max (inclusive)
function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Get a random number between 3 and 10 (inclusive)
let AgentsCount = getRandomIntInclusive(3, 10);

document.getElementById('navbarAgent').textContent  = `${AgentsCount} agents Available`;

// FIle Download Option
function downloadFile(url, filename) {
  // Create a temporary anchor element
  const link = document.createElement('a');
  link.style.display = 'none';
  link.href = url;
  
  // The 'download' attribute specifies the filename
  link.download = filename;

  // Append the link to the document body
  document.body.appendChild(link);

  // Programmatically click the link to trigger the download
  link.click();

  // Clean up by removing the temporary link
  document.body.removeChild(link);
}

// =======================Bot====================\\

(function() {
      const elToggles = document.querySelectorAll('.cbToggle'); // CHANGED: was elToggle
      const elPanel  = document.getElementById('cbPanel');
      const elBody   = document.getElementById('cbBody');
      const elInput  = document.getElementById('cbInput');
      const elSend   = document.getElementById('cbSend');
      const elClose  = document.getElementById('cbClose');

      function setOpen(open) {
        elPanel.classList.toggle('cb-open', open);
        // CHANGED: apply aria-expanded to each toggle button
        elToggles.forEach(btn => btn.setAttribute('aria-expanded', String(open)));
        elPanel.setAttribute('aria-modal', String(open));
        if (open) {
          setTimeout(() => elInput.focus(), 100);
        } else {
          // optional: return focus to first toggle if it exists
          if (elToggles[0]) elToggles[0].focus();
        }
      }

      function togglePanel() { setOpen(!elPanel.classList.contains('cb-open')); }

      // CHANGED: add listener to each toggle button
      elToggles.forEach(btn => btn.addEventListener('click', togglePanel));
      elClose.addEventListener('click', () => setOpen(false));

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && elPanel.classList.contains('cb-open')) setOpen(false);
      });

      function appendMessage(text, who = 'user') {
        const msg = document.createElement('div');
        msg.className = `cb-msg ${who}`;
        msg.textContent = text;
        elBody.appendChild(msg);
        elBody.scrollTop = elBody.scrollHeight;
      }

      function getCSRF(){
        const name = 'csrftoken=';
        const parts = document.cookie.split(';');
        for (let c of parts){
          c = c.trim();
          if (c.startsWith(name)) return c.substring(name.length);
        }
        return '';
      }

      async function sendToBackend(text){
        const body = new URLSearchParams();
        body.append('q', text);
        const r = await fetch(chatBotApiUrl, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCSRF(), 'Content-Type': 'application/x-www-form-urlencoded' },
          body
        });
        if (!r.ok) throw new Error('Network error');
        return r.json();
      }

      async function handleSend(){
        const text = elInput.value.trim();
        if (!text) return;
        appendMessage(text, 'user');
        elInput.value = '';

        appendMessage('Thinking…', 'bot');
        const thinkingNode = elBody.lastChild;

        try {
          const j = await sendToBackend(text);
          thinkingNode.remove();
          appendMessage(j.answer || 'No response.', 'bot');
        } catch (err) {
          thinkingNode.remove();
          appendMessage('Sorry, something went wrong.', 'bot');
        }
      }

      elSend.addEventListener('click', handleSend);
      elInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSend();
        }
      });

      if (location.hash === '#chat') setOpen(true);
    })();

// const chatBotTextYou = document.getElementById('chatBotTextYou');
// const divContainer = document.getElementById('divContainer');
// const sendButton = document.getElementById('sendButtonOfBot')
// sendButton.addEventListener('click', () => {
//     if (chatBotTextYou.value!="") {
//         // Send Your Chat
//         const newDiv = document.createElement('div');
//         // Add Tailwind CSS classes for styling
//         newDiv.classList.add(
//             'chatbotTextBody_You'
//         );
//         // Set the content of the new div
//         newDiv.textContent = chatBotTextYou.value;
//         let check = chatBotTextYou.value
//         chatBotTextYou.value = "";
//         // Append the new div to the container
//         divContainer.appendChild(newDiv);
//         sentence = "Hello World".trim();
//         const isFound = sentence.includes(check.trim());

//         // API==========================================
        
//         const apiUrl = 'http://127.0.0.1:8000/bot/api';

//         // Function to fetch data from the API
//         const fetchData = async () => {
//             // Show a loading message

//             try {
//                 // Use the fetch API to make the GET request
//                 const response = await fetch(apiUrl, {
//                     method: 'POST', // Specify the method as POST
//                     headers: {
//                         // Tell the server we are sending JSON data
//                         'Content-Type': 'application/json; charset=UTF-8',
//                     },
//                     body: JSON.stringify({ 'question': check }), // Convert the JavaScript object to a JSON string
//                 });

//                 // Check if the response is successful (status code 200-299)
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! Status: ${response.status}`);
//                 }

//                 // Parse the JSON data from the response
//                 const data = await response.json();

//                 // The API returns an array of results, we take the first one
//                 const user = data;

//                 const newDivbot = document.createElement('div');
//                 // Add Tailwind CSS classes for styling
//                 newDivbot.classList.add(
//                     'chatbotTextBody_Bot'
//                 );
//                 // Set the content of the new div
//                 newDivbot.textContent = data.result;
//                 chatBotTextYou.value = "";
//                 // Append the new div to the container
//                 divContainer.appendChild(newDivbot);


//             } catch (error) {
//                 console.error('There was a problem with the fetch operation:', error);
//                 dataContainer.innerHTML = `<p style="color: red;">Failed to fetch data. Please try again.</p>`;
//             }
//         };
//         fetchData()
//     }
//     else {

//     }
//     // =========================================================




//     // if (isFound) {
//     //     const newDivbot = document.createElement('div');
//     //     // Add Tailwind CSS classes for styling
//     //     newDivbot.classList.add(
//     //         'chatbotTextBody_Bot'
//     //     );
//     //     // Set the content of the new div
//     //     newDivbot.textContent = "Hello";
//     //     chatBotTextYou.value = "";
//     //     // Append the new div to the container
//     //     divContainer.appendChild(newDivbot);
//     // }
//     // else {
//     //     alert("dfh")
//     // }

// });