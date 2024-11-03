// test.js




document.addEventListener("DOMContentLoaded", init);


async function init() {


    // 태그 연결
    document.getElementById("a-test").addEventListener("click", async function(evt) {
        evt.preventDefault();
        const url = this.getAttribute("href");

        const resp = await fetch(url, {});
        if(resp.ok){ window.location.href = url; }
        else{ console.error(resp.status) }
    })
}





