layui.use(['layer', 'form', 'element', 'jquery'], function() {
	var layer = layui.layer;
	var element = layui.element;
	var form = layui.form;
	var $ = layui.jquery;
	var hideBtn = $('#hideBtn');
	var mainLayout = $('#main-layout');
	var mainMask = $('.main-mask');
	//监听导航点击
	element.on('nav(leftNav)', function(elem) {
		// var navA = $(elem).find('a');
		var navA = elem;
		var id = navA.attr('data-id');
		var url = navA.attr('data-url');
		var text = navA.attr('data-text');
		if(!url){
			return;
		}
		var isActive = $('.main-layout-tab .layui-tab-title').find("li[lay-id=" + id + "]");
		if(isActive.length > 0) {
			//切换到选项卡
			element.tabChange('tab', id);
		} else {
			element.tabAdd('tab', {
				title: text,
				content: '<iframe src="' + url + '" name="iframe' + id + '" class="iframe" framborder="0" data-id="' + id + '" scrolling="auto" width="100%"  height="100%"></iframe>',
				id: id
			});
			element.tabChange('tab', id);
			
		}
		mainLayout.removeClass('hide-side');
	});
	//监听导航点击
	element.on('nav(rightNav)', function(elem) {
		var navA = elem;
		var filter = navA.attr('data-filter');
		var url = navA.attr('data-url');

		if(!url){
			return;
		}
		if(filter=="logout"){
			var r = document.cookie.match("\\b_xsrf=([^;]*)\\b");
    		_xsrf = r ? r[1] : undefined;
			$.ajax({
			  "type": "post",
			  "url": url,
			  "data":{"_xsrf":_xsrf},
			  "success": function(resp){
				if(resp.ok) {
					layer.msg("注销成功",{time:2000},function () {
						window.location.reload();
                    })
				}
			  }
			});
		}
	});
	//菜单隐藏显示
	hideBtn.on('click', function() {
		if(!mainLayout.hasClass('hide-side')) {
			mainLayout.addClass('hide-side');
			// “右向左身上按钮”隐藏
			hideBtn.find(".layui-icon-shrink-right").addClass("hidden");
			// “左向右身上按钮”展示
			hideBtn.find(".layui-icon-spread-left").removeClass("hidden");

		} else {
			mainLayout.removeClass('hide-side');
			// “右向左身上按钮”展示
			hideBtn.find(".layui-icon-shrink-right").removeClass("hidden");
			// “左向右身上按钮”隐藏
			hideBtn.find(".layui-icon-spread-left").addClass("hidden");
		}
	});
	//遮罩点击隐藏
	mainMask.on('click', function() {
		mainLayout.removeClass('hide-side');
	})

	//示范一个公告层
//	layer.open({
//		  type: 1
//		  ,title: false //不显示标题栏
//		  ,closeBtn: false
//		  ,area: '300px;'
//		  ,shade: 0.8
//		  ,id: 'LAY_layuipro' //设定一个id，防止重复弹出
//		  ,resize: false
//		  ,btn: ['火速围观', '残忍拒绝']
//		  ,btnAlign: 'c'
//		  ,moveType: 1 //拖拽模式，0或者1
//		  ,content: '<div style="padding: 50px; line-height: 22px; background-color: #393D49; color: #fff; font-weight: 300;">后台模版1.1版本今日更新：<br><br><br>数据列表页...<br><br>编辑删除弹出功能<br><br>失去焦点排序功能<br>数据列表页<br>数据列表页<br>数据列表页</div>'
//		  ,success: function(layero){
//		    var btn = layero.find('.layui-layer-btn');
//		    btn.find('.layui-layer-btn0').attr({
//		      href: 'http://www.layui.com/'
//		      ,target: '_blank'
//		    });
//		  }
//		});
});
