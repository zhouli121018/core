/*
 *	JavaScript
 */


/* 业务相关函数
 **********************************************************/



/* 基础函数
 **********************************************************/

//剔除字符串空白: http://www.yaosansi.com
String.prototype.trim  = function() {return this.replace(/(^\s*)|(\s*$)/g, "");};
String.prototype.ltrim = function() {return this.replace(/(^\s*)/g, "");};
String.prototype.rtrim = function() {return this.replace(/(\s*$)/g, "");};

function go(url) {window.location.href = url;}

//检测邮件地址类型
function checkMailAddrType(address) {
	if (address[0] == '@') return 'domain';
	return 'email';
}

//检测邮件地址
function checkMailAddr(addr) {
	var pattern = new RegExp(/^\w[-\w.+]*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/);
	return pattern.test(addr);
}

//检测邮件地址名称
function checkMailName(name) {
	var pattern = new RegExp(/^\w[-\w.+]*$/);
	return pattern.test(name);
}

//检测域名
function checkDomain(domain) {
	var pattern = new RegExp(/^\w[-\w.+]*([-.]\w+)*\.\w+([-.]\w+)*$/);
	return pattern.test(domain);
}

//强密码检测
/*function checkStrongCipher(password, notice) {
	if(notice == undefined) notice = true;
	if(password.length < 8) {
		if(notice) {
			alert("密码长度最少为8位！");
			return false;
		}
		return new Array(false, "密码长度最少为8位！");
	}
	if(password.search(/([a-z]+)/) == -1 || password.search(/([0-9]+)/) == -1) {
		if(notice) {
			alert("密码中必须包括字母和数字！");
			return false;
		}
		return new Array(false, "密码中必须包括字母和数字！");
	}
	return true;
}*/

function checkStrongCipher(string, notice) {
	if(notice == undefined) notice = true;
	var check1 = /[a-z]/;
	var check6 = /[A-Z]/;
	var check2 = /[0-9]+/i;
	var check3 = new RegExp('^[0-9a-zA-Z~!@#$%^&*()_+\\[\\];\\-\\=\\\'\\\\,./<>?:\\"\\|\\{\\}`]+$', 'i');//符号，数字，字母
	var check4 = new RegExp('.*(.)\\1{3,}.*', 'g');
	
	
	if(string.length < 8) {
		if(notice) {
			alert("密码长度必须大于8位！");
			return false;
		}
		return new Array(false, "密码长度必须大于8位！");
	}
	if(string.length > 20) {
		if(notice) {
			alert("密码长度必须小于20位！");
			return false;
		}
		return new Array(false, "密码长度必须小于20位！");
	}
	if(!check1.test(string) || !check6.test(string) || !check2.test(string)) {
		if(notice) {
			alert("密码中必须包含大写字母和小写字母以及数字！");
			return false;
		}
		return new Array(false, "密码中必须包含大写字母和小写字母以及数字！");
	}
	if(!check3.test(string)){
		if(notice) {
			alert("密码中不允许输入全角符号！");
			return false;
		}
		return new Array(false, "密码中不允许输入全角符号！");
	}
	if(check4.test(string)) {
		if(notice) {
			alert("密码中连续重复的数或字母长度不能在3位（含3位）以上");
			return false;
		}
		return new Array(false, "密码中连续重复的数或字母长度不能在3位（含3位）以上");
	}

	var check5 = new RegExp('\\d+|[a-zA-Z]+', 'g');
	var match = string.match(check5);
	
	var index;
	var str_arr = new Array();
	for( index in match ) {
		if(match[index] && match[index].length>=3) {
			str_arr.push(match[index]);
		}
	}

	var res = true;
	index = 0;
	for(index in str_arr) {
		var v = str_arr[index];
		var v_len = v.length;
		
		var delta_arr = new Array();
		var lastdelta = '';
		for(var i=0; i<v_len; i++) {
			if(i == 0 || !v[i]) {
				continue;
			}
			var delta = v[i].charCodeAt() - v[i-1].charCodeAt();
			if((delta == 1 || delta == -1 || delta == 0) && (delta == lastdelta || delta_arr.length == 0)) {
				delta_arr.push(v[i]);
				lastdelta = delta;
			}
			else
				delta_arr.length = 0;
		}


		if(delta_arr.length >= 2) {
			res = false;
			break;
		}

	}

	if(!res) {
		if(notice) {
			alert("密码中递增、递减的数或字母长度不能在3位（含3位）以上");
			return false;
		}
		return new Array(false, "密码中递增、递减的数或字母长度不能在3位（含3位）以上");
	}


	return true;
}

//数字检测
function checkNumber(number, isint) {
	if(isint == undefined) isint = false;
	if(isint) {
		var re = /^\d+$/;
	} else {
		var re = /^\d+(\.(\d)+)?$/;
	}
	return re.test(number);
}

//检测字符串格式
function checkFormat(string, type) {
	var expression = null;
	if(type == 'domain') {
		expression = /^\w+([-.]*\w+)*\.\w+([-.]\w+)*$/;
	} else if(type == 'email') {
		expression = /^\w+([-+.]*\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
	} else if(type == 'phone') {
		expression = /(^([0][1-9]{2,3}[-])?\d{3,8}(-\d{1,6})?$)|(^\([0][1-9]{2,3}\)\d{3,8}(\(\d{1,6}\))?$)|(^\d{3,8}$)/;
	} else if(type == 'number') {
		expression = /^\d+(\.(\d)+)?$/;
	} else if(type == 'username') {
		expression = /^\w+([-+.]*\w+)*$/;
	} else if(type == 'ip') {
		var re = /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
		if(!re.test(string)) return false;
		return !(RegExp.$1 > 255 || RegExp.$2 > 255 || RegExp.$3 > 255 || RegExp.$4 > 255);
	}
	var pattern = new RegExp(expression);
	return pattern.test(string);

}

//选中/取消表单中的单选框
function setCheckbox(obj, form_id, prefix) {
	var form = document.getElementById(form_id);
	for(var i = 0; i < form.elements.length; i++) {
		var e = form.elements[i];
		if(e.name && (!prefix || (prefix && e.name.match(prefix)))) {e.checked = obj.checked;}
	}
}

//取得单个复选框的值
function getCheckboxValue(obj) {
	for(var i=0; i<obj.length; i++) {
		if(obj[i].checked) return obj[i].value;
	}
	return true;
}

//取得多个复选框的值
function getCheckboxValueByName(form_id, name) {
	var form = document.getElementById(form_id);
	var vals = [];
	for(var i = 0; i < form.elements.length; i++) {
		var e = form.elements[i];
		if(e.name && e.name == name && e.checked) vals.push(e.value);
	}
	return vals;
}

