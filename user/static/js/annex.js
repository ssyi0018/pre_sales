var delete_id;
var edit_id;
$(function () {
    bindBtnAddEvent();
    bindBtnSaveEvent();
    bindBtnDeleteEvent();
    bindBtnConfirmDeleteEvent();
    bindBtnEditEvent();
    listTable();
})

function bindBtnAddEvent() {
    $('#btnAdd').click(function () {
        edit_id = undefined;

        $('#formAdd')[0].reset();
        $('#myModalLabel').text('上传文件');

        $('#myModal').modal('show');
        initUpdateTime();
    });
}

function initUpdateTime() {
    $('#id_update_time').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '0',
        language: 'zh-CN',
        autoclose: true,
        // todayHighlight: true, // 今日高亮显示
        // minView: "month", // 最小视图为月份，如果为 day 的话还会让你选小时

    })
}

function bindBtnSaveEvent() {
    $('#btnSave').click(function () {
        // 清除错误信息
        $('.error-msg').empty();

        if (edit_id) {
            //编辑
            doEdit();
        } else {
            //添加
            doAdd();
        }


    })
}

function doAdd() {
    var form_data = new FormData($('#formAdd')[0]);
    $.ajax({
        url: '/sales/add/',
        type: 'post',
        data: form_data,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function (res) {
            if (res.status) {
                alert('提交成功');
                $('#formAdd')[0].reset();
                $('#myModal').modal('hide');
                location.reload();
            } else {
                $.each(res.error, function (name, errorList) {
                    $('#id_' + name).next().text(errorList[0]);
                });
            }
            // 新增判断逻辑开始
            if (res.filename_exists) {
                alert('已有重复的文件名，不允许上传');
            }
            // 新增判断逻辑结束
        }
    });
}

function doEdit() {
    var form_data = new FormData($('#formAdd')[0]);
    $.ajax({
        url: '/sales/edit/' + '?uid=' + edit_id,
        type: 'post',
        data: form_data,
        processData: false,
        contentType: false,
        dataType: 'JSON',
        success: function (res) {
            if (res.status) {
                alert('更新成功');
                // 清空表单
                $('#formAdd')[0].reset();
                // 关闭对话框
                $('#myModal').modal('hide');
                //页面刷新
                location.reload();
            } else {
                if (res.tips) {
                    alert(res.tips);
                } else {
                    $.each(res.error, function (name, errorList) {
                        $('#id_' + name).next().text(errorList[0]);
                    })
                }
            }
        }
    })
}

//点击删除按钮
function bindBtnDeleteEvent() {
    // 自定义class样式做ajax触发
    $('.btn-delete').click(function () {
        //alert('点击了删除');
        $('#deleteModal').modal('show');

        //获取当前行id给全局变量
        delete_id = $(this).attr('uid');
    })
}

function bindBtnConfirmDeleteEvent() {
    $('#btnConfirmDelete').click(function () {
        // 确认删除，把全局变量中的id发送到后台
        $.ajax({
            //url: '/order/' + delete_id + 'delete/',
            url: '/sales/delete/',
            type: 'GET',
            data: {
                uid: delete_id
            },
            dataType: 'JSON',
            success: function (res) {
                if (res.status) {
                    // 删除对话框隐藏
                    //$('#deleteModal').modal('hide');
                    // 当前删除的数据页面删除掉(js)
                    //$("tr[uid='"+ delete_id + "']").remove();
                    // 要删除的全局变量置空
                    //delete_id = 0;

                    // 最简单的思路:
                    location.reload();
                } else {
                    alert(res.error);
                }
            }
        })
    });
}

// 编辑对话框公用新建框
function bindBtnEditEvent() {
    $('.btn-edit').click(function () {
        // 清空对话框中数据
        $('#formAdd')[0].reset();
        var currentId = $(this).attr('uid');
        edit_id = currentId;
        //发送ajax去后台发送当前行数据
        $.ajax({
            url: '/sales/detail/',
            type: 'GET',
            data: {
                uid: currentId
            },
            dataType: 'JSON',
            success: function (res) {
                if (res.status) {
                    // 数据赋值到对话框中
                    $.each(res.data, function (name, value) {
                        $('#id_' + name).val(value);
                    })
                    // 修改对话框标题
                    $('#myModalLabel').text('更新文件');
                    $('#myModal').modal('show');
                } else {
                    alert(res.error);
                }
            }
        })
        initUpdateTime();
        //对话框中默认展现
    })
}

//左边树点击
function clickMe(self) {
    // 寻找标签
    var hasHide = $(self).next().hasClass('hide')
    if (hasHide) {
        $(self).next().removeClass('hide');
    } else {
        $(self).next().addClass('hide');
    }
    $(self).parent().siblings().find('.content').addClass('hide');
}

// 点击左边右边页面刷新
function listTable () {
    $('.content-link').on('click', function (event) {
        event.preventDefault(); // 阻止链接默认跳转行为
        var href = $(this).attr('href'); // 获取链接地址
        $.get(href, function (data) { // 发送 GET 请求，获取服务器返回的数据
            $('table').html(data); // 将服务器返回的数据重新渲染页面中的table标签
            bindBtnEditEvent();
        });
    });
};