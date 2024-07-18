const CWB_API_KEY="CWB-840CF1E7-FC59-4E06-81C9-F4BB79253855";
let records=null;

const weekTitle=document.querySelector(".info_week")
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0'); 
const day = String(today.getDate()).padStart(2, '0'); 
const todayStr = `${year}-${month}-${day}`;
console.log(todayStr);

let decodedUrl=null
let currentUrl = window.location.href;
if(decodedUrl){
    decodedUrl=''
}else{
    decodedUrl = decodeURIComponent(currentUrl.split("/")[4]);
}



fetchWeatherData(decodedUrl);


function fetchWeatherData(cityName){
    fetch("/api/v1/weather/all/all/daily").then((response)=>{
        return  response.json();
            }).then((data)=>{
                weekTitle.textContent=`${cityName}天氣週預報`
                console.log(data[0]);
                records = searchCity(data, cityName);
                if(records){
                    
                    updateWeatherDivs(records,todayStr);
                }
                
            
            });
}







//尋找指定的城市
function searchCity(data, cityName) {
    for (let i = 0; i < data.length; i++) {
        if (data[i][cityName]) {
            return data[i][cityName];
        }
    }
    return null; 
}


//渲染三張圖
function updateWeatherDivs(records,todayStr){
    
    const weatherClasses = ['city_weather_first', 'city_weather_second', 'city_weather_third'];
    for (let i = 0; i < 3; i++) {
        let time
        let datetime
        const starweatherTime =records["briefDescription"][i]["start"].split(" ")[1].split(":")[0]
        const starweatherdate = records["briefDescription"][i]["start"].split(" ")[0]
        const endweatherTime =records["briefDescription"][i]["end"].split(" ")[1].split(":")[0]
        const endweatherdate = records["briefDescription"][i]["end"].split(" ")[0]
        const weatherDiv = document.querySelector(`.${weatherClasses[i]}`);
        const maxTemp = records["MaxT"][i]["para"][0];
        const minTemp = records["MinT"][i]["para"][0];
        const pop = records["PoP"][i]["para"][0];
        const picNumber = records["briefDescription"][i]["para"][0];
        const paddedNumber = String(picNumber).padStart(2, '0');
        const wx = records["briefDescription"][i]["para"][1]
        console.log(endweatherdate);
        
        if(starweatherdate == todayStr && endweatherdate == todayStr){
           
            if(starweatherTime<6){
                datetime="今天清晨"
            }else if(starweatherTime>=6 && starweatherTime<18){
                datetime="今天早上"
            }else if(starweatherTime>=18 && starweatherTime<24){
                datetime="今天晚上"
            }  
        }else if(starweatherdate == todayStr && endweatherdate != todayStr){
            datetime="今晚明晨"
        }else{
            if(starweatherTime<6){
                datetime="明天清晨"
            }else if(starweatherTime>=6 && starweatherTime<18){
                datetime="明天早上"
            }else if(starweatherTime>=18 && starweatherTime<24){
                datetime="明天晚上"
            } 
        }
       
        
       

        weatherDiv.innerHTML = `
            <div class="toptime" >${datetime}</div>
            <div><img src="https://www.cwa.gov.tw/V8/assets/img/weather_icons/weathers/svg_icon/day/${paddedNumber}.svg" style="height: 60PX;width: 60px;"></div>
            <div class="topdegree">${minTemp}-${maxTemp}°C </div>
            <div class="toppop" ><img src="/static/umbrella.png" style="height:15px ;width: 15px;margin-right: 5px;">${pop}%</div>
            <div class="toppop" >${wx}</div>
        `;
    }
}

//表格

function renderTable(records) {
    console.log(records[0]);
    let weatherIndex = [9, 17, 10, 18, 11, 19, 12, 20, 13, 21, 14, 22, 15, 23];
    let tableCells = document.querySelectorAll('td');
    tableCells[0].textContent=`${decodedUrl}`
    if (records[0].time === "晚上") {
        // render 橫槓
        let div = document.createElement('div');
        div.innerText = "-";
        tableCells[weatherIndex[0]].appendChild(div);
        // render 剩下的 13 筆資料
        for (let i = 1; i < 14; i++) {
            renderWeatherData(tableCells, weatherIndex[i], records[i - 1]);
        }
    } else if (records[0].time === "半夜") {
        // render 扣除半夜的，剩下的 14 筆資料
        for (let i = 0; i < 14; i++) {
            renderWeatherData(tableCells, weatherIndex[i], records[i + 1]);
        }
    }
    else {
        // render  14 筆資料
        for (let i = 0; i < 14; i++) {
            renderWeatherData(tableCells, weatherIndex[i], records[i]);
        }
    }

    // render 日期
    renderDates(tableCells);
}

function renderWeatherData(tableCells, cellIndex, record) {
    let MaxT = record["MaxT"];
    let MinT = record["MinT"];
    
    let Wx =record["Wx"]
    let div = document.createElement('div');
    let img = document.createElement('img');
    div.classList.add('weekdegree');
    img.classList.add('weekpic');
    img.src=`https://www.cwa.gov.tw/V8/assets/img/weather_icons/weathers/svg_icon/day/${Wx}.svg`
    div.innerText = `${MinT}-${MaxT}°C`;
    tableCells[cellIndex].appendChild(img);
    tableCells[cellIndex].appendChild(div);
}

function renderDates(tableCells) {
    let dateIndex = [1, 2, 3, 4, 5, 6, 7];
    const daysOfWeek = ["日", "一", "二", "三", "四", "五", "六"];
    for (let i = 0; i < 7; i++) {
        let nextDay = new Date(today);
        nextDay.setDate(today.getDate() + i);
        let month = nextDay.getMonth() + 1;
        let day = nextDay.getDate();
        let dayOfWeek = daysOfWeek[nextDay.getDay()];
        if (i < dateIndex.length) {
            tableCells[dateIndex[i]].innerHTML = `${month}/${day}<br>星期${dayOfWeek}`;
        }
    }
}

fetch(`/api/v1/weekly_weather/${decodedUrl}`).then((response) => {
    return response.json();
}).then((data) => {
    const records = data["weather"];
    renderTable(records);
});



