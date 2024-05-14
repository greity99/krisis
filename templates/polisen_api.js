// Konstruera URL med filterparametrar
const baseUrl = 'https://polisen.se/api/events';
const filterParams = {
  type: 'Bombhot;Brand;Detonation;Farligt föremål, misstänkt;Försvunnen person;Inbrott;Inbrott, försök;Naturkatastrof;Polisinsats/kommendering;Rån;Rån väpnat; Rån övrigt;Rån, försök;Skottlossning;Skottlossning, misstänkt;Spridning smittsamma kemikalier; ',
  locationname: 'Malmö',
  datetime: 2024
};

// Konvertera filterparametrar till en del av URL:en
const url = new URL(baseUrl);
Object.keys(filterParams).forEach(key => url.searchParams.append(key, filterParams[key]));

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Hantera den returnerade datan här
    console.log(data);

    const id = "test"; // @TODO: Erätt detta med ett id (för HTML-element där data ska visas)
    const element = document.getElementById(id);
    data.map((item) => {
        element.innerHTML += `<p>${item.name}: ${item.summary}</p>`;
    });
  })
  .catch(error => {
    console.error('There was a problem with your fetch operation:', error);
  });