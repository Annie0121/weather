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

        let date_container=document.querySelector("#date_container");
        let temperature_container=document.querySelector("#temperature_container");
        let chance_container=document.querySelector("#chance_container");
        let wet_container=document.querySelector("#wet_container")


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








    })
    .catch(error => {console.error(error)})
})

