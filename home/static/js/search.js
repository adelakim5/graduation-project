let search = document.querySelector("#searchBar");
search.addEventListener("keydown", (e) => {
  if (e.keyCode === 13) {
    if (search.value === "") {
      alert("검색어를 입력해주세요.");
    } else {
      location.href = `/search/?searchkeyword=${search.value}`;
    }
  }
});
