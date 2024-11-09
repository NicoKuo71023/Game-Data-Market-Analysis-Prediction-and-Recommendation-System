window.addEventListener('scroll', function () {
    if (window.scrollY > 0) {
        document.querySelector('.navbar').classList.remove('navbar-top');
        document.querySelector('.search-bar').classList.add("scrolled");
        document.querySelectorAll('.fontcolor').forEach(element => {
            element.classList.add('black');
        });
        document.querySelectorAll('.nav-link').forEach(element => {
            element.classList.add('fontcolor_black');
        });
    } else {
        document.querySelector('.navbar').classList.add('navbar-top');
        document.querySelector('.search-bar').classList.remove("scrolled");
        document.querySelectorAll('.fontcolor').forEach(element => {
            element.classList.remove('black');
        });
        document.querySelectorAll('.nav-link').forEach(element => {
            element.classList.remove('fontcolor_black');
        });
    }
});


function animateCounter(elementId, targetNumber, intervalTime, addTime) {
    let currentNumber = 0;
    const element = document.getElementById(elementId);

    // 計算增量步幅，根據目標數字和間隔時間自適應
    const step = Math.ceil(targetNumber / (1000 / intervalTime));

    const interval = setInterval(() => {
        currentNumber += step; // 按步幅增加數字
        if (currentNumber >= targetNumber) {
            currentNumber = targetNumber; // 避免超過目標數字
            clearInterval(interval); // 停止計時器
        }
        element.textContent = currentNumber; // 更新元素內容
    }, intervalTime);
}

// 使用函數為多個數字元素設置動畫
// animateCounter("game-sold", 580, 40); // 設定目標數字和間隔時間
// animateCounter("counter2", 1200, 5); // 不同的目標數字和間隔時間
// animateCounter("counter3", 300, 20); // 不同的目標數字和間隔時間
window.addEventListener('load', () => {
    const title = document.getElementById("floatingTitle");
    const title_s = document.getElementById("floatingTitle_s");
    const title_s2 = document.getElementById("floatingTitle_s_2");

    // 依次延遲 0.3 秒顯示每個標題
    title.classList.add("visible");
    setTimeout(() => {
        title_s.classList.add("visible");
    }, 400); // 0.4 秒延遲

    setTimeout(() => {
        title_s2.classList.add("visible");
    }, 900); // 再延遲 0.3 秒（總共 0.6 秒）
});

const counters = [
    { id: "game-sold", targetNumber: 580, intervalTime: 40 },
    { id: "growth", targetNumber: 60, intervalTime: 40 },
    { id: "game-released", targetNumber: 14000, intervalTime: 40 },
    { id: "peak-player", targetNumber: 33.6, intervalTime: 40 }
];

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counter = counters.find(c => c.id === entry.target.id);
            if (counter) {
                animateCounter(counter.id, counter.targetNumber, counter.intervalTime);
                entry.target.style.opacity = 1; // 顯示元素
                observer.unobserve(entry.target); // 停止觀察已啟動動畫的元素
            }
        }
    });
}, { threshold: 0.5 });

// 將目標元素加入 observer
counters.forEach(counter => {
    const element = document.getElementById(counter.id);
    observer.observe(element);
});


function redirectToGameInfo() {
    const searchId = document.getElementById('searchId').value;
    if (searchId) {
        window.location.href = `/game-info?steamId=${searchId}`;
    } else {
        alert('請輸入有效的 Steam ID');
    }
}

