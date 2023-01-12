// fetch(request, {mode: 'cors'});

// fetch(
//     "/api/attractions?page=0"                       
// ).then(function(response){
//     return response.json();
// }).then(function(body){
// 	// console.log(body);     data {}
//     data = body.data;         //  []

// 	// 新增資料顯示在畫面上
//     for (let i = 0; i < data.length; i++) {
//         setAttraction(data[i]);
// 	}
	
//     // fetch頁面完
// 	   // 判斷是否有下一頁
//     nextPage = body.nextPage;
//     // console.log(nextPage);      // 1
// });

// 思考第一筆資料傳入
function setAttraction(data) {
    // console.log(data) {}
    // console.log(data.images);

	let attractionsContent = document.createElement("div");
	attractionsContent.setAttribute("class", "attractions__content");

	// <div class="attractions__space">
	let attractionsSpace = document.createElement("div");
	attractionsSpace.setAttribute("class", "attractions__space");

	// attractions__image
	let attractionsImage = document.createElement("img");
	attractionsImage.setAttribute("class", "attractions__image");
	attractionsImage.setAttribute("src", data.images[0]);

	// <div class="attractions__filter">
	let attractionsFilter = document.createElement("div");
	attractionsFilter.setAttribute("class", "attractions__filter");

	// <div class="attractions__name">
	let attractionsName = document.createElement("div");
	attractionsName.setAttribute("class", "attractions__name");
	attractionsName.innerHTML = data.name;


	// <div class="attractions__information">
	let attractionsInformation = document.createElement("div");
	attractionsInformation.setAttribute("class", "attractions__information");

	// <div class="attractions__mrt">MRT1</div>
	let attractionsMRT = document.createElement("div");
	attractionsMRT.setAttribute("class", "attractions__mrt");
	attractionsMRT.innerHTML = data.mrt;

	// <div class="attractions__cat">CAT1</div>
	let attractionsCat = document.createElement("div");
	attractionsCat.setAttribute("class", "attractions__cat");
	attractionsCat.innerHTML = data.category;


	// 找出要塞進的起始div 把資料塞進去
	// appendChild() => 找出父層，一層一層塞資料    // class="attractions"
	let attractionsDiv = document.getElementsByClassName("attractions")[0];

	// 第一層
	attractionsDiv.appendChild(attractionsContent);

	// 第二層
	attractionsContent.appendChild(attractionsSpace);
	attractionsContent.appendChild(attractionsInformation);
	// 第三層-1
	attractionsSpace.appendChild(attractionsImage);
	attractionsSpace.appendChild(attractionsFilter);
	attractionsSpace.appendChild(attractionsName);
	// 第三層-2
	attractionsInformation.appendChild(attractionsMRT);
	attractionsInformation.appendChild(attractionsCat);

};



// 自動載入
/* 
思路
1.當畫面捲動到最下面時 =>將要看到footer，自動載入新的資料
2.原本的資料仍在上面不動，所以資料資料是以新增的方式加入
3.當載入的頁面資料nextPage顯示 null 不再新增資料
*/



// 1.觀察器就是用來設定你要偵測捲動目標是否進入可見範圍的容器

//  option 是選項，都不填就會使用預設值，option 可以填的內容如下：
let options = {
  root: document.getElementsByClassName("root"),
  rootMargin: '10px',
  threshold: [0]
};


//  callback 就是當目標(target)進入/離開觀察器(root)的可見範圍會做的事。
let observer = new IntersectionObserver(callback, [options]);



// 2.指定觀察目標(entry)
let footer = document.getElementsByClassName("footer")[0];
// console.log(footer);
// console.log(typeof(footer));    
observer.observe(footer);



// 3.容器跟目標都設定好後，就可以設計 callback 要做的事了：

// 預設 page 從0開始
let nextPage = 0;

function callback(entries, observer) {
  for (const entry of entries) {
    if (entry.isIntersecting == true) {
      // 元素已經進入視窗
      // console.log("元素已經進入視窗");
      fetch(
      `/api/attractions?page=${nextPage}`
      ).then(function(response){
        return response.json();
      }).then(function(body){
        // console.log(data);     data {}
        data = body.data;         //  []
        for (let i = 0; i < data.length; i++) {
          setAttraction(data[i]);
        }
		// fetch頁面完
		// 判斷是否有下一頁
		// 第0頁,nextPage=1 ； 第1頁,nextPage=2
        nextPage = body.nextPage;
        console.log(nextPage);      // 1
		if (nextPage == null) {
			observer.disconnect();
		}
      });
    }
  }
}