let _lastTimestamp = 0; //上传时间增量
let _lastLoaded = 0;    //上传进度增量
var is_onload = 0;
// 上传配置项
let uploadOption = {
    action:"https://www.duwentao.cf:21286/xxtj/file/", //上传接口
    filter:"",                          //文件类型过滤器
    maxsize:1024,                       //文件上传大小限制，单位：M
    params:null,                        //请求参数
    startCallback:onload_start,         //开始上传的回调函数
    progressCallback:onload_progress,   //上传进度回调函数
    successCallback:onload,               //上传成功回调函数
    errorCallback:onload_error                  //上传错误的回调函数
}

//配置方法
//let config = (action, params, filter, maxsize, startcb)=>{
//    if(action!=null && action!=""){
//        uploadOption.action = action;
//    }
//    if(filter!=null){
//        uploadOption.filter = filter;
//    }
//    if(maxsize!=null && !isNaN(maxsize)){
//        uploadOption.maxsize = maxsize;
//    }
//    if(params!=null){
//        uploadOption.params = params;
//    }
//    uploadOption.startCallback = startcb;
//}


function set_params(action, params){
    uploadOption.action = action;
	uploadOption.params = params;
}

//设置配置对象，建议使用
let setOption = (opt)=>{
    if(opt!=undefined && opt!=null){
        uploadOption.action = opt.action || "http://localhost/uplad.do";
        uploadOption.filter = opt.filter || "";
        uploadOption.maxsize = opt.maxsize || 50;
        uploadOption.params = opt.params || null;
        uploadOption.startCallback = opt.startCallback || null;
        uploadOption.progressCallback = opt.progressCallback || null;
        uploadOption.successCallback = opt.successCallback || null;
        uploadOption.errorCallback = opt.errorCallback || null;
    }
}

