const CWB_API_KEY="CWB-840CF1E7-FC59-4E06-81C9-F4BB79253855";
let records=null;

//fetch三張圖的資料
fetch("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization="+CWB_API_KEY).then((response)=>{
    return response.json();
}).then((data)=>{
    /*  異動數字改資料["location"][3]更改縣市;*/
    const records = data.records["location"][3];
    
    console.log( records["weatherElement"][0]["time"][0]["startTime"].split(" ")[0]);
    updateWeatherDivs(records);
    
    
    
});

//渲染三張圖
function updateWeatherDivs(records){
    const weatherClasses = ['city_weather_first', 'city_weather_second', 'city_weather_third'];

    for (let i = 0; i < 3; i++) {
        console.log(records["weatherElement"][0]["time"]);
        const weatherDiv = document.querySelector(`.${weatherClasses[i]}`);
        const minTemp = records["weatherElement"][2]["time"][i]["parameter"]["parameterName"];
        const maxTemp = records["weatherElement"][4]["time"][i]["parameter"]["parameterName"];
        const pop = records["weatherElement"][1]["time"][i]["parameter"]["parameterName"];
        const wx = records["weatherElement"][3]["time"][i]["parameter"]["parameterName"];
        const picNumber = records["weatherElement"][0]["time"][i]["parameter"]["parameterValue"];
        const paddedNumber = String(picNumber).padStart(2, '0');
        weatherDiv.innerHTML = `
            <div class="toptime" >今日白天</div>
            <div  ><img src="https://www.cwa.gov.tw/V8/assets/img/weather_icons/weathers/svg_icon/day/${paddedNumber}.svg" style="height: 60PX;width: 60px;"></div>
            <div class="topdegree">${minTemp}-${maxTemp}°C </div>
            <div class="toppop" ><img src="/static/umbrella.png" style="height:15px ;width: 15px;margin-right: 5px;">${pop}%</div>
            <div class="toppop" >${wx}</div>
        `;
    }
}

//fetch圖表
fetch("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization="+CWB_API_KEY).then((response)=>{
    return response.json();
}).then((data)=>{
    const records = data["records"]["locations"][0]["location"][0]["weatherElement"];
    renderTable(records)
   
    
})


//圖表渲染
function renderTable(records){
    console.log(records);
    let weatherData = records[6]["time"];
    let MinDegree =records[8]["time"];
    let tableCells = document.querySelectorAll('td');
    let weatherIndex = [9,17,10,18,11,19,12,20,13,21,14,22,15,23]; // 你想要插入數據的單元格索引
    let MaxDegree =records[5]["time"];


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
}