// 下拉選單模糊搜尋
let timeout;
document.getElementById('searchId').addEventListener('input', function () {
    clearTimeout(timeout);
    const query = this.value;
    timeout = setTimeout(() => {
        if (query.length >= 1) {
            fetch(`/search-game?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    const dropdown = document.getElementById('dropdown');
                    dropdown.innerHTML = '';
                    if (data.length > 0) {
                        dropdown.style.display = 'block';
                        data.forEach(item => {
                            const li = document.createElement('li');
                            li.textContent = `${item.name} (${item.steamId})`;
                            li.onclick = () => selectGame(item.steamId, item.name);
                            dropdown.appendChild(li);
                        });
                    } else {
                        dropdown.style.display = 'none';
                    }
                });
        } else {
            document.getElementById('dropdown').style.display = 'none';
        }
    }, 300);
});




// 點擊事件監聽器，用於隱藏下拉選單
document.addEventListener('click', function (event) {
    const searchInput = document.getElementById('searchId');
    const dropdown = document.getElementById('dropdown');

    // 檢查點擊是否在搜尋框或下拉選單內
    if (!searchInput.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});


function selectGame(steamId, gameName) {
    // 選擇遊戲後，重定向到詳細頁面
    window.location.href = `/game-info?steamId=${steamId}`;
}



// game-info 從es抓下來的資料格式化
document.addEventListener('DOMContentLoaded', async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const steamId = urlParams.get('steamId');

    if (steamId) {
        // const response = await fetch(`http://127.0.0.1:5000/search?steamId=${steamId}`);
        const response = await fetch(`https://64eb-1-160-6-125.ngrok-free.app/search?steamId=${steamId}`);
        // const response = await fetch('http://127.0.0.1:5000/search?steamId=$730');
        const data = await response.json();

        if (data.length > 0) {
            const result = data[0];
            const gameDetails = document.getElementById('gameDetails');
            const gameData = document.getElementById('gameData');
            const gamePicture = document.getElementById('gamePicture');

            const releaseDate = new Date(result.releaseDate);
            const formattedDate = releaseDate.toLocaleDateString('zh-Hant', { year: 'numeric', month: 'numeric', day: 'numeric' });

            // 格式化數據
            const formattedPlaytime = result.avgPlaytime.toFixed(2) + ' 小時';  // 平均遊玩時數，保留兩位小數並加上單位
            const formattedRevenue = `$${result.revenue.toLocaleString()} 美元`;  // 收入加上千分位和美元符號
            // const formattedTotalRevenue = `$${result.totalRevenue.toLocaleString()} 美元`;  // 總收入加上千分位和美元符號
            const formattedCopiesSold = result.copiesSold.toLocaleString();  // 銷售數量加上千分位
            const formattedPlayers = result.players.toLocaleString();  // 玩家數量加上千分位
            const formattedOwners = result.owners.toLocaleString();  // 擁有者數量加上千分位
            const formattedFollowers = result.followers.toLocaleString();  // 關注者數量加上千分位
            const formattedWishlists = result.wishlists.toLocaleString();  // 願望清單數量加上千分位
            const formattedReviews = result.reviews.toLocaleString();  // 評論者數量加上千分位


            gameDetails.innerHTML = `
        <h3 style="text-align: center;">遊戲概述</h3>
        <hr style="border: 1px solid #ff9300;">
        <p>遊戲簡述: ${result.description}</p>
        <p>價格: $${result.price}</p>
        <p>開發者: ${result.developers.join(', ')}</p>
        <p>發行商: ${result.publishers.join(', ')}</p>
        <p>遊戲類型: ${result.genres.join(', ')}</p>
        <p>標籤: ${result.tags.join(', ')}</p>
        <p>發行日期: ${formattedDate}</p>
    `;


            gamePicture.innerHTML = `
        <h1 style="color: #ff9300; text-align: center;">${result.name}</h1>
        <img src="https://cdn.akamai.steamstatic.com/steam/apps/${steamId}/header.jpg" alt="" style="display: block;margin: 20px auto;">
        `;

            gameData.innerHTML += `
        <h3 style="text-align: center;">統計數據</h3>
        <hr style="border: 1px solid #ff9300;">
        <p>估計收入: ${formattedRevenue}</p>
        <p>平均遊玩時數: ${formattedPlaytime}</p>
        <p>銷售數量: ${formattedCopiesSold}</p>
        <p>活躍玩家數: ${formattedPlayers}</p>
        <p>擁有者數量: ${formattedOwners}</p>
        <p>關注者數量: ${formattedFollowers}</p>
        <p>加入願望清單數: ${formattedWishlists}</p>
        <p>評論數: ${formattedReviews}</p>
    `;

        } else {
            alert('找不到任何遊戲資訊');
        }
    }
});