function addToCache(selectId) {
    const selectElement = document.getElementById(selectId);
    const selectedOptions = Array.from(selectElement.selectedOptions).map(option => option.text);

    if (selectedOptions.length > 0) {
        const list = document.getElementById('cachedSelections');
        selectedOptions.forEach(option => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            listItem.textContent = option;
            listItem.addEventListener('click', () => {
                // 點擊已選項目，移除它
                list.removeChild(listItem);
                removeFromHiddenInputs(option); // 同時更新隱藏的輸入
            });
            list.appendChild(listItem);
        });
        selectElement.selectedIndex = 0; // 重置選單
    } else {
        alert('請選擇一個選項');
    }
}

function updateSelected(selectId, displayId, hiddenInputId) {
    const select = document.getElementById(selectId);
    const selectedValue = select.value;
    const displayDiv = document.getElementById(displayId);
    const hiddenInput = document.getElementById(hiddenInputId);

    if (selectedValue) {
        // 創建新的顯示項目
        const newItem = document.createElement('div');
        newItem.className = "selectedTag";

        // // 創建 i 元素並添加 class
        // const icon = document.createElement('i');
        // icon.className = "fa fa-times";

        // 將 i 元素添加到 div 中
        // newItem.appendChild(icon);
        newItem.textContent = "🗙 " + selectedValue;
        console.log()
        newItem.classList.add('selected-item');
        newItem.addEventListener('click', () => {
            // 點擊已選項目，移除它
            displayDiv.removeChild(newItem);
            removeFromHiddenInputs(selectedValue); // 同時更新隱藏的輸入
        });
        displayDiv.appendChild(newItem);

        // 更新隱藏的輸入欄位
        hiddenInput.value = hiddenInput.value ? hiddenInput.value + ',' + selectedValue : selectedValue;
    }

    // 清空選擇框以便再次選擇
    select.value = "";
}

function removeFromHiddenInputs(value) {
    const hiddenInputs = [
        document.getElementById('hiddenfeatures'),
        document.getElementById('hiddengenres'),
        document.getElementById('hiddentags'),
    ];

    hiddenInputs.forEach(input => {
        const currentValues = input.value.split(',').filter(item => item !== value);
        input.value = currentValues.join(',');
    });
}


function updateHiddenInputs() {
    const features = document.querySelectorAll('#selectedfeatures .selected-item');
    const genres = document.querySelectorAll('#selectedgenres .selected-item');
    const tags = document.querySelectorAll('#selectedtags .selected-item');

    document.getElementById('hiddenfeatures').value = Array.from(features).map(item => item.textContent).join(',');
    document.getElementById('hiddengenres').value = Array.from(genres).map(item => item.textContent).join(',');
    document.getElementById('hiddentags').value = Array.from(tags).map(item => item.textContent).join(',');

}



document.getElementById('gameForm').addEventListener('submit', function (event) {
    event.preventDefault(); // 防止默認提交，避免頁面刷新

    // 更新隱藏欄位
    updateHiddenInputs();

    // 收集表單資料
    const formData = new FormData(this);

    // 發送資料到伺服器
    fetch('/submit-game', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert(data.message); // 顯示成功消息
            // 顯示訊息在頁面上而不是 alert
            document.getElementById('responseMessage').textContent = data.message;
        })
});