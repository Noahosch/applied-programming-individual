const quotes = [
  { text: "It is never too late to be what you might have been.", author: "George Eliot" },
  { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
  { text: "Act as if what you do makes a difference. It does.", author: "William James" },
  { text: "Great things are done by a series of small things brought together.", author: "Vincent van Gogh" },
  { text: "How we spend our days is, of course, how we spend our lives.", author: "Annie Dillard" },
  { text: "Nothing will work unless you do.", author: "Maya Angelou" },
  { text: "The journey of a thousand miles begins with one step.", author: "Lao Tzu" },
  { text: "Do what you can, with what you have, where you are.", author: "Theodore Roosevelt" },
  { text: "You do not have to see the whole staircase. Just take the first step.", author: "Martin Luther King Jr." },
  { text: "Wherever you are, be all there.", author: "Jim Elliot" },
  { text: "The best way out is always through.", author: "Robert Frost" },
  { text: "And now that you don't have to be perfect, you can be good.", author: "John Steinbeck" }
];

const clock = document.querySelector("#clock");
const date = document.querySelector("#date");
const quote = document.querySelector("#quote");
const quoteAuthor = document.querySelector("#quote-author");
const formatToggle = document.querySelector("#format-toggle");
const nextQuote = document.querySelector("#next-quote");

let use24Hour = localStorage.getItem("stillpoint-24-hour") !== "false";
let lastQuoteIndex = -1;

function updateClock() {
  const now = new Date();
  clock.dateTime = now.toISOString();
  clock.textContent = new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
    hour12: !use24Hour
  }).format(now);
  date.textContent = new Intl.DateTimeFormat(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric"
  }).format(now);
}

function updateFormatButton() {
  formatToggle.textContent = use24Hour ? "24H" : "12H";
  formatToggle.setAttribute("aria-label", `Switch to ${use24Hour ? "12" : "24"}-hour time`);
}

function showAnotherQuote() {
  let quoteIndex;
  do {
    quoteIndex = Math.floor(Math.random() * quotes.length);
  } while (quotes.length > 1 && quoteIndex === lastQuoteIndex);

  lastQuoteIndex = quoteIndex;
  quote.textContent = `“${quotes[quoteIndex].text}”`;
  quoteAuthor.textContent = quotes[quoteIndex].author;
}

formatToggle.addEventListener("click", () => {
  use24Hour = !use24Hour;
  localStorage.setItem("stillpoint-24-hour", String(use24Hour));
  updateFormatButton();
  updateClock();
});

nextQuote.addEventListener("click", showAnotherQuote);

updateFormatButton();
updateClock();
showAnotherQuote();
window.setInterval(updateClock, 1000);