//header
const header = document.querySelector('.fixed-header');
window.addEventListener('scroll', () => {
    if (window.scrollY > 0) {
        header.style.backgroundColor = 'black';
    } else {
        header.style.backgroundColor = 'transparent';
    }
});
//end
//icon header
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.toggle-button');
    const nav = document.querySelector('.profile_main_contener nav');
  
    toggleButton.addEventListener('click', function() {
      nav.classList.toggle('hidden');
    });
    function checkWindowSize() {
      if (window.innerWidth <= 1100) {
        nav.classList.add('hidden');
      } else {
        nav.classList.remove('hidden');
      }
    }
    window.addEventListener('resize', checkWindowSize);
    checkWindowSize();
  });


  
  document.addEventListener('DOMContentLoaded', function () {
    var menuButton = document.getElementById('menu-button');
    var dropdownContent = document.querySelector('.center-content');
    var header = document.querySelector('header');
    menuButton.addEventListener('click', function () {
        header.style.backgroundColor = 'black';
        dropdownContent.classList.toggle('show');
    });
});





document.getElementById("catalogLink").addEventListener("click", function(event) {
    event.preventDefault();
    window.location.href = "/#type_products";
});



document.addEventListener('DOMContentLoaded', function () {
    
    window.addEventListener('load', function () {
        document.body.classList.add('loaded');
    });




    var scrollLinks = document.querySelectorAll('.scroll-link');
  
    scrollLinks.forEach(function(scrollLink) {
      scrollLink.addEventListener('click', function(event) {
        event.preventDefault();
  
        var targetId = this.getAttribute('href').substring(1);
  
        var targetElement = document.getElementById(targetId);
  
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      });
    });


    const menuButton = document.getElementById('menu-button');
    const menu = document.querySelector('.left-content nav str');

    menuButton.addEventListener('click', function () {
        if (menu.style.display === 'block') {
        menu.style.display = 'none';
        } else {
        menu.style.display = 'block';
        header.style.backgroundColor = 'black';
        }
    });

    var radio1 = document.getElementById('radio1');
    var radio2 = document.getElementById('radio2');
    var radio3 = document.getElementById('radio3');
    var order_country = document.querySelector('.order_country');
    var order_receiving_point = document.querySelector('.order_receiving_point');
    var order_street = document.querySelector('.order_street');
    var order_house = document.querySelector('.order_house');
    var order_flat = document.querySelector('.order_flat');
    var dbE = document.querySelector('.dbE');
    var ddE = document.querySelector('.ddE');
    var wws = document.querySelector('.wws');
    var ttam_dbE = document.querySelector('.ttam_dbE');
    var ttam_ddE = document.querySelector('.ttam_ddE');
    var ttam_wws = document.querySelector('.ttam_wws');

    function hideAllContainers() {
        order_country.style.display = 'none';
        order_receiving_point.style.display = 'none';
        order_street.style.display = 'none';
        order_house.style.display = 'none';
        order_flat.style.display = 'none';
        dbE.style.display = 'none';
        ddE.style.display = 'none';
        wws.style.display = 'none';
        ttam_dbE.style.display = 'none';
        ttam_ddE.style.display = 'none';
        ttam_wws.style.display = 'none';
    }

    function clearAllInputs() {
        var inputs = document.querySelectorAll('.order_country input, .order_receiving_point input, .order_street input, .order_house input, .order_flat input');
        inputs.forEach(function(input) {
            input.value = '';
        });
    }

    radio1.addEventListener('click', function() {
        if (radio1.checked) {
            if (order_receiving_point.style.display === 'block') {
                hideAllContainers();
                radio1.checked = false;
            } else {
                hideAllContainers();
                clearAllInputs();
                order_receiving_point.style.display = 'block';
                dbE.style.display = 'block';
                ttam_dbE.style.display = 'block';

            }
        }
    });

    radio2.addEventListener('click', function() {
        if (radio2.checked) {
            if (order_street.style.display === 'block') {
                hideAllContainers();
                radio2.checked = false;
            } else {
                hideAllContainers();
                clearAllInputs();
                order_street.style.display = 'block';
                order_house.style.display = 'block';
                order_flat.style.display = 'block';
                ddE.style.display = 'block';
                ttam_ddE.style.display = 'block';

            }
        }
    });

    radio3.addEventListener('click', function() {
        if (radio3.checked) {
            if (order_country.style.display === 'block') {
                hideAllContainers();
                radio3.checked = false;
            } else {
                hideAllContainers(); 
                clearAllInputs();
                order_country.style.display = 'block';
                order_street.style.display = 'block';
                order_house.style.display = 'block';
                order_flat.style.display = 'block';
                wws.style.display = 'block';
                ttam_wws.style.display = 'block';
            
            }
        }
    });

    function restrictToEnglishLetters(event) {
        var input = event.target;
        var value = input.value;
        var regex = /[^a-zA-Z ]/g;
        input.value = value.replace(regex, '');
    }

    var englishOnlyInputs = document.querySelectorAll('.english-only');
    englishOnlyInputs.forEach(function(input) {
        input.addEventListener('input', restrictToEnglishLetters);
    });

    function restrictToNumeric(event) {
        var input = event.target;
        var value = input.value;
        var regex = /[^a-zA-Z0-9 ]/g;
        input.value = value.replace(regex, '');
    }

    var numericOnlyInputs = document.querySelectorAll('.numeric-eng');
    numericOnlyInputs.forEach(function(input) {
        input.addEventListener('input', restrictToNumeric);
    });


    function restrictToNumericPlus(event) {
        var input = event.target;
        var value = input.value;    
        var regex = /[^0-9\+]/g;

        input.value = value.replace(regex, '');
    }

    var numericPlusOnlyInputs = document.querySelectorAll('.numeric-plus-only');

    numericPlusOnlyInputs.forEach(function(input) {
        input.addEventListener('input', restrictToNumericPlus);
    });


    //---------------------------------------------- city list begin
    let belarusCities = [];

    function loadBelarusCities() {
        const username = 'tw1chee2k';
        const url = `https://secure.geonames.org/searchJSON?country=BY&maxRows=1000&username=${username}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.geonames) {
                    belarusCities = data.geonames.map(city => city.name);
                }
            })
            .catch(error => console.error('Ошибка при загрузке городов:', error));
    }
    
    function updateCityContainer(inputText) {
        const cityContainer = document.getElementById('cityContainer');
        cityContainer.innerHTML = '';
    
        if (inputText.trim() === '') {
            cityContainer.style.display = 'block';
            return;
        }
    
        const filteredCities = belarusCities.filter(city => city.toLowerCase().includes(inputText.toLowerCase()));
        filteredCities.forEach(city => {
            const cityItem = document.createElement('div');            
            const form_radio1 = document.getElementById('form_radio1');
            const form_radio2 = document.getElementById('form_radio2');
            cityItem.classList.add('city_item');
            cityItem.textContent = city;

            cityItem.addEventListener('click', function() {
                document.getElementById('cityInput').value = city;
                form_radio1.style.display = 'block';
                form_radio2.style.display = 'block';
                cityContainer.style.display = 'none';

            });
            cityContainer.appendChild(cityItem);
        });
    
        if (filteredCities.length > 0) {
            cityContainer.style.display = 'block';
            
        } else {
            cityContainer.style.display = 'none';
        }
    }
    
    loadBelarusCities();
    
    cityInput.addEventListener('input', function() {
        updateCityContainer(this.value);
    });
    //---------------------------------------------- city list end
    //---------------------------------------------- input city
    cityInput.addEventListener('input', function() {
        const enteredCity = this.value.trim();
        const foundCity = belarusCities.find(city => city.toLowerCase() === enteredCity.toLowerCase());
        const form_radio1 = document.getElementById('form_radio1');
        const form_radio2 = document.getElementById('form_radio2');
    
        if (foundCity) {
            form_radio1.style.display = 'block';
            form_radio2.style.display = 'block';
            console.log(`City "${foundCity}" was found in db!`);
        } else {
            form_radio1.style.display = 'none';
            form_radio2.style.display = 'none';
            console.log(`City "${enteredCity}" not found in db.`);
        }
    });
    //---------------------------------------------- input city end
    var receivingPointInput = document.getElementById("receiving_point");
    var receivingPointContainer = document.querySelector(".cont_receiving_point");
    
    receivingPointInput.addEventListener("click", function() {
        receivingPointContainer.style.display = "block";
    });
    
    var receivingPointItems = document.querySelectorAll(".receiving_point_item");
    
    receivingPointItems.forEach(function(item) {
        item.addEventListener("click", function() {
            var numberText = this.querySelector("span:first-child").textContent;
            var numberMatch = numberText.match(/№(\d+),/);
            var number = numberMatch ? numberMatch[1] : '';
            var input = document.getElementById("receiving_point");
            input.value = number;
            receivingPointContainer.style.display = "none";
        });
    });
    
});

document.addEventListener("DOMContentLoaded", function() {
    const thumbnails = document.querySelectorAll(".thumbnailIMG_prod img");
    const mainImage = document.querySelector(".mainIMG_prod");

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener("click", function() {
            const newImageSrc = this.getAttribute("src");
            mainImage.style.opacity = "0";
            setTimeout(function() {
                mainImage.setAttribute("src", newImageSrc);
                mainImage.style.opacity = "1"; 
            }, 200); 
        });
    });
});

//end
//info message
var alertBox = document.querySelector('.custom-alert');
alertBox.style.display = 'block';
setTimeout(function() {
    alertBox.classList.add('hidden');
}, 2000);
//end
//del item in basket
function deleteItem(id) {
    fetch("/remove_item", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: id })
    }).then((response) => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error("Ошибка при удалении товара");
        }
    });
    }
//end
//---------------------------------------------- city list begin
let belarusCities = [];

function loadBelarusCities() {
    const username = 'tw1chee2k';
    const url = `https://secure.geonames.org/searchJSON?country=BY&maxRows=1000&username=${username}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.geonames) {
                belarusCities = data.geonames.map(city => city.name);
            }
        })
        .catch(error => console.error('Ошибка при загрузке городов:', error));
}

