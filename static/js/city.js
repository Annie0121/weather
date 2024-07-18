const CWB_API_KEY="CWB-840CF1E7-FC59-4E06-81C9-F4BB79253855";
let records=null;

const today = new Date();
const todayStr = today.toISOString().split('T')[0];


const weekTitle=document.querySelector(".info_week")

fetchWeatherData("臺北市");

function fetchWeatherData(cityName){
    fetch("/api/v1/weather/all/all/daily").then((response)=>{
        return  response.json();
            }).then((data)=>{
               
                weekTitle.textContent=`${cityName}天氣週預報`
                records = searchCity(data, cityName);
                updateWeatherDivs(records);
            
            });
}


//fetch三張圖的資料
/*
fetch("/api/v1/weather/all/all/daily").then((response)=>{
    return response.json();
}).then((data)=>{
    records = searchCity(data, "臺北市");
    updateWeatherDivs(records);

});*/


fetch("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization="+CWB_API_KEY).then((response)=>{
    return  response.json();
        }).then((data)=>{
            console.log(data);
        });

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
function updateWeatherDivs(records){
    const weatherClasses = ['city_weather_first', 'city_weather_second', 'city_weather_third'];
    for (let i = 0; i < 3; i++) {
        let time
        let datetime
        const weatherTime =records["briefDescription"][0]["start"].split(" ")[1].split(":")[0]
        const weatherdate = records["briefDescription"][0]["start"].split(" ")[0]
        const weatherDiv = document.querySelector(`.${weatherClasses[i]}`);
        const maxTemp = records["MaxT"][0]["para"][0];
        const minTemp = records["MinT"][0]["para"][0];
        const pop = records["PoP"][0]["para"][0];
        const picNumber = records["briefDescription"][0]["para"][0];
        const paddedNumber = String(picNumber).padStart(2, '0');
        const wx = records["briefDescription"][0]["para"][1]

        if(weatherTime==6){
            time="白天"
            if(weatherdate==todayStr){
                datetime ="今日白天"
            }else{
                datetime ="明日白天"
            }
        }else if(weatherTime==12){
            time="晚上"
            if(weatherdate==todayStr){
                datetime ="今日白天"
            }else{
                datetime ="明日白天"
            }
        }else{
            datetime="今晚明晨"
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

//fetch圖表 /weekly_weather/新北市

fetch("/api/v1/weekly_weather/新北市").then((response)=>{
    return response.json();
}).then((data)=>{
    console.log(data);
    //console.log(data["weather"]);
    const records = data["weather"]
    renderTable(records)
})




function renderTable(records){
    
    let weatherIndex = [9,17,10,18,11,19,12,20,13,21,14,22,15,23];
    let tableCells = document.querySelectorAll('td');
    let RHindex =[25,26,27,28,29,30,31]
    let popindex =[33,34,35,36,37,38,39]
    console.log(tableCells[9]);

    for(let i =0;i<14;i++){
        console.log(records[i]["MaxT"]);
        let MaxT= records[i]["MaxT"]
        let MinT=records[i]["MinT"]
        let PoP12h =records[i]["PoP12h"]
        let RH =records[i]["RH"]
        
        
        //天晚上氣溫
        let div = document.createElement('div');
        div.innerText = `${MinT}-${MaxT}°C`;

        tableCells[weatherIndex[i]].appendChild(div);
        //tableCells[RHindex[i]].textContent=`${RH}%`;
        //tableCells[popindex[i]].textContent=PoP12h;

        //日期
        let dateIndex = [1,2,3,4,5,6,7];
        
        const daysOfWeek = ["日", "一", "二", "三", "四", "五", "六"];
        // 使用循環來生成未來七天的日期
        for (let i = 0; i < 7; i++) {
            let nextDay = new Date(today);
            nextDay.setDate(today.getDate() + i);
            let month = nextDay.getMonth() + 1; // 月份從0開始，所以要加1
            let day = nextDay.getDate();
            let dayOfWeek = daysOfWeek[nextDay.getDay()];
            
            // 確保索引不超過 tableCells 的長度
            if (i < dateIndex.length) {
                tableCells[dateIndex[i]].innerHTML = `${month}/${day}<br>星期${dayOfWeek}`;
            }

        }
        

        
    }
}


/*

fetch("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-023?Authorization="+CWB_API_KEY).then((response)=>{
    return response.json();
}).then((data)=>{
    
    const records = data["records"]["locations"][0]["location"][0]["weatherElement"];
   //records[0]["time"][i]["startTime"].split(" ")[0]
    //console.log(records[0]["time"][2]["startTime"].split(" ")[0]);
    renderTable(records)
})

*/


//圖表渲染
/*
function renderTable(records){
    


    
    let weatherData = records[6]["time"];
    let MinDegree =records[8]["time"];
    let tableCells = document.querySelectorAll('td');
    let weatherIndex = [9,17,10,18,11,19,12,20,13,21,14,22,15,23]; // 你想要插入數據的單元格索引
    let MaxDegree =records[5]["time"];
    console.log(tableCells[1]);
   
    //日期
    let j = 0; 
    let dateIndex = [1,2,3,4,5,6,7];
    for(i=0;i<weatherData.length; i+=2){
        let dateString = records[0]["time"][i]["startTime"].split(" ")[0];
        let date = new Date(dateString);
        let month = date.getMonth() + 1; // 月份從0開始，所以要加1
        let day = date.getDate();
        let daysOfWeek = ["日", "一", "二", "三", "四", "五", "六"];
        let dayOfWeek = daysOfWeek[date.getDay()];
        tableCells[dateIndex[j]].innerHTML = `${month}/${day}<br>星期${dayOfWeek}`;
        console.log(`${month}/${day} 星期${dayOfWeek}`);
        j++;
    }

    //天氣(早上晚上)
    
    for (let i = 0; i < weatherData.length; i++) {
        let img = document.createElement('img');
        img.src=`https://www.cwa.gov.tw/V8/assets/img/weather_icons/weathers/svg_icon/day/${weatherData[i]["elementValue"][1].value}.svg`
        img.classList.add('weekpic');
        let div = document.createElement('div');
        div.innerText = `${MinDegree[i]["elementValue"][0].value}-${MaxDegree[i]["elementValue"][0].value}°C`;
        div.classList.add('weekdegree');
        tableCells[weatherIndex[i]].appendChild(img);
        tableCells[weatherIndex[i]].appendChild(div);
    }
    
    //體感溫度
    
    let bodyIndex = [25,26,27,28,29,30,31];
    let bodyMinTemp =records[11]["time"]

    
}*/