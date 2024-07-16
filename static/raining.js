let records=null;
fetch("https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization="+CWB_API_KEY).then((response)=>{
	return response.json();
}).then((data)=>{
	records=data.records;
	renderRaining(0);
});
function renderRaining(page){
	let startIndex=page*10;
	let endIndex=(page+1)*10;
	const container=document.querySelector("#raining");
	for(let i=startIndex;i<endIndex;i++){
		const station=records.Station[i];
		const item=document.createElement("div");
		item.className="station";
		const name=document.createElement("div");
		name.className="name";
		name.textContent=station.StationName+"、"+station.GeoInfo.TownName+"、"+station.GeoInfo.CountyName;
		const amount=document.createElement("amount");
		amount.className="amount";
		amount.textContent=station.RainfallElement.Now.Precipitation+" mm";
		item.appendChild(name);
		item.appendChild(amount);
		container.appendChild(item);
	}
}