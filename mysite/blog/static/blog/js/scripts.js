$(document).ready(function(){

    $('#post_like_btn').click(function(){
        like_post($(this).attr('value'))
    });

    function like_post(slug_post){
        var token=$("[name='csrfmiddlewaretoken']").attr('value')
        $.ajax({
            url:'/blog/like/',
            type:'post',
            data:{
                slug:slug_post,
                csrfmiddlewaretoken: token,
            },
            success:function(data){
                if (data.liked){
                    $('#post_like_btn').text('UnLike');
                    $('#post_like_btn').removeClass().addClass('btn btn-light fa fa-heart');
                }
                else{
                     $('#post_like_btn').text('Like')
                     $('#post_like_btn').removeClass().addClass('btn btn-light fa fa-heart-o');
                }
            $('#id_total_likes').text('Total likes: '+data.total_likes)
            }
        });
    }

    $('#comment_btn').click(function(){
        comments_post($(this).attr('value'))
    });

    function comments_post(slug_post){
        var token=$("[name='csrfmiddlewaretoken']").attr('value')
        var name=$('#name_comment').val()
        var body=$('#body_comment').val()
        if (name && body){
            $.ajax({
                url:'/blog/article/'+slug_post,
                type:'post',
                data:{
                    slug:slug_post,
                    name:$('#name_comment').val(),
                    body:$('#body_comment').val(),
                    csrfmiddlewaretoken: token,
                },
                success:function(data){
                    $('#comments').html(data);
                    name:$('#name_comment').val('');
                    body:$('#body_comment').val('');
                }
            });
        }
        else{
            alert("Не все поля заполнены для коммента записи");
        }
    }

});