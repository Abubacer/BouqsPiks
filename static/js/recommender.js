function getRecommendations() {
  event.preventDefault();
  // Get user inputs from the form
  const gender = document.getElementById('gender').value;
  const personality = document.getElementById('personality').value;
  const occasion = document.getElementById('occasion').value;
  const priceRange = document.getElementById('priceRange').value;

  // Send user inputs to Flask server
  fetch('/get_recommendations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ gender, personality, occasion, priceRange }),
  })
  .then(response => response.json())
  .then(data => {
    // Display recommendations on the webpage
    displayRecommendations(data.recommendations);
  })
  .catch(error => console.error('Error:', error));
}

function displayRecommendations(recommendations) {
  const productCardsDiv = document.getElementById('productCards');
  productCardsDiv.innerHTML = ''; // Clear previous product cards

  // Display product cards using Bootstrap
  recommendations.forEach((recommendation, index) => {
    const cardDiv = document.createElement('div');
    cardDiv.classList.add('col-md-4', 'mb-4');

    const card = document.createElement('div');
    card.classList.add('card');

    const image = document.createElement('img');
    image.src = `/static/img/image${index + 1}.jpg`; // Assuming images are named image1.jpg, image2.jpg, etc.
    image.classList.add('card-img-top');
    image.alt = recommendation;

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    const title = document.createElement('h5');
    title.classList.add('card-title');
    title.textContent = recommendation;

    const description = document.createElement('p');
    description.classList.add('card-text');
    description.textContent = dummy_flower_data[index].description;

    const price = document.createElement('p');
    price.classList.add('card-text');
    price.textContent = `$${dummy_flower_data[index].price.toFixed(2)}`;

    const button = document.createElement('a');
    button.href = '#'; // Add a link to view more details or make a purchase
    button.classList.add('btn', 'btn-primary');
    button.textContent = 'View Details';

    // Append elements to build the card
    cardBody.appendChild(title);
    cardBody.appendChild(description);
    cardBody.appendChild(price);
    cardBody.appendChild(button);

    card.appendChild(image);
    card.appendChild(cardBody);

    cardDiv.appendChild(card);
    productCardsDiv.appendChild(cardDiv);
  });
}

