

let weather_container=document.querySelector("#weather_container");
let all_weather_rows=document.querySelectorAll(".weather__row");


console.log("確定有抓到所有天氣區塊的DOM",all_weather_rows)


// >監聽事件：網頁Load完後，就向後端取得
document.addEventListener("DOMContentLoaded",function(){


    fetch("/api/v1/weather/all/all/daily")
    .then((response)=>{
        if(response.ok){return response.json()}
        else {throw new Error("API request failed")}
    })
    .then((data)=>{
        console.log(data)
        console.log(Object.keys(data[0])[0])
        // create_weather_row(data)
    })
    .catch(error => {console.error(error)})


})


function create_weather_row(data){

    // >建立最外層的div
    let new_weather_row=document.createElement("div");
    new_weather_row.classList.add("weather__row");

    // >建立『城市名稱』的div
    let new_city_name=document.createElement("div");
    new_city_name.classList.add("weather__city-name");
    new_city_name.textContent=Object.keys(data)[0];

    new_weather_row.appendChild(new_city_name);


    // >建立『天氣icon』的image
    let new_weather_icon=document.createElement("img");

    //__寫到一半！
}



// >透過迴圈，針對每個城市方塊建立點擊的監聽事件，點了之後就會呼叫慧倫的函式＋轉跳到她的city頁面
all_weather_rows.forEach(row => {
    row.addEventListener("click",function(event){

        const selected_city=row.querySelector(".weather__city-name").textContent.trim();

        window.location.href = '/city';
        // ++這邊改成要轉跳畫面＋呼叫會輪到時候寫好的函式（記得import)
    })
})




