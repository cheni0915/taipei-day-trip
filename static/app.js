// 抓取圖片資料放置位置
let attractions_images = document.getElementsByClassName("attractions__image");
let attractions_names = document.getElementsByClassName("attractions__name");
let attractions_mrts = document.getElementsByClassName("attractions__mrt");
let attractions_cats = document.getElementsByClassName("attractions__cat");

// 12筆資料
// console.log(attractions_mrts);

// "http://18.180.213.40:3000/api/attractions?page=1"     EC2
// "http://192.168.2.168:3000/api/attractions?page=0"     自家

// fetch(request, {mode: 'cors'});


fetch(
    "http://192.168.2.168:3000/api/attractions?page=0"
).then(function(response){
    return response.json();
}).then(function(data){
    // console.log(data);     data {}
    data = data.data;         //  []

    /**
     *  fetch到資料後
     *  1.抓出需要的資料
     *  2.另外開function建構放置資料位置
     * 
     */
    for (let i = 0; i < data.length; i++) {
        // 12筆景觀資料   index 0~11   id 1~12
        // console.log(data);
        // console.log(data[i].category);

        // 這樣會放到內文裡，圖片是要更改src連結的部分
        // attractions_images[i].innerHTML = data[i].images[0];

        attractions_images[i].setAttribute("src", data[i].images[0]);
        attractions_names[i].innerHTML = data[i].name;
        attractions_mrts[i].innerHTML = data[i].mrt;
        attractions_cats[i].innerHTML = data[i].category;

    }



});
    // 網頁讀取資料
    // 創造div裡面內容
    /**
    <div class="attractions"></div>
        <div class="attractions__content">
            <div class="attractions__space">
                 <img
                    src="{{ url_for('static', filename='image/welcome.png') }}"
                    class="attractions__image"
                    alt=""
                 />
                <div class="attractions__filter"></div>
                <div class="attractions__name">test1</div>
            </div>
            <div class="attractions__information">
                <div class="attractions__mrt">MRT1</div>
                <div class="attractions__cat">CAT1</div>
            </div>
        </div>
     */










/* 
思路
1.當畫面捲動到最下面時 =>將要看到footer，自動載入新的資料
2.原本的資料仍在上面不動，所以資料資料是以新增的方式加入
3.當載入的頁面資料nextPage顯示 null 不再新增資料

*/


/*

root
指定的容器，比如要偵測 #container 內的目標是否進入可見範圍，就可以像這樣設定：
root: document.getElementById('container');
預設為 null 也就是代表整個頁面(body)。

rootMargin
意思是移動到目標的相對位置，
預設四邊都是 0px，如果設定 10px 的話，
代表是距離目標還有 10px 時才會觸發事件，也可以設定負值，
比如設定 -20px 的話，代表已經進入目標 20px 後才會觸發事件。

threshold
這個參數是設定目標進入可見範圍多少百分比後會觸發，用陣列帶入，比如：
threshold: [0, 0.25, 0.5]
就會目標出現 0%(也就是剛出現)、25% 及 50% 時都觸發事件。


*/ 






// 1.觀察器就是用來設定你要偵測捲動目標是否進入可見範圍的容器

//  option 是選項，都不填就會使用預設值，option 可以填的內容如下：
// let options = {
//   root: document.getElementsByClassName("root"),
//   rootMargin: '10px',
//   threshold: [0]
// };


//  callback 就是當目標(target)進入/離開觀察器(root)的可見範圍會做的事。
// let observer = new IntersectionObserver(callback, [options]);



// 2.指定觀察目標(entry)
// let footer = document.getElementsByClassName("footer__content");
// console.log(typeof(footer))
// observer.observe(footer);


// 3.容器跟目標都設定好後，就可以設計 callback 要做的事了：
// function callback(entry) {
// }




// observer.observe(footer);

// function callback(entries, observer) {
//   for (const entry of entries) {
//     if (entry.intersectionRatio > 0) {
//       // 元素已經進入視窗
//       console.log("元素已經進入視窗");
//     } else {
//       // 元素已經離開視窗
//       console.log("元素已經離開視窗");
//     }
//   }
// }

