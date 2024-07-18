document.addEventListener("DOMContentLoaded", function () {
    backToMainPage();
  });


function backToMainPage() {
    const titleElement = document.getElementById("title");
    titleElement.addEventListener("click", function () {
    window.location.href = "/";
});
}


document.addEventListener("DOMContentLoaded",function(){

    //>取得路徑後，做切割，好取得我們要的城市＋鄉鎮資料
    let url=location.pathname;
    let url_split=url.split("/");
    url_split = url_split.map(part => decodeURIComponent(part));

    let selected_city=url_split[2];
    let selected_district=url_split[3];


    console.log(selected_city)


    let topic=document.querySelector("#topic");
    topic.textContent=`${selected_city}${selected_district} 一週晚間預報`


    fetch(`/api/v1/weather/${selected_city}/${selected_district}`)
    .then(response => {
        if(response.ok){return response.json()}
        else {throw new Error("API request failed")}
    })
    .then(data => {

        const weather_table = document.querySelector("#weather_table");
        const weather_container=document.querySelector("#weather_container");


        // >監聽事件：隨時監測畫面是否有大小改變，如果有，依照寬度渲染對應的內容
        window.addEventListener('resize', checkScreenWidth);
        checkScreenWidth();
    

        // > 函式：用來判斷螢幕寬度
        function checkScreenWidth(){
            if (window.innerWidth <= 1200) {
                weather_table.style.display = 'none';
                weather_container.style.display = 'flex';
                render_blocks();
            } else {
                weather_table.style.display = 'table';
                weather_container.style.display = 'none';
                render_table();
            }
        };


        // >函式：寬度為桌機大小時，渲染畫面用
        function render_table(){

            let date_container=document.querySelector("#date_container");
            let temperature_container=document.querySelector("#temperature_container");
            let chance_container=document.querySelector("#chance_container");
            let wet_container=document.querySelector("#wet_container")

            date_container.innerHTML = '<td class="title">日期</td>';
            temperature_container.innerHTML = '<td class="title">最高體感溫度</td>';
            chance_container.innerHTML = '<td class="title">12小時降雨機率</td>';
            wet_container.innerHTML = '<td class="title">平均相對濕度</td>';
    
    
            data.weather.slice(0,7).forEach( weather => {
    
    
                // >日期
                let new_date_td=document.createElement("td");
                new_date_td.classList.add("title");
                new_date_td.textContent=weather.date
                date_container.appendChild(new_date_td);
    
                // >體感溫度
                let new_temperature_td=document.createElement("td");
                new_temperature_td.textContent=`${weather.details[2].value}°C`
                temperature_container.appendChild(new_temperature_td);
    
                // >降雨機率
                let new_chance_td=document.createElement("td");
                if (weather.details[0].value === " "){
                    new_chance_td.textContent="-"
                }
                else {
                    new_chance_td.textContent=`${weather.details[0].value}%`
                }
                chance_container.appendChild(new_chance_td);
    
    
                // >濕度
                let new_wet_td=document.createElement("td");
                new_wet_td.textContent=`${weather.details[1].value}%`;
                wet_container.appendChild(new_wet_td);
            })
        }


        // >函式：寬度為手機與平板大小時，渲染畫面用
        function render_blocks(){

            weather_container.innerHTML = '';

            data.weather.slice(0, 7).forEach(weather => {

                let weather_block = document.createElement("div");
                weather_block.classList.add("weather-block");

                weather_block.innerHTML = `
                    <div class="weather-item">
                        <span class="weather-label">日期</span>
                        <span class="weather-value">${weather.date}</span>
                    </div>
                    <div class="weather-item">
                        <span class="weather-label">最高體感溫度</span>
                        <span class="weather-value">${weather.details[2].value}°C</span>
                    </div>
                    <div class="weather-item">
                        <span class="weather-label">12小時降雨機率</span>
                        <span class="weather-value">${weather.details[0].value === " " ? "-" : weather.details[0].value + '%'}</span>
                    </div>
                    <div class="weather-item">
                        <span class="weather-label">平均相對濕度</span>
                        <span class="weather-value">${weather.details[1].value}%</span>
                    </div>
                `;

                weather_container.appendChild(weather_block);
            });


        };

    })
    .catch(error => {console.error(error)})
})