//上传方法
let upload = (resolve, reject)=>{
    if (is_weixin())
    {
        var winHeight = $(window).height();
        $(".weixin-tip").css("height",winHeight);
        $(".weixin-tip").show();
        return;
    }
    let elem = document.getElementById("progress");
	let progress_num = document.getElementById("progress_num");
	progress_num.innerHTML = '';
    elem.style.width = 0 + "%";
    let input = document.getElementById("file");
		var form = new FormData();
		let length = input.files['length'];
		let sizeM = 0;
		for(let i=0; i<length; i++){
			let file = input.files[i];
			let tmparr = file.name.split(".");
			if(tmparr.length == 1) {
                file.name = file.name.replace('%3A','') + ".jpg";
            }
			else {
                let fileType =  tmparr[tmparr.length-1].toLowerCase();
                if(uploadOption.filter!=null && uploadOption.filter!=""){
                    let filterArr = uploadOption.filter.split(",");
                    let notFilter = true;
                    for(let i=0; i<filterArr.length; i++){
                        if(fileType == filterArr[i].toLowerCase()){
                            notFilter = false;
                        }
                    }
                    alert(1);
                    if(notFilter){
                        //文件类型不符合要求
                        if(uploadOption.errorCallback!=undefined && uploadOption.errorCallback!=null){
                            uploadOption.errorCallback("文件类型不符合要求");
                        }
                        else{
                            alert("文件类型不符合要求");
                        }
                        //reject("文件类型不符合要求");
                        return;
                    }
                }
            }
			sizeM = file.size/1024/1024 + sizeM;
			form.append("file"+i, file);
			form.append("fileName"+i, file.name);
			form.append("size"+i, file.size);

		}
		if(length == 1){
		    let elem = document.getElementById("tips_addmore_div");
	        elem.style.display = "";
        }
        form.append("filenum_sum", length);
        if(sizeM > uploadOption.maxsize){
            //文件大小不符合要求
            if(uploadOption.errorCallback!=undefined && uploadOption.errorCallback!=null){
                uploadOption.errorCallback("文件大小不符合要求");
            }
            else{
                alert("文件大小不符合要求");
            }
            //reject("文件大小不符合要求");
            return;
        }

        if(uploadOption.params!=null){
            for(let key in uploadOption.params){
                form.append(key, uploadOption.params[key]);
            }
        }

		var xhr = false;
			if (window.XMLHttpRequest) {
				xhr = new XMLHttpRequest();
				if(xhr.overrideMimeType){
					xhr.overrideMimeType("text/xml");
				}
			} else if(window.ActiveXObject) {
				try{
					xhr = new ActiveXObject("Msxml2.XMLHTTP");
				}catch (e) {
					try {
						xhr = new ActiveXObject("Microsoft.XMLHTTP")
					}catch (e) {}
				}
			}
			if(!xhr){
				alert("不能创建xmlhttp实例，请不要使用兼容模式或更换浏览器！")
				return false;
			}
        var action = uploadOption.action;
        xhr.open("POST", action);
        // ****** 各种事件的监听 ******
        //开始上传
        xhr.upload.onloadstart = function(event){
            _lastTimestamp = event.timeStamp;
            _lastLoaded = 0;
            if(uploadOption.startCallback!=undefined && uploadOption.startCallback!=null){
                uploadOption.startCallback();
            }
        };
        //上传进度
        xhr.upload.onprogress = function(event){
            var offtimestamp = event.timeStamp - _lastTimestamp;
            _lastTimestamp = event.timeStamp;
            var offloaded = event.loaded - _lastLoaded;
            _lastLoaded = event.loaded;
            offtimestamp = offtimestamp / 1000; //转换成秒
            offloaded = offloaded / 1024; //转换成KB
            var speed = Math.round(offloaded/offtimestamp); // KB/S
            var progress = event.loaded / event.total; // 0~1
            var total = Math.round(event.total/1024); // KB
            if(uploadOption.progressCallback!=undefined && uploadOption.progressCallback!=null){
                uploadOption.progressCallback({
                    computable: event.lengthComputable,
                    speed: speed,
                    progress: progress,
                    total: total,
                    event: event
                });
            }
        };
        //上传完成
//        xhr.onload = function(event){
//            if(uploadOption.successCallback!=undefined && uploadOption.successCallback!=null){
//                var resultObj;
//                try {
//                    resultObj = JSON.parse(xhr.responseText);
//                } catch (error) {
//                    resultObj = xhr.responseText;
//                }
//                uploadOption.successCallback(resultObj);
//            }
//        };
        //上传错误
        xhr.onerror =  function(event){
            if(uploadOption.errorCallback!=undefined && uploadOption.errorCallback!=null){
                uploadOption.errorCallback();
            }
        };
        //状态变化
        xhr.onreadystatechange = function(){
            if(xhr.readyState==4){
                if(xhr.status==200){
                    try {
                        var resultObj = JSON.parse(xhr.responseText);
                    } catch (e) {
						var resultObj = xhr.responseText;
                    }
					uploadOption.successCallback(resultObj);
                }
				else{
					uploadOption.errorCallback();
				}

            }
        }
        xhr.send(form);
        xmlhttp.send(null);
        input.value = '';
        input.outerHTML = '';
}


function onload_start(){
	let elem = document.getElementById("myBar");
	elem.style.display = "";
	return true;
}


function onload_progress(event){
	let elem = document.getElementById("progress");
	let progress_num = document.getElementById("progress_num");
	if (1 == event.progress)
    {
        progress_num.innerHTML = "正在处理";
    }
	else
    {
    	progress_num.innerHTML = elem.style.width = event.progress*100 + "%";
    }

//	alert(elem.style.width);
}


function onload(resultObj){
    if(resultObj["status"]==="success") {
        let progress_num = document.getElementById("progress_num");
        progress_num.innerHTML = "上传成功";
        is_onload = 1;
    }
}


function onload_error(){
	let progress_num = document.getElementById("progress_num");	
	alert("上传错误");
	progress_num.innerHTML = "上传错误";
}


function is_weixin(){
    var ua = navigator.userAgent.toLowerCase();
    if(ua.match(/MicroMessenger/i)=="micromessenger") {
        if(ua.match(/Mobile/i)=="mobile"){
            return true;
        }
        return false;
    }
    else {
        return false;
    }
}
