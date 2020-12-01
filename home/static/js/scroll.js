var count = 0;
//스크롤 바닥 감지
let food = document.querySelector(".food");
window.onscroll = function (e) {
  //추가되는 임시 콘텐츠
  //window height + window scrollY 값이 document height보다 클 경우,
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    //실행할 로직 (콘텐츠 추가)
    count++;
    let addContent = `<div class="row my-5 align-items-center food">
        <div class="col-lg-7">
          {% if food.image %}
          <a href="{% url 'detail' food.id %}">
            <img class="img-fluid rounded mb-4 mb-lg-0" src="{{ food.image.url }}" alt="photo">
          </a>
          {% endif %}
        </div>
        <div class="col-lg-5">
          <h2 class="font-weight-bold">{{ food.title }}</h2>
          <p>{{ food.description }}<br>(후기: {{food.comments.count}}개)</p>
          <p>예약금액: {{ food.price }}원</p>
          <a href="{% url 'detail' food.id  %}" class="btn btn-to-detail">더보기</a>
        </div>
      </div>`;
    //article에 추가되는 콘텐츠를 append
    food.append(addContent);
  }
};
