// Konstruera URL med filterparametrar för första API-anropet
const baseUrl = 'https://polisen.se/api/events';
const filterParams = {
  type: 'Bombhot;Brand;Detonation;Farligt föremål, misstänkt;Försvunnen person;Inbrott;Inbrott, försök;Naturkatastrof;Polisinsats/kommendering;Rån;Rån väpnat; Rån övrigt;Rån, försök;Skottlossning;Skottlossning, misstänkt;Spridning smittsamma kemikalier; ',
  locationname: 'Malmö',
  datetime: 2024
};

// Konvertera filterparametrar till en del av URL:en
const url = new URL(baseUrl);
Object.keys(filterParams).forEach(key => url.searchParams.append(key, filterParams[key]));

// Använd Fetch API för att skicka GET-förfrågan för första API-anropet
fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Hantera den returnerade datan från första API-anropet här
    console.log(data);

    const id = "test"; // @TODO: Ersätt detta med ett id för HTML-element där data ska visas
    const element = document.getElementById(id);
    data.map((item) => {
        element.innerHTML += `<p>${item.name}: ${item.summary}</p>`;
    });
  })
  .catch(error => {
    console.error('There was a problem with your fetch operation:', error);
  });

// Konstruera URL för andra API-anropet
const secondUrl = 'https://polisen.se/api/events'; // Ersätt detta med den faktiska URL:en för det andra API:et

// Använd Fetch API för att skicka GET-förfrågan för andra API-anropet
fetch(secondUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.text(); 
  })
  .then(data => {
    // Dela upp den returnerade texten baserat på radbrytningar (\n)
    const events = data.split('\n');

    // Loopa igenom varje händelse
    events.forEach(event => {
      // Dela upp varje händelse baserat på kommatecken
      const eventDetails = event.split(', ');

      // Skapa nya HTML-element för varje händelse
      const card = document.createElement('div');
      card.classList.add('card', 'mx-4');

      const cardBody = document.createElement('div');
      cardBody.classList.add('card-body');

      const title = document.createElement('h5');
      title.classList.add('card-title');
      title.textContent = eventDetails[1]; // Händelse typ

      const description = document.createElement('p');
      description.classList.add('event-description');
      description.textContent = eventDetails[3]; // Beskrivning

      const cardFooter = document.createElement('div');
      cardFooter.classList.add('card-footer', 'small', 'text-muted');
      cardFooter.innerHTML = `Publicerad: <span class="event-date">${eventDetails[0]}</span>, ${eventDetails[2]}`; // Datum och plats

      // Lägg till skapade elementen till DOM:en
      cardBody.appendChild(title);
      cardBody.appendChild(description);
      card.appendChild(cardBody);
      card.appendChild(cardFooter);

      const eventContainer = document.getElementById('event-container');
      eventContainer.appendChild(card);
    });
  })
  .catch(error => {
    console.error('There was a problem with your fetch operation:', error);
  });
