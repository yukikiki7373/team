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




// スクロールした際の動きを関数でまとめる
function setFadeElement(){
    var windowH = $(window).height();//ウィンドウの高さを取得
    var scroll = $(window).scrollTop();//スクロール値を取得

    //出現範囲の指定
    //要素までの高さを四捨五入した値で取得
    var contentsTop = Math.round($('#top-dreams').offset().top);
    var contentsH = $('#top-dreams').outerHeight(true);//要素の高さを取得

    //出現範囲内に入ったかどうかをチェック
    if(scroll+window >= contentsTop && scroll + windowH <= contentsTop+contentsH){
        $("#page-top").addClass("UpMove");//入っていたらUpMoveクラスを追加
        $("#page-top").removeClass("DownMove");//DownMoveを削除
        $(".hide-btn").removeClass("hide-btn");//hide-btnを削除
    }else{
        //サイト表示時にDownMoveクラスを一瞬付与させないためのクラス付け
        //hide-btnがなければ下記の動作を行う
        if(!$(".hide-btn").length){
            $("#page-top").addClass("DownMove");
            $("#page-top").removeClass("UpMove");
        }
    }
}

//画面をスクロールしたら動かしたい場合の記述
$(window).scroll(function(){
    setFadeElement();/*スクロールした際の動きの関数を呼ぶ*/
})


//ページが読み込まれたらすぐに動かしたい場合の記述
$(window).on('load', function(){
   setFadeElement();
});

//#page-topをクリックした際の設定
$('#page-top').click(function(){
    $('body,html').animate({
      scrollTop: 0//ページトップまでスクロール
    },500);//ページスクロールトップまでの速さ。数が大きくなるほど遅くなる
    return false;//リンク自体の無効化
});




//アコーディオンをクリックした時の動作
$('.title').on('click', function () {//タイトル要素をクリックしたら
	$('.box').slideUp(500);//クラス名.boxがついたすべてのアコーディオンを閉じる

	var findElm = $(this).next(".box");//タイトル直後のアコーディオンを行うエリアを取得

	if ($(this).hasClass('close')) {//タイトル要素にクラス名closeがあれば
		$(this).removeClass('close');//クラス名を除去    
	} else {//それ以外は
		$('.close').removeClass('close'); //クラス名closeを全て除去した後
		$(this).addClass('close');//クリックしたタイトルにクラス名closeを付与し
		$(findElm).slideDown(500);//アコーディオンを開く
	}
});