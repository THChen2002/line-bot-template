// 初始化LIFF
function initializeLiff(liffId) {
    liff.init({ liffId }).then(() => {
        if (!liff.isLoggedIn()) {
            liff.login({ redirectUri: window.location.href });
        } else {
            // 獲取使用者資訊
            liff.getProfile().then(profile => {
                // 發送請求到後端驗證 admin 身份
                $.ajax({
                    url: '/admin/auth',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ userId: profile.userId }),
                    success: function(res) {
                        // 驗證通過，顯示主要內容，隱藏載入畫面
                        $('#liffLoading').addClass('d-none');
                        $('#mainContent').removeClass('d-none');
                    },
                    error: function(xhr) {
                        // 驗證失敗，導向 forbidden 頁面
                        window.location.href = "/forbidden";
                        liff.closeWindow();
                    }
                });
            }).catch(err => {
                console.error('取得使用者資訊失敗', err);
            });
        }
    }).catch(err => {
        console.error('LIFF 初始化失敗', err);
    });
}

$(document).ready(function() {
    initializeLiff(liffId);
});