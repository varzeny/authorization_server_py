// access.js

// 엑세스 토큰 갱신
reqAccessToken();
setInterval(reqAccessToken, 1200000);

async function reqAccessToken() {
    const resp = await fetch("/oauth/token/access", {
        method:"POST",
        headers:{'Content-Type': 'application/json'},
    });

    if(resp.ok){
        console.log("access_token 발급 성공");
        return true;
    }
    else{
        console.log("access_token 발급 실패");
        return false;
    }
}