const baseUrl = 'https://polisen.se/api/events';
const filterParams = {
  type: 'Bombhot;Brand;Detonation;Farligt föremål, misstänkt;Försvunnen person;Inbrott;Inbrott, försök;Naturkatastrof;Polisinsats/kommendering;Rån;Rån väpnat; Rån övrigt;Rån, försök;Skottlossning;Skottlossning, misstänkt;Spridning smittsamma kemikalier; ',
  locationname: 'Malmö',
  datetime: 2024
};

// Konvertera filterparametrar till en del av URL:en
const url = new URL(baseUrl);
Object.keys(filterParams).forEach(key => url.searchParams.append(key, filterParams[key]));

// Använd Fetch API för att skicka GET-förfrågan för API-anropet
fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Konvertera svaret till JSON-format
  })
  .then(data => {
    // Loopa igenom varje händelse i datan och skapa HTML-kort för varje händelse
    data.forEach(event => {
      const card = document.createElement('div');
      card.classList.add('card', 'mx-4', 'mt-3');

      const cardBody = document.createElement('div');
      cardBody.classList.add('card-body');

      const title = document.createElement('h5');
      title.classList.add('card-title');
      title.textContent = event.name; // Antag att 'name' är titeln på händelsen

      const description = document.createElement('p');
      description.classList.add('card-text');
      description.textContent = event.summary; // Antag att 'summary' är beskrivningen av händelsen

      const eventDetails = document.createElement('p');
      eventDetails.classList.add('card-text');
      eventDetails.textContent = `${event.datetime} - ${event.locationname}`; // Antag att 'datetime' är datumet för händelsen och 'locationname' är platsen

      // Lägg till skapade elementen till card body
      cardBody.appendChild(title);
      cardBody.appendChild(description);
      cardBody.appendChild(eventDetails);

      // Lägg till card body i card
      card.appendChild(cardBody);

      // Lägg till card i den del av HTML:en där du vill visa korten
      const mainElement = document.querySelector('main'); // Här antar vi att korten ska visas inuti <main> elementet
      mainElement.appendChild(card);
    });
  })
  .catch(error => {
    console.error('There was a problem with your fetch operation:', error);
  });