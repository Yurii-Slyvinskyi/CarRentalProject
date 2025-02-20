document.addEventListener("DOMContentLoaded", () => {
  const filterCars = document.getElementById("all-cars-input");

  // Пошук за моделлю автомобіля
  document.addEventListener("input", (event) => {
    if (event.target.id === "all-cars-input") {
      const value = event.target.value.toLowerCase().trim();
      const getTitles = Array.from(
        document.getElementsByClassName("card-title")
      );

      getTitles.forEach((title) => {
        const carCard = title.closest(".col");
        if (title.textContent.toLowerCase().includes(value)) {
          carCard.style.display = "";
        } else {
          carCard.style.display = "none";
        }
      });
    }
  });

  function filterCarsByType(carType) {
    const allCars = document.querySelectorAll("#results-container .col");

    allCars.forEach((car) => {
      const carTypeElement = car.querySelector(".card-title");
      const carTypeText = carTypeElement.textContent.toLowerCase();

      if (carType === "all" || carTypeText.includes(carType)) {
        car.style.display = "";
      } else {
        car.style.display = "none";
      }
    });
  }

  // Відкриття модального вікна
  document
    .getElementById("filterButton")
    .addEventListener("click", function () {
      document.getElementById("filterModal").style.display = "block";
    });

  // Закриття модального вікна
  document.querySelector(".close").addEventListener("click", function () {
    document.getElementById("filterModal").style.display = "none";
  });

  // Закриття модального вікна при кліку поза ним
  window.addEventListener("click", function (event) {
    if (event.target == document.getElementById("filterModal")) {
      document.getElementById("filterModal").style.display = "none";
    }
  });

  // Відправка форми фільтрів
  document
    .getElementById("applyFilters")
    .addEventListener("click", function () {
      applyFilters();
    });

  // Скидання фільтрів
  document
    .getElementById("resetFilters")
    .addEventListener("click", function () {
      resetFilters();
    });
});

// Функція для застосування фільтрів
function applyFilters() {
  const form = document.getElementById("filter-form");
  const formData = new FormData(form);

  fetch("/filter", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      updateResults(data);
      document.getElementById("filterModal").style.display = "none"; // Закрити модальне вікно після застосування фільтрів
    })
    .catch((error) => console.error("Error:", error));
}

// Функція для скидання фільтрів
function resetFilters() {
  // Скидання всіх чекбоксів у формі
  const form = document.getElementById("filter-form");
  const checkboxes = form.querySelectorAll("input[type='checkbox']");
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });

  // Оновлення результатів (повернення до початкового стану)
  fetch("/cars") // Замініть "/cars" на ваш ендпоінт для отримання всіх автомобілів
    .then((response) => response.json())
    .then((data) => {
      updateResults(data);
      document.getElementById("filterModal").style.display = "none"; // Закрити модальне вікно
    })
    .catch((error) => console.error("Error:", error));
}

// Функція для оновлення результатів
function updateResults(data) {
  const resultsContainer = document.getElementById("results-container");
  resultsContainer.innerHTML = ""; // Очищення контейнера перед оновленням

  data.forEach((car) => {
    const col = document.createElement("div");
    col.className = "col"; // Базовий клас для Bootstrap

    const card = document.createElement("div");
    card.className = "card h-100";

    const img = document.createElement("img");
    img.src = car.image_url || "https://via.placeholder.com/150";
    img.className = "card-img-top";
    img.alt = `${car.brand} ${car.model}`;
    img.id = "fixed-size-photo"; // Додаємо ID для фіксованого розміру зображення

    const cardBody = document.createElement("div");
    cardBody.className = "card-body d-flex flex-column";

    const title = document.createElement("h5");
    title.className = "card-title";
    title.textContent = `${car.brand} ${car.model} ${car.year}`;

    const description = document.createElement("p");
    description.className = "card-text";
    description.textContent =
      car.description || "No description available for this car.";

    const link = document.createElement("a");
    link.href = `/car/${car.slug}`;
    link.className = "btn btn-primary mt-auto";
    link.textContent = "See the car";

    // Додавання елементів у картку
    cardBody.appendChild(title);
    cardBody.appendChild(description);
    cardBody.appendChild(link);

    card.appendChild(img);
    card.appendChild(cardBody);
    col.appendChild(card);

    resultsContainer.appendChild(col);
  });
}
