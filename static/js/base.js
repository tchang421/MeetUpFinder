$(function () {
    $(document).scroll(function () {
        var $nav = $("#navbar nav");
        $nav.toggleClass("scrolled", $(this).scrollTop() > ($nav.height()/2));
    });
});
