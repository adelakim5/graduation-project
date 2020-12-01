let form = document.querySelector("#reservation");
let peopleSize = document.querySelector("#peopleSize");
let limitPrice = +document.querySelector("#foodPrice").textContent;
const isCartExist = document.querySelector("#pastCart").textContent;
let calculatedTotalPrice = document.querySelector("#total_price");
peopleSize.addEventListener("change", (e) => {
  console.log(`e: ${e.target.value}`);
  calculatedTotalPrice.value = e.target.value * limitPrice;
});

const requestBtn = document.querySelector("#requestBtn");
requestBtn.addEventListener("click", () => {
  if (isCartExist === true) {
    alert("이미 요청한 내역이 있습니다");
  } else {
    const promptPhoneNumber = prompt("전화번호를 입력해주세요.\n※정확히 입력하여야 예약 알림 메시지를 받을 수 있습니다.※ \n (ex.010-1234-5678)");
    let phoneNumber = document.querySelector("#phoneNum");
    const regExp = /^(?:(010-?\d{4})|(01[1|6|7|8|9]-?\d{3,4}))-?\d{4}$/;
    if (regExp.test(promptPhoneNumber)) {
      phoneNumber.value = promptPhoneNumber;
      form.submit();
    } else {
      alert("유효하지 않은 번호입니다.");
      return;
    }
  }
});
