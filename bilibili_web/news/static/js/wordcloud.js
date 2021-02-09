function wordcloudquery(mid) {
    $('#data').html('');
    $.ajax({
        url: '/cloud?mid=' + mid,
        type: "get",
        data: "",
        contentType: "application/json;charset=UTF-8",
        success: function (data) {
            let list = '';
            $.each(JSON.parse(data), function (i, d) {
                list += '<li><a href="' + d.url + '">' + d.title + '<span style="margin-left: 30px; font-size: xx-small; color: grey">播放量：' + (d.play_cnt/10000).toFixed(2) + '万</span></a></li>'
            });
            $('#data').append(list);
        },
        error: function (error) {
            console.error(error)
        }
    })
}