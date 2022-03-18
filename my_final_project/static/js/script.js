/*----ブラウザ上部にヘッダーを固定------------*/

$(function(){
    // 変数navPosに、nav要素の初期位置を代入
    var navPos = $("nav").offset().top;
  
    // ブラウザをスクロール
    $(window).scroll(function(){
      // スクロール量とnav要素の初期位置を比較
      if($(window).scrollTop() > navPos){
        // 条件を満たした場合：nav要素をブラウザ上部に固定
        $("nav").css("position", "fixed");
      }else{
        // 満たさない場合：nav要素を通常の配置にする
        $("nav").css("position", "static");
      }
    });
  });
  
/*----//ブラウザ上部にヘッダーを固定------------*/



$(function () {
    //tab1以外を非表示にする
    $('#contents div[id != "tab1"]').hide();

    //タブをクリック
    $("a").click(function () {
        //クリック時の処理
        $("#contents div").hide();
        $($(this).attr("href")).show();

        //現在のcurrentクラスを排除
        $(".current").removeClass("current");

        //選択されたタブ（自分自身）にcurrentクラスを追加
        $(this).addClass("current");
        return false;
    });
});


 /*-----タイトルと説明がエンターを押すと繋がる---*/
 (function(){
    $('#title_area').on("keydown", function(e) {
      if( e.keyCode == 13 || e.keyCode == 40) {
        $("#comment_area").select();
        return false;
      }
    });
    $('#comment_area').on("keydown", function(e) {
      if( e.keyCode == 38 && this.selectionStart == 0) {
        $("#title_area").select();
        return false;
      }
    });
  })();

/*---画像を取得してリサイズする--*/
  const fileup = (e) => {
const img = document.getElementById('img');
const reader = new FileReader();
const imgReader = new Image();
const imgWidth = 680;
reader.onloadend = () => {
  imgReader.onload = () => {
    const imgType = imgReader.src.substring(5, imgReader.src.indexOf(';'));
    const imgHeight = imgReader.height * (imgWidth / imgReader.width);
    const canvas = document.createElement('canvas');
    canvas.width = imgWidth;
    canvas.height = imgHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(imgReader,0,0,imgWidth,imgHeight);
    img.src = canvas.toDataURL(imgType);
  }
  imgReader.src = reader.result;
}
reader.readAsDataURL(e.files[0]);
}