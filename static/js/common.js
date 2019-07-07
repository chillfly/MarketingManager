layui.config({
    base: '/static/js/module/'
}).extend({
    dialog: 'dialog',
});

layui.use(['form', 'jquery', 'laydate', 'layer', 'laypage', 'dialog', 'element', 'dialog'], function () {
    var form = layui.form,
        layer = layui.layer,
        $ = layui.jquery,
        dialog = layui.dialog;

    var laydate = layui.laydate
    laydate.render({elem: '#birthday'});

    //获取当前iframe的name值
    var iframeObj = $(window.frameElement).attr('name');


    //全选
    form.on('checkbox(allChoose)', function (data) {
        var child = $(data.elem).parents('table').find('tbody input[type="checkbox"]');
        child.each(function (index, item) {
            item.checked = data.elem.checked;
        });
        form.render('checkbox');
    });
    //渲染表单
    form.render();

    form.on('switch', function (data) {
        if (data.elem.checked) {
            //开启
            data.elem.value = 1
        } else {
            //关闭
            data.elem.value = 0
        }
    });

    // 表单元素验证
    form.verify({
        //只能是整数
        isdigit: [
            /^\d+$/
            , '必须为数字'
        ],
        weibourl: [
            /^https:\/\/weibo\.com\S*/
            , '微博url不匹配'
        ],
        birthday: [
            /^\d{4}-\d{2}-\d{2}$/
            , '生日格式必须满足“xxxx-xx-xx”的格式'
        ],
    });

    //监听提交
    form.on('submit(go-submit)', function (data) {
        var loading_index = layerLoad(layer)
        $.ajax({
            "type": data.form.method,
            "url": data.form.action,
            "data": data.field,
            "success": function (resp) {
                layer.close(loading_index)
                var msg = "";
                if (resp.ok) {
                    msg = "成功 " + resp.data;
                } else {
                    msg = "失败 " + resp.reason;
                }
                // 默认执行反馈
                layer.alert(msg, function () {
                    try {
                        // 默认是弹出框做的表单，所以提交成功后，应该刷新其上层页面
                        parent.refresh();
                    } catch (e) {
                        // 报异常，说明找不到上层页面，即当前页不是弹出框表单页，那么刷新当前页面即可
                        self.refresh()
                    }
                });
            }
        });
        return false;
    });

    /***** 列表顶部操作 start ************************************************************************/
    //顶部添加
    $('.addBtn').click(function () {
        self.iframe_init($(this), iframeObj);
        return false;

    }).mouseenter(function () {

        dialog.tips('添加', '.addBtn');

    })
    //顶部排序
    $('.listOrderBtn').click(function () {
        var url = $(this).attr('data-url');
        dialog.confirm({
            message: '您确定要进行排序吗？',
            success: function () {
                layer.msg('确定了')
            },
            cancel: function () {
                layer.msg('取消了')
            }
        })
        return false;

    }).mouseenter(function () {

        dialog.tips('批量排序', '.listOrderBtn');

    })
    //顶部批量删除
    $('.delBtn').click(function () {
        var url = $(this).attr('data-url');
        dialog.confirm({
            message: '您确定要删除选中项',
            success: function () {
                layer.msg('删除了')
            },
            cancel: function () {
                layer.msg('取消了')
            }
        })
        return false;

    }).mouseenter(function () {

        dialog.tips('批量删除', '.delBtn');

    });
    /***** 列表顶部操作 end ************************************************************************/

    /***** 列表内部操作 start ************************************************************************/
    //列表添加
    $('#table-list').on('click', '.add-btn', function () {
        self.iframe_init($(this), iframeObj);
        return false;
    })
    //列表删除
    $('#table-list').on('click', '.del-btn', function () {
        var url = $(this).attr('data-url');
        var id = $(this).attr('data-id');
        var method = $(this).attr('data-method');
        dialog.confirm({
            message: '您确定要进行删除吗？',
            success: function () {
                $.ajax({
                    type: method || "get",
                    url: url,
                    data: {"id": id},
                    success: function (res) {
                        if (res.ok) {
                            layer.msg("删除成功", function () {
                                self.refresh();
                            })
                        } else {
                            layer.msg("删除失败")
                        }
                    }
                });
            },
        })
        return false;
    })
    //列表跳转
    $('#table-list,.tool-btn').on('click', '.go-btn', function () {
        var url = $(this).attr('data-url');
        var id = $(this).attr('data-id');
        window.location.href = url + "?id=" + id;
        return false;
    })
    //编辑栏目
    $('#table-list').on('click', '.edit-btn', function () {
        self.iframe_init($(this), iframeObj);
        return false;
    });

    $('#table-list').on('click', '.login-btn', function () {
        var that = $(this)
        var id = $(this).data("id")
        var login_url = $(this).data("url")
        var loading_index = layerLoad(layer)
        $.ajax({
            "type": "get",
            "url": "/weibo/account/loadloginpage/",
            "data": {"id": id},
            "success": function (resp) {
                if (resp.ok) {
                    // 已经登录了
                    layer.close(loading_index);  // 关闭加载层
                    layer.alert("已经登录了");
                } else {
                    // 未登录
                    // 判断是否需要验证码
                    if (resp.data.needverify) {
                        // 需要验证码
                        // 加载验证码输入窗口
                        layer.close(loading_index);  // 关闭加载层
                        self.iframe_init(that, iframeObj);
                        return false;
                    } else {
                        // 不需要验证码
                        // 执行登录
                        ajaxFormSubmit(login_url, {"id": id}, function (resp) {
                            layer.close(loading_index);  // 关闭加载层
                            if (resp.ok) {
                                // 登录成功
                                msg = "登录成功"
                            } else {
                                // 登录失败
                                msg = "登录失败!\n" + resp.reason
                            }
                            // 默认执行反馈
                            layer.alert(msg, function () {
                                self.refresh()
                            });
                        });
                    }
                }
            }
        });
    });
    /***** 列表内部操作 end **************************************************************************/
});

/**
 * 控制iframe窗口的刷新操作
 */
var iframeObjName;

/**
 * 展示iframe之前的初始化（数据准备）
 * */
function iframe_init(that, iframeObj) {
    var id = that.attr('data-id') || undefined;
    var url = that.attr('data-url');
    if (id != undefined) {
        url = url + "?id=" + id
    }
    var title = that.data("title") || "菜单编辑";
    var width = that.data("width") || "700px";
    var height = that.data("height") || "620px";
    var closesave = that.data("closesave") || "0";
    //将iframeObj传递给父级窗口
    self.page(title, url, iframeObj, w = width, h = height, cs = closesave);
}

//父级弹出页面
function page(title, url, obj, w, h, cs) {
    if (title == null || title == '') {
        title = false;
    }
    ;
    if (url == null || url == '') {
        url = "/404/";
    }
    ;
    if (w == null || w == '') {
        w = '700px';
    }
    ;
    if (h == null || h == '') {
        h = '350px';
    }
    ;
    iframeObjName = obj;

    var open_obj = {
        type: 2,
        title: title,
        fixed: false, //不固定
        content: url,
    }
    if (cs == "1") {
        open_obj.cancel = function () {
            layer.confirm("是否保存？", {icon: 3, title: "提示"}, function () {
                //执行保存功能
                console.log("哈哈")
                $.ajax({
                    type: method || "post",
                    url: url,
                    data: {"id": id},
                    success: function (res) {
                        if (res.ok) {
                            layer.msg("删除成功", function () {
                                self.refresh();
                            })
                        } else {
                            layer.msg("删除失败")
                        }
                    }
                })
            })
        }
    }
    //如果手机端，全屏显示
    if (window.innerWidth <= 768) {
        open_obj.area = [320, h]
        var index = layer.open(open_obj);
        layer.full(index);
    } else {
        open_obj.area = [w, h]
        open_obj.maxmin = true
        var index = layer.open(open_obj);
    }
}

/**
 * 刷新子页,关闭弹窗
 */
function refresh() {
    //根据传递的name值，获取子iframe窗口，执行刷新
    if (window.frames[iframeObjName]) {
        window.frames[iframeObjName].location.reload();

    } else {
        window.location.reload();
    }

    layer.closeAll();
}

function table_render(data_url, cols, table_id, callback, toolbar) {
    var tableIns = table.render({
        elem: table_id || '#table',
        url: data_url
        , limit: 30
        , even: true
        , page: true
        , cols: [cols]
        , done: function (res, curr, count) {
            if (callback) {
                callback(res, curr, count);
            }
        }
    });
    return tableIns
}

function tableInit(data_url, cols, table_id, callback) {
    // 添加转义
    // for (var i = 0; i < cols.length; i++) {
    //     if (!cols[i].templet) {
    //         cols[i].templet = "<div>{{= d." + cols[i].field + " }}</div>"
    //     }
    // }

    var tableIns = table.render({
        elem: table_id || '#table',
        url: data_url
        , limit: 30
        , even: true
        , page: true
        , cols: [cols]
        , done: function (res, curr, count) {
            if (callback) {
                callback(res, curr, count);
            }
        }
    });

    form.on("submit(go-search)", function (data) {
        var $frm = $(data.form);
        var frm_data = $frm.serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        if ($(this).attr("data-toggle") === "clear") {
            $frm.trigger("reset");
            frm_data = {}
        }
        if ($(this).attr("data-toggle") === "export") {
            // 导出
            var url = data_url + "&export=1&" + $frm.serialize();
            window.open(url);
            return false;
        }
        tableIns.config.where = frm_data;
        tableIns.config.page.curr = 1;
        tableIns.reload({
            where: frm_data,
            page: {
                curr: 1
            }
        });
        return false;
    });
    return tableIns;
}


function ajaxFormSubmit(url, data, success_callback, err_callback, type) {
    // 防止跨站请求伪造
    var r = document.cookie.match("\\b_xsrf=([^;]*)\\b");
    data._xsrf = r ? r[1] : undefined;

    $.ajax({
        "type": type || "post",
        "url": url,
        "data": data,
        "success": function (resp) {
            if (success_callback) {
                success_callback(resp);
            }
        },
        "error": function (resp) {
            if (err_callback) {
                err_callback(resp);
            }
        }
    });
}

function layerLoad(layer) {
    var index = layer.load(1, {shade: 0.5,});
    return index
}