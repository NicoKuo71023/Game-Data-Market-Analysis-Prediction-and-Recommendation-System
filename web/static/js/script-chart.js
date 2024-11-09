// 設定資料

document.addEventListener('DOMContentLoaded', function () {
    // 當表單提交後，發送資料到後端並更新圖表
    const form = document.getElementById('gameForm'); // 假設你的表單有 id="gameForm"

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // 防止表單的默認提交行為

        // 收集表單數據
        const formData = new FormData(form);

        // 將 FormData 轉換成 URLSearchParams 以便於傳遞
        const params = new URLSearchParams();
        formData.forEach((value, key) => {
            params.append(key, value);
        });

        // 發送 POST 請求到後端
        // fetch('http://127.0.0.1:5000/submit-game', {
        fetch('https://64eb-1-160-6-125.ngrok-free.app/submit-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: params
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok " + response.statusText);
                }
                return response.json();
            })
            .then(d => {
                let data = d.data;  // 從回應中取得預測數據
                // 清空現有圖表，防止重疊
                d3.select("#chart").selectAll("*").remove();
                drawChart(data);  // 使用新的數據重新繪製圖表
                console.log(data);
            })
            .catch(error => {
                console.error("Error loading data:", error);
            });
    });
});



function drawChart(data) {
    // 設定圖表尺寸和邊距
    const margin = { top: 20, right: 30, bottom: 30, left: 50 },
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // 創建 SVG 容器
    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // 設定 x 和 y 軸的比例尺
    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.price))
        .range([0, width]);

    // 使用 data 中的最小和最大 predicted_sales 值設定 y 軸範圍
    const y = d3.scaleLinear()
        .domain([d3.min(data, d => d.predicted_sales), d3.max(data, d => d.predicted_sales)])
        .nice()
        .range([height, 0]);

    // 添加 x 軸，並設定字體大小
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).ticks(5))
        .style("font-size", "14px");

    // 添加 y 軸，並設定字體大小
    svg.append("g")
        .call(d3.axisLeft(y).ticks(5))
        .style("font-size", "14px");

    // 繪製折線
    const linePath = svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "lightgrey") // 預設顏色
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(d => x(d.price))
            .y(d => y(d.predicted_sales))
        );

    // 添加點標記
    const circles = svg.selectAll("circle")
        .data(data)
        .enter().append("circle")
        .attr("cx", d => x(d.price))
        .attr("cy", d => y(d.predicted_sales))
        .attr("r", 3) // 預設半徑
        .attr("fill", "lightgrey"); // 預設顏色

    // 在整個 #chart 容器上加入 hover 效果
    d3.select("#chart")
        .on("mouseover", function () {
            linePath.transition().duration(200)
                .attr("stroke", "#d35400") // 更深的橘色
                .attr("stroke-width", 1); // 加粗

            circles.transition().duration(200)
                .attr("fill", "#d35400") // 更深的橘色
                .attr("r", 3); // 點變大
        })
        .on("mouseout", function () {
            linePath.transition().duration(200)
                .attr("stroke", "lightgrey") // 恢復原色
                .attr("stroke-width", 1.5); // 恢復原始寬度

            circles.transition().duration(200)
                .attr("fill", "lightgrey") // 恢復原色
                .attr("r", 3); // 點恢復原始大小
        });
}

