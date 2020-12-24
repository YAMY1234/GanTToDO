$(function(){

	// Cache some selectors

	var clock = $('#clock'),
		alarm = clock.find('.alarm'),
		ampm = clock.find('.ampm'),
		dialog = $('#alarm-dialog').parent(),
		alarm_set = $('#alarm-set'),
		alarm_clear = $('#alarm-clear'),
		time_is_up = $('#time-is-up').parent();

	// This will hold the number of seconds left
	// until the alarm should go off
    // 倒计时
	var alarm_counter = -1;

	// Map digits to their names (this will be an array)
	var digit_to_name = 'zero one two three four five six seven eight nine'.split(' ');

	// This object will hold the digit elements
    //此对象将保持数字元素
	var digits = {};

	// 显示数组
	var positions = [
		'h1', 'h2', ':', 'm1', 'm2', ':', 's1', 's2'
	];

	// 生成数字并添加到时钟里面
	// 

	var digit_holder = clock.find('.digits');

	$.each(positions, function(){

		if(this == ':'){
			digit_holder.append('<div class="dots">');
		}
		else{

			var pos = $('<div>');

			for(var i=1; i<8; i++){
				pos.append('<span class="d' + i + '">');
			}

			// Set the digits as key:value pairs in the digits object
			digits[this] = pos;

			// Add the digit elements to the page
			digit_holder.append(pos);
		}

	});

	// 周
	var weekday_names = '一 二 三 四 五 六 日'.split(' '),
		weekday_holder = clock.find('.weekdays');

	$.each(weekday_names, function(){
		weekday_holder.append('<span>' + this + '</span>');
	});

	var weekdays = clock.find('.weekdays span');


	//利用计时器更新时间

	(function update_time(){
        
        // 使用moment.js输出当前时间作为字符串
		// HH是12小时格式的时间，
		//分秒之前+0
		// 
		// d is for day of week and A is for AM/PM

		var now = moment().format("hhmmssdA");

		digits.h1.attr('class', digit_to_name[now[0]]);
		digits.h2.attr('class', digit_to_name[now[1]]);
		digits.m1.attr('class', digit_to_name[now[2]]);
		digits.m2.attr('class', digit_to_name[now[3]]);
		digits.s1.attr('class', digit_to_name[now[4]]);
		digits.s2.attr('class', digit_to_name[now[5]]);

		

		var dow = now[6];
		dow--;
		
		// Sunday!
		if(dow < 0){
			// Make it last
			dow = 6;
		}

		//加入事件
		weekdays.removeClass('active').eq(dow).addClass('active');

		// 设置am或pm
		ampm.text(now[7]+now[8]);


		// 设置报警

		if(alarm_counter > 0){
			
			// 记数递减
			alarm_counter--;

			// 点亮闹钟图标
			alarm.addClass('active');
		}
		else if(alarm_counter == 0){

			time_is_up.fadeIn();
            //播放报警音
			//
			// 

			try{
				$('#alarm-ring')[0].play();
			}
			catch(e){}
			
			alarm_counter--;
			alarm.removeClass('active');
		}
		else{
			// 清除警报
			alarm.removeClass('active');
		}

		//再次允许运行1s
		setTimeout(update_time, 1000);

	})();

	//切换主题

	$('#switch-theme').click(function(){
		clock.toggleClass('light dark');
	});


	// Handle setting and clearing alamrs

	$('.alarm-button').click(function(){
		
		// Show the dialog
		dialog.trigger('show');

	});

	dialog.find('.close').click(function(){
		dialog.trigger('hide')
	});

	dialog.click(function(e){

		// When the overlay is clicked, 
		// hide the dialog.

		if($(e.target).is('.overlay')){
			// This check is need to prevent
			// bubbled up events from hiding the dialog
			dialog.trigger('hide');
		}
	});


	alarm_set.click(function(){

		var valid = true, after = 0,
			to_seconds = [3600, 60, 1];

		dialog.find('input').each(function(i){

			// Using the validity property in HTML5-enabled browsers:

			if(this.validity && !this.validity.valid){

				// The input field contains something other than a digit,
				// or a number less than the min value

				valid = false;
				this.focus();

				return false;
			}

			after += to_seconds[i] * parseInt(parseInt(this.value));
		});

		if(!valid){
			alert('输入数字');
			return;
		}

		if(after < 1){
			alert('输入一个时间!');
			return;	
		}

		alarm_counter = after;
		dialog.trigger('hide');
	});

	alarm_clear.click(function(){
		alarm_counter = -1;

		dialog.trigger('hide');
	});

	// Custom events to keep the code clean
	dialog.on('hide',function(){
		dialog.fadeOut();
	}).on('show',function(){

		// Calculate how much time is left for the alarm to go off.

		var hours = 0, minutes = 0, seconds = 0, tmp = 0;

		if(alarm_counter > 0){
			
			// There is an alarm set, calculate the remaining time

			tmp = alarm_counter;
			hours = Math.floor(tmp/3600);
			tmp = tmp%3600;

			minutes = Math.floor(tmp/60);
			tmp = tmp%60;

			seconds = tmp;
		}

		// Update the input fields
		dialog.find('input').eq(0).val(hours).end().eq(1).val(minutes).end().eq(2).val(seconds);

		dialog.fadeIn();

	});

	time_is_up.click(function(){
		time_is_up.fadeOut();
	});

});