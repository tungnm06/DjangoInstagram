/**/
;(function($, window) {
	// 核心构造函数- 轮播
    var HmSlider = function(option) {
    	this._init(option);
    };
    
    // 核心原型- 存储轮播用到的事件和方法
    HmSlider.prototype = {
    	constructor: HmSlider,
    	// 初始化
    	_init: function(option) {
    		this.containerID = option.id;
    		this.showTime = option.showTime;
    		this.isAuto = option.isAuto;
    		this.data = option.data;
    		this.length = this.data.length;
    		this.step = option.step;
    		this.timerId = 0;

    		// 初始化 DOM 元素
    		var $container = $("#" + this.containerID);
		    // 设置html内容
		    $container.html( this.parseData2HTML() );
    		this.$slider = $container.find(".slider");
    		this.$panel = $container.find(".slider-panel");
		    this.$prev = $container.find(".slider-prev");
		    this.$next = $container.find(".slider-next");
		    this.$navItem = $container.find(".slider-item");
		    this.$sliderPage = $container.find(".slider-page");
		    // 初始化播索引号
		    this.setIndex(0, this.length);
		    // 获取索引号
    		this.index = this.$slider.data("index");
    		// 初始化默认样式
		    this.$panel.fadeTo(0, 0).eq(0).fadeTo(0, 1);
		    // 初始化所有事件
		    this.bindEvent();
		    // 隐藏左右箭头
		    this.$sliderPage.hide();
    	},
    	// 实现轮播效果
	    slide: function(index) {
	    	// 播放下一张
	        this.$panel
	        	.eq(index).fadeTo(this.showTime, 1).css("z-index", 1)
	        	.siblings().fadeTo(this.showTime, 0).css("z-index", 0);
	        // 改变 index 的值，控制播放的索引
	        this.setIndex(index, this.length);
	        // 修改 数字导航 样式
	        this.$navItem.eq(index).addClass("slider-selected")
	            .siblings().removeClass("slider-selected")
	    },
	    // 控制当前轮播图的索引号
	    setIndex: function(index, length) {
	    	// 设置索引号
	        if(index > length - 1) {
	            this.index = 0;
	        } else if(index < 0) {
	            this.index = length - 1;
	        } else {
	            this.index = index;
	        }

	        this.$slider.data("index", this.index);
	    },
	    // 绑定事件
	    bindEvent: function() {
	    	// 保存 this 
	    	var self = this;
	    	// 向左滑动
	    	self.$prev.on("click", function() {
	            self.index -= 1;
	            self.setIndex(self.index, self.length);
	            self.slide(self.index);
	        });
	    	// 向右滑动
	        self.$next.on("click", function() {
	            self.index += 1;
	            self.setIndex(self.index, self.length);
	            self.slide(self.index);
	        });
	        // 数字导航
	        self.$navItem.on("click", function() {
	            var index = parseInt($(this).html()) - 1;
	            self.setIndex(self.index, self.length);
	            self.slide(index);
	        });
	        // 取消定时器
	        self.$slider.on("mouseenter", function() {
	        	self.$sliderPage.show();
	        	clearInterval(self.timerId);
	        });
	        // 开启定时器
	        self.$slider.on("mouseleave", function() {
	        	self.$sliderPage.hide();
	        	self.isAuto && self.autoPlay();
	        });

	        // 自动播放
	        this.isAuto && this.autoPlay();
	    },
	    parseData2HTML: function() {
	    	// 将JSON数据转化为 html 结构
	        var sliderMainList = [],
	            sliderNavList = [],
	            resultsList = [];

	        sliderMainList.push('<ul class="slider-main">');
	        this.data.forEach(function(value) {
	            sliderMainList.push('<li class="slider-panel">');
	            sliderMainList.push('<a href="' + value.href + '">');
	            sliderMainList.push('<img src="' + value.src + '" title="' +value.title+ '"/>');
	            sliderMainList.push("</a>");
	            sliderMainList.push("</li>");
	        });
	        sliderMainList.push('</ul>');

	        sliderNavList.push('<ul class="slider-nav">');
	        this.data.forEach(function(value, i) {
	            var index = i + 1;
	            if(i >= 1) {
	                sliderNavList.push('<li class="slider-item">'+ index +'</li>');
	            } else {
	                sliderNavList.push('<li class="slider-item slider-selected">'+ index +'</li>');
	            }
	        });
	        sliderNavList.push('</ul>');
	        
	        resultsList.push('<div class="slider" data-index="0">');
	        resultsList.push(sliderMainList.join(""));
	        resultsList.push('<div class="slider-extra">');
	        resultsList.push(sliderNavList.join(""));

	        resultsList.push('<div class="slider-page">');
	        resultsList.push('<a href="javascript:void(0)" class="slider-prev">&lt;</a>');
	        resultsList.push('<a href="javascript:void(0)" class="slider-next">&gt;</a>');
	        resultsList.push('</div>');
	        resultsList.push('</div>');

	        return resultsList.join("");
	    },
	    autoPlay: function() {
	    	var self = this;
    		var autoPlay = function() {
    			self.index += 1;
    			self.setIndex(self.index, self.length);
    			self.slide(self.index);
    		};

    		self.timerId = setInterval(autoPlay, self.step);
	    }
    };

    // 写jQuery 插件的格式
    // $.extend($.fn, {});
	$.fn.hmSilder = function(option) {
		// 设置默认参数
		var defaults = {
			showTime: 1000,		// 两个轮播图之间的转化时间
			step: 2000,			// 每一个轮播图停留多少时间
			id: this[0].id,	    // 指定轮播图的展示位置
			data: [],			// 轮播图的数据源
			isAuto: false	    // 是否自动播放
		};

		// 初始化参数
		var settings = $.extend({}, defaults, option);

		// 调用轮播图模块
		new HmSlider(settings);

		// 实现链式编程
		return this;
	};
})(jQuery, window);