function updateCityContainer(inputText) {
    const cityContainer = document.getElementById('cityContainer');
    cityContainer.innerHTML = '';

    if (inputText.trim() === '') {
        cityContainer.style.display = 'block';
        return;
    }

    const filteredCities = belarusCities.filter(city => city.toLowerCase().includes(inputText.toLowerCase()));
    filteredCities.forEach(city => {
        const cityItem = document.createElement('div');            
        const form_radio1 = document.getElementById('form_radio1');
        const form_radio2 = document.getElementById('form_radio2');
        cityItem.classList.add('city_item');
        cityItem.textContent = city;

        cityItem.addEventListener('click', function() {
            document.getElementById('cityInput').value = city;
            form_radio1.style.display = 'block';
            form_radio2.style.display = 'block';
            cityContainer.style.display = 'none';

        });
        cityContainer.appendChild(cityItem);
    });

    if (filteredCities.length > 0) {
        cityContainer.style.display = 'block';
        
    } else {
        cityContainer.style.display = 'none';
    }
}

loadBelarusCities();

cityInput.addEventListener('input', function() {
    updateCityContainer(this.value);
});
//---------------------------------------------- city list end
//---------------------------------------------- input city
cityInput.addEventListener('input', function() {
    const enteredCity = this.value.trim();
    const foundCity = belarusCities.find(city => city.toLowerCase() === enteredCity.toLowerCase());
    const form_radio1 = document.getElementById('form_radio1');
    const form_radio2 = document.getElementById('form_radio2');

    if (foundCity) {
        form_radio1.style.display = 'block';
        form_radio2.style.display = 'block';
        console.log(`City "${foundCity}" was found in db!`);
    } else {
        form_radio1.style.display = 'none';
        form_radio2.style.display = 'none';
        console.log(`City "${enteredCity}" not found in db.`);
    }
});
//---------------------------------------------- input